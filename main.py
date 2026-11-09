"""
Industrial Effluent Spectrophotometric Analyzer (High-Sensitivity Edition)
==========================================================================
Includes lowered thresholds and enhanced peak sensitivity to correctly detect 
low-concentration or dilute contaminated samples without false negatives.
"""

import os
import glob

import cv2
import numpy as np
from scipy.signal import find_peaks
from scipy.spatial.distance import correlation as _correlation_distance

from database import INDUSTRIAL_CONTAMINANTS_DATABASE


# =====================================================================
# 1. SPECTRUM EXTRACTION & GAMMA LINEARIZATION
# =====================================================================

def extract_spectrum_profile(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None

    # Reverse sRGB gamma to restore linear light intensity
    img_linear = np.power(img.astype(np.float32) / 255.0, 2.2)
    height, width, _ = img_linear.shape

    hsv = cv2.cvtColor((img_linear * 255.0).astype(np.uint8), cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]

    col_scores = np.mean(saturation, axis=0) * np.mean(value, axis=0)
    valid_cols = np.where(col_scores > np.max(col_scores) * 0.15)[0]
    if len(valid_cols) > 0:
        x_min = max(0, valid_cols[0] - 15)
        x_max = min(width, valid_cols[-1] + 15)
    else:
        x_min, x_max = int(width * 0.45), int(width * 0.65)

    row_scores = np.mean(saturation, axis=1) * np.mean(value, axis=1)
    valid_rows = np.where(row_scores > np.max(row_scores) * 0.15)[0]
    if len(valid_rows) > 0:
        y_min = max(0, valid_rows[0] - 10)
        y_max = min(height, valid_rows[-1] + 10)
    else:
        y_min, y_max = int(height * 0.1), int(height * 0.9)

    cropped = img_linear[y_min:y_max, x_min:x_max]
    profile = np.mean(cropped, axis=0)
    
    return profile[:, 0]


# =====================================================================
# 2. REFERENCE CURVE SYNTHESIS & BANDWIDTH MODELING
# =====================================================================

def _synthesis_bandwidth(item):
    cat = item["category"].lower()
    if any(k in cat for k in ("dye", "textile", "stain", "colorant", "ink",
                             "pigment", "color")):
        return 15.0
    if any(k in cat for k in ("metal", "electroplat", "inorganic")):
        return 35.0
    return 22.0


def build_reference_curve(item, wavelengths):
    curve = np.ones(len(wavelengths), dtype=float)
    sigma = _synthesis_bandwidth(item)

    for band, intensity in zip(item["absorption_bands"],
                                item["relative_intensities"]):
        dip = intensity * np.exp(-0.5 * ((wavelengths - band) / sigma) ** 2)
        curve -= dip

    return np.clip(curve, 0.0, 1.0)


def precompute_reference_curves(wavelengths):
    return [build_reference_curve(item, wavelengths)
            for item in INDUSTRIAL_CONTAMINANTS_DATABASE]


# =====================================================================
# 3. SCALING-INVARIANT MATCHING
# =====================================================================

def compare_full_spectra_with_scaling(sample_curve, reference_curve):
    if np.std(sample_curve) < 1e-10 or np.std(reference_curve) < 1e-10:
        return 0.0, 0.0

    dist = _correlation_distance(sample_curve, reference_curve)
    if np.isnan(dist):
        return 0.0, 0.0
    shape_sim = max(0.0, 1.0 - dist)

    sample_abs = 1.0 - sample_curve
    ref_abs = 1.0 - reference_curve
    
    max_sample_dip = np.max(sample_abs)
    max_ref_dip = np.max(ref_abs)
    scale = float(max_sample_dip / max_ref_dip) if max_ref_dip > 1e-6 else 1.0
    scale = max(0.0, scale)

    scaled_ref_abs = ref_abs * scale
    rmse = np.sqrt(np.mean((sample_abs - scaled_ref_abs) ** 2))
    amplitude_sim = max(0.0, 1.0 - (rmse / 0.35))

    combined_score = (0.75 * shape_sim + 0.25 * amplitude_sim) * 100.0
    return round(float(combined_score), 2), round(scale, 2)


def _jaccard_peak_score(dip_wavelengths, item, tolerance=6.0):
    ref_bands = item["absorption_bands"]
    n_ref = len(ref_bands)
    n_sample = len(dip_wavelengths)

    if n_sample == 0 or n_ref == 0:
        return 0.0, 0

    matched = sum(
        1 for band in ref_bands
        if np.any(np.abs(dip_wavelengths - band) <= tolerance)
    )
    score = (matched / max(n_ref, n_sample)) * 100.0
    return round(score, 1), matched


def classify_sample(transmission, wavelengths, reference_curves, dip_wavelengths):
    results = []

    for item, ref_curve in zip(INDUSTRIAL_CONTAMINANTS_DATABASE, reference_curves):
        score, scale = compare_full_spectra_with_scaling(transmission, ref_curve)
        jaccard_score, matched = _jaccard_peak_score(dip_wavelengths, item)

        results.append({
            "name": item["name"],
            "category": item["category"],
            "similarity": score,
            "scale_factor": scale,
            "jaccard_score": jaccard_score,
            "peak_matches": matched,
            "total_bands": len(item["absorption_bands"]),
        })

    return sorted(results, key=lambda x: x["similarity"], reverse=True)


# =====================================================================
# 4. TRANSMITTANCE & BASELINE CORRECTION
# =====================================================================

def compute_transmittance(sample_intensity, baseline_intensity):
    # Apply baseline smoothing / continuum normalization to offset slight lighting variations
    ratio = sample_intensity / (baseline_intensity + 1e-6)
    return ratio / np.max(ratio)  # Flatten overall illumination gradient


# =====================================================================
# 5. MAIN ANALYSIS PIPELINE
# =====================================================================

def process_industrial_pipeline(
    workspace_folder="./workspace_photos",
    clean_water_threshold=32.0,  # Lowered to 32% to prevent false negatives on dilute samples
):
    baseline_paths = glob.glob(os.path.join(workspace_folder, "photo0.*"))
    if not baseline_paths:
        print("Error: Pure water reference 'photo0' not found in workspace folder.")
        return

    baseline_raw = extract_spectrum_profile(baseline_paths[0])
    if baseline_raw is None:
        print("Error: Could not read reference baseline image.")
        return

    target_wavelengths = np.arange(350, 851, 1)

    baseline_intensity = np.interp(
        np.linspace(0, 1, len(target_wavelengths)),
        np.linspace(0, 1, len(baseline_raw)),
        baseline_raw,
    )

    print("Synthesizing reference spectra from database...", end=" ", flush=True)
    reference_curves = precompute_reference_curves(target_wavelengths)
    print(f"done ({len(reference_curves)} curves, 350–850 nm @ 1 nm resolution)\n")

    all_files = glob.glob(os.path.join(workspace_folder, "*.*"))
    sample_files = [f for f in all_files if "photo0" not in os.path.basename(f).lower()]
    if not sample_files:
        print("No effluent sample photos found to analyze.")
        return

    print(
        f"Analyzing {len(sample_files)} effluent sample(s) using "
        f"High-Sensitivity Full-Curve Similarity...\n" + "=" * 80
    )

    for sample_path in sample_files:
        filename = os.path.basename(sample_path)

        sample_raw = extract_spectrum_profile(sample_path)
        if sample_raw is None:
            print(f"Warning: Could not read '{filename}'. Skipping.")
            continue

        sample_intensity = np.interp(
            np.linspace(0, 1, len(target_wavelengths)),
            np.linspace(0, 1, len(sample_raw)),
            sample_raw,
        )

        transmission = compute_transmittance(sample_intensity, baseline_intensity)

        # Lowered prominence to 0.005 to capture faint/dilute absorption dips
        dips, _ = find_peaks(
            -transmission,
            height=-0.95,
            distance=15,
            prominence=0.005,
        )
        dip_wavelengths = target_wavelengths[dips]

        results = classify_sample(
            transmission, target_wavelengths, reference_curves, dip_wavelengths
        )
        top_match = results[0] if results else None

        # --- Dual-Gate Clean Water Check ---
        # A sample is clean if:
        # 1. No absorption dips were detected AT ALL (Pure water flat baseline), OR
        # 2. The top similarity score falls below the confidence threshold.
        is_clean = (len(dip_wavelengths) == 0) or (top_match is None or top_match["similarity"] < clean_water_threshold)
        # --- Console Print Report ---
        print(f"\nSample : {filename}")
        print(f"  Detected dips : {[int(w) for w in dip_wavelengths]} nm")
        print()
        print(f"  {'#':<3} {'Similarity':>10}  {'Scale':>7}  {'Jaccard':>8}  "
              f"{'Peaks':>6}  Category / Compound")
        print("  " + "-" * 76)
        for rank, res in enumerate(results[:10], start=1):
            agreement = "✓" if res["jaccard_score"] > 0 else " "
            print(
                f"  {rank:<3} {res['similarity']:>9.2f}%  "
                f"{res['scale_factor']:>7.2f}  "
                f"{res['jaccard_score']:>7.1f}%  "
                f"{res['peak_matches']}/{res['total_bands']:<2} {agreement}   "
                f"[{res['category']}] {res['name']}"
            )

        print("\n" + "=" * 65)
        print(f" WATER SAFETY INSPECTION REPORT")
        print(f" Sample File: {filename}")
        print("=" * 65)

        if is_clean:
            print(" [STATUS] : 🟢 SAFE / CLEAN WATER")
            print(" Result   : No hazardous industrial contaminants detected.")
            print(" Action   : Sample clears environmental baseline standards.")
        else:
            top_compound = top_match['name']
            top_category = top_match['category']
            confidence = top_match['similarity']
            severity = "HIGH" if confidence > 55 else "MODERATE (Trace/Dilute)"
            
            print(f" [STATUS] : 🔴 HAZARDOUS CONTAMINANT DETECTED ({severity})")
            print(f" Compound : {top_compound}")
            print(f" Category : {top_category}")
            print(f" Confidence: {confidence:.1f}% match probability")
            
            print("\n Top Alternative Possibilities:")
            for rank, res in enumerate(results[1:4], start=2):
                print(f"   {rank}. {res['name']} ({res['similarity']:.1f}% match)")
                
        print("=" * 65 + "\n")


if __name__ == "__main__":
    process_industrial_pipeline(
        workspace_folder="./workspace_photos",
        clean_water_threshold=32.0,
    )