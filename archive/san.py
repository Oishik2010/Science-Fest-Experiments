import os
import glob
import cv2
import numpy as np
from scipy.signal import find_peaks

# Expanded atomic emission lines database, focusing heavily on Copper (CuSO4)
ELEMENT_SPECTRA = {
    "Copper (Cu)": [324.8, 327.4, 510.6, 515.3, 521.8, 570.0, 578.2], # Added more Cu lines
    "Sodium (Na)": [589.0, 589.6],
    "Mercury (Hg)": [404.7, 435.8, 546.1, 577.0, 579.1],
    "Hydrogen (H)": [434.0, 486.1, 656.3],
    "Helium (He)": [388.9, 447.1, 501.6, 587.6, 667.8],
    "Neon (Ne)": [540.1, 585.2, 640.2, 650.7, 692.9],
    "Potassium (K)": [404.4, 766.5, 769.9]
}

def extract_curve_from_plot(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_purple = np.array([110, 30, 30])
    upper_purple = np.array([175, 255, 255])
    
    mask = cv2.inRange(hsv, lower_purple, upper_purple)
    y_indices, x_indices = np.where(mask > 0)
    
    if len(x_indices) == 0:
        return None, None

    x_vals, y_vals = [], []
    for x in np.unique(x_indices):
        ys = y_indices[x_indices == x]
        x_vals.append(x)
        y_vals.append(np.min(ys))
        
    x_vals = np.array(x_vals)
    y_vals = np.array(y_vals)
    height = img.shape[0]
    intensity_vals = height - y_vals
    
    return x_vals, intensity_vals

def analyze_spectrum_image(image_path, slope=0.5, intercept=400.0, tolerance=4.0):
    x_vals, intensities = extract_curve_from_plot(image_path)
    if x_vals is None or len(x_vals) == 0:
        return [], []

    # Map pixel x-positions to wavelengths using current calibration
    wavelengths = x_vals * slope + intercept

    min_i, max_i = np.min(intensities), np.max(intensities)
    if max_i - min_i > 0:
        intensities = (intensities - min_i) / (max_i - min_i)
    else:
        intensities = np.zeros_like(intensities)

    peaks, _ = find_peaks(intensities, height=0.05, distance=5, prominence=0.02)
    
    if len(peaks) == 0:
        return [], []

    detected_wavelengths = wavelengths[peaks]
    peak_intensities = intensities[peaks]

    element_scores = []

    for element, ref_lines in ELEMENT_SPECTRA.items():
        matched_lines = 0
        total_matched_intensity = 0.0
        
        for ref_line in ref_lines:
            differences = np.abs(detected_wavelengths - ref_line)
            match_mask = differences <= tolerance
            if np.any(match_mask):
                matched_lines += 1
                best_match_idx = np.argmin(differences)
                total_matched_intensity += peak_intensities[best_match_idx]

        if matched_lines > 0:
            coverage_ratio = matched_lines / len(ref_lines)
            avg_intensity = total_matched_intensity / matched_lines
            confidence = coverage_ratio * avg_intensity * 100
            
            element_scores.append({
                "element": element,
                "confidence": round(confidence, 2),
                "matched_lines": matched_lines,
                "total_lines": len(ref_lines)
            })

    element_scores = sorted(element_scores, key=lambda x: x['confidence'], reverse=True)
    return element_scores, detected_wavelengths

def process_output_folder(output_folder, slope=0.5, intercept=400.0):
    image_files = glob.glob(os.path.join(output_folder, "*_spectrum_graph.png"))
    
    if not image_files:
        print(f"No spectrum graph images found in {output_folder}")
        return

    print(f"Analyzing {len(image_files)} spectrum graphs with wavelength calibration (Slope={slope}, Intercept={intercept})...\n" + "="*60)

    for img_path in image_files:
        filename = os.path.basename(img_path)
        print(f"\nAnalyzing File: {filename}")
        
        results, peak_wls = analyze_spectrum_image(img_path, slope=slope, intercept=intercept)
        
        # Print diagnostic peak wavelengths so we can calibrate
        if len(peak_wls) > 0:
            formatted_wls = [round(w, 1) for w in peak_wls]
            print(f"  -> Detected Peak Wavelengths (nm): {formatted_wls}")
        else:
            print("  -> No peaks detected.")
        
        if not results:
            print("  -> Element Match Result: No matching elements found.")
        else:
            print(f"  {'Element':<20} | {'Confidence':<12} | {'Matched Lines'}")
            print(f"  {'-'*20}-+-{'-'*12}-+-{'-'*15}")
            for res in results:
                print(f"  {res['element']:<20} | {res['confidence']:>6}%      | {res['matched_lines']}/{res['total_lines']}")
        print("-" * 60)

if __name__ == "__main__":
    OUTPUT_FOLDER = "./output_graphs"
    
    # ADJUST THESE IF YOUR PEAK WAVELENGTHS ARE SHIFTED
    SLOPE = 0.5
    INTERCEPT = 400.0
    
    process_output_folder(OUTPUT_FOLDER, slope=SLOPE, intercept=INTERCEPT)