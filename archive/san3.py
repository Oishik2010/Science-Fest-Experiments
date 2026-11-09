import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# =====================================================================
# INDUSTRIAL EFFLUENT & CONTAMINANT SPECTROPHOTOMETRIC DATABASE
# Maps wastewater contaminants to their characteristic absorption bands (nm)
# =====================================================================
INDUSTRIAL_CONTAMINANTS_DATABASE = [
    {
        "name": "Copper Sulfate / Copper Ion (Cu²⁺)",
        "category": "Heavy Metal Contamination",
        "absorption_bands": [600, 650, 700, 800] # Strong red/near-IR absorption
    },
    {
        "name": "Hexavalent Chromium (Cr⁶⁺ / Dichromate)",
        "category": "Toxic Industrial Pollutant",
        "absorption_bands": [370, 420, 450]     # Strong UV-blue absorption
    },
    {
        "name": "Trivalent Chromium (Cr³⁺)",
        "category": "Heavy Metal Contamination",
        "absorption_bands": [400, 570]           # Blue-green / green absorption
    },
    {
        "name": "Nickel Effluent (Ni²⁺)",
        "category": "Electroplating Contaminant",
        "absorption_bands": [390, 720]           # Green complex absorption
    },
    {
        "name": "Cobalt Effluent (Co²⁺)",
        "category": "Heavy Metal Contamination",
        "absorption_bands": [510, 525, 580]      # Pink/red complex absorption
    },
    {
        "name": "Iron / Ferric Complexes (Fe³⁺)",
        "category": "Industrial Runoff Pollutant",
        "absorption_bands": [490, 530]           # Yellow/brown water contaminant
    },
    {
        "name": "Permanganate Wastewater (MnO₄⁻)",
        "category": "Chemical Plant Effluent",
        "absorption_bands": [525, 545, 565]      # Purple dye/oxidizer bands
    },
    {
        "name": "Methylene Blue (Synthetic Dye)",
        "category": "Textile Industry Effluent",
        "absorption_bands": [610, 665]           # Organic dye absorption
    },
    {
        "name": "Lead Effluent Complexes (Pb²⁺)",
        "category": "Toxic Heavy Metal",
        "absorption_bands": [283, 364, 405]      # UV-blue boundary absorption
    },
    {
        "name": "Cadmium Effluent (Cd²⁺)",
        "category": "Industrial Metal Contaminant",
        "absorption_bands": [326, 468, 480]      # Metal salt absorption
    }
]

def extract_spectrum_profile(image_path):
    """Loads image, automatically crops the prism rainbow, and extracts the 1D intensity profile."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img_rgb.shape

    # Convert to HSV to isolate the vibrant rainbow band
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation = hsv[:, :, 1]
    value = hsv[:, :, 2]
    
    col_scores = np.mean(saturation, axis=0) * np.mean(value, axis=0)
    valid_cols = np.where(col_scores > (np.max(col_scores) * 0.15))[0]

    if len(valid_cols) > 0:
        x_min, x_max = max(0, valid_cols[0] - 15), min(width, valid_cols[-1] + 15)
    else:
        x_min, x_max = int(width * 0.45), int(width * 0.65)

    row_scores = np.mean(saturation, axis=1) * np.mean(value, axis=1)
    valid_rows = np.where(row_scores > (np.max(row_scores) * 0.15))[0]
    
    if len(valid_rows) > 0:
        y_min, y_max = max(0, valid_rows[0] - 10), min(height, valid_rows[-1] + 10)
    else:
        y_min, y_max = int(height * 0.1), int(height * 0.9)

    cropped_img = img_rgb[y_min:y_max, x_min:x_max]
    profile = np.mean(cropped_img, axis=0)
    intensity = np.mean(profile, axis=1)
    return intensity

def classify_effluent_contaminants(dip_wavelengths, tolerance=30.0):
    """Matches observed absorption dips against known industrial effluent contaminant profiles."""
    contaminant_scores = []
    
    for item in INDUSTRIAL_CONTAMINANTS_DATABASE:
        name = item["name"]
        category = item["category"]
        ref_bands = item["absorption_bands"]
        
        matched = 0
        for band in ref_bands:
            if any(np.abs(dip_wavelengths - band) <= tolerance):
                matched += 1
                
        if matched > 0:
            confidence = (matched / len(ref_bands)) * 100
            contaminant_scores.append({
                "name": name,
                "category": category,
                "confidence": round(confidence, 2),
                "matched": matched,
                "total": len(ref_bands)
            })
            
    return sorted(contaminant_scores, key=lambda x: x['confidence'], reverse=True)

def process_industrial_pipeline(workspace_folder="./workspace_photos", output_folder="./prism_results"):
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Load pure water baseline (photo0)
    baseline_paths = glob.glob(os.path.join(workspace_folder, "photo0.*"))
    if not baseline_paths:
        print("Error: Pure water reference 'photo0' not found in workspace.")
        return

    baseline_raw = extract_spectrum_profile(baseline_paths[0])
    target_wavelengths = np.arange(350, 851, 1) # Standard 350 nm to 850 nm scale
    
    baseline_intensity = np.interp(
        np.linspace(0, 1, len(target_wavelengths)),
        np.linspace(0, 1, len(baseline_raw)),
        baseline_raw
    )

    # 2. Find sample effluent photos (excluding photo0)
    sample_files = [f for f in glob.glob(os.path.join(workspace_folder, "*.*")) if "photo0" not in os.path.basename(f).lower()]
    if not sample_files:
        print("No effluent sample photos found to analyze.")
        return

    print(f"Analyzing {len(sample_files)} effluent samples (350 nm - 850 nm) for contamination...\n" + "="*70)

    for sample_path in sample_files:
        filename = os.path.basename(sample_path)
        base_name, _ = os.path.splitext(filename)
        
        sample_raw = extract_spectrum_profile(sample_path)
        if sample_raw is None:
            continue

        sample_intensity = np.interp(
            np.linspace(0, 1, len(target_wavelengths)),
            np.linspace(0, 1, len(sample_raw)),
            sample_raw
        )

        # Baseline Correction (Sample / Pure Water Transmission)
        transmission = sample_intensity / (baseline_intensity + 1e-6)

        # Save 1 nm CSV data points
        csv_path = os.path.join(output_folder, f"{base_name}_effluent_data_350_850.csv")
        with open(csv_path, 'w') as f:
            f.write("Wavelength_nm,Transmission_Intensity\n")
            for wl, val in zip(target_wavelengths, transmission):
                f.write(f"{wl},{val:.5f}\n")

        # Find absorption dips (valleys in transmission)
        inv_spectrum = -transmission
        dips, _ = find_peaks(inv_spectrum, height=-0.95, distance=15, prominence=0.02)
        dip_wavelengths = target_wavelengths[dips]

        # Classify Effluent Contamination
        contamination_results = classify_effluent_contaminants(dip_wavelengths)

        # Plot and save diagnostic graph
        plt.figure(figsize=(10, 4))
        plt.plot(target_wavelengths, transmission, color='teal', linewidth=1.5)
        plt.title(f"Effluent Absorption Spectrum (350nm-850nm) - {filename}")
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Relative Transmission (Sample / Pure Water)")
        plt.xlim(350, 850)
        plt.grid(True, linestyle='--', alpha=0.6)
        
        graph_path = os.path.join(output_folder, f"{base_name}_effluent_graph.png")
        plt.savefig(graph_path, dpi=300, bbox_inches='tight')
        plt.close()

        # Print detailed report to console
        print(f"Effluent Sample: {filename}")
        print(f"  -> Detected Absorption Dips: {[int(w) for w in dip_wavelengths]} nm")
        if contamination_results:
            print(f"  -> Contamination Classification (Ranked):")
            for res in contamination_results[::]: # Top 3 matches
                print(f"     * [{res['category']}] {res['name']}")
                print(f"       Confidence: {res['confidence']}% ({res['matched']}/{res['total']} absorption bands matched)")
        else:
            print("  -> Status: Clean / No prominent effluent contamination detected.")
        print("-" * 70)

if __name__ == "__main__":
    process_industrial_pipeline()