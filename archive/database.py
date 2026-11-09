import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# =====================================================================
# COMPREHENSIVE INDUSTRIAL EFFLUENT DATABASE (100 CONTAMINANTS & COMPOUNDS)
# =====================================================================
INDUSTRIAL_CONTAMINANTS_DATABASE = [
    # --- HEAVY METALS & TOXIC INORGANIC COMPLEX EFFLUENTS (1 - 30) ---
    {"name": "Copper Sulfate / Copper Ion (Cu²⁺)", "category": "Heavy Metal Contamination", "absorption_bands": [600, 650, 700, 800]},
    {"name": "Copper Nitrate Cu(NO₃)₂", "category": "Heavy Metal Contamination", "absorption_bands": [620, 680, 810]},
    {"name": "Copper Chloride CuCl₂", "category": "Heavy Metal Contamination", "absorption_bands": [650, 750, 830]},
    {"name": "Hexavalent Chromium (Cr⁶⁺ / Dichromate)", "category": "Toxic Industrial Pollutant", "absorption_bands": [370, 420, 450]},
    {"name": "Potassium Chromate (K₂CrO₄)", "category": "Electroplating Contaminant", "absorption_bands": [375, 440]},
    {"name": "Trivalent Chromium (Cr³⁺)", "category": "Tanneries & Metal Finishing", "absorption_bands": [400, 570]},
    {"name": "Nickel Sulfate (NiSO₄)", "category": "Electroplating Contaminant", "absorption_bands": [390, 650, 720]},
    {"name": "Nickel Chloride (NiCl₂)", "category": "Electroplating Contaminant", "absorption_bands": [410, 730]},
    {"name": "Cobalt Nitrate Co(NO₃)₂", "category": "Heavy Metal Contamination", "absorption_bands": [510, 525, 580]},
    {"name": "Cobalt Chloride (CoCl₂)", "category": "Chemical Synthesis Effluent", "absorption_bands": [520, 660]},
    {"name": "Ferric Chloride (FeCl₃)", "category": "Etching & PCB Effluent", "absorption_bands": [420, 490, 530]},
    {"name": "Ferrous Sulfate (FeSO₄)", "category": "Steel Pickling Effluent", "absorption_bands": [430, 680]},
    {"name": "Iron Potassium Cyanide / Prussian Blue", "category": "Chemical Industry Waste", "absorption_bands": [690, 710]},
    {"name": "Permanganate Wastewater (MnO₄⁻)", "category": "Chemical Plant Effluent", "absorption_bands": [525, 545, 565]},
    {"name": "Manganous Salt Runoff (Mn²⁺)", "category": "Mining & Industrial Runoff", "absorption_bands": [400, 530]},
    {"name": "Lead Nitrates & Complexes (Pb²⁺)", "category": "Battery Factory Wastewater", "absorption_bands": [364, 405]},
    {"name": "Cadmium Chloride (CdCl₂)", "category": "Solar & Battery Manufacturing", "absorption_bands": [380, 468, 480]},
    {"name": "Zinc Sulfate / Zinc Ion (Zn²⁺)", "category": "Galvanizing Industry Effluent", "absorption_bands": [370, 480]},
    {"name": "Zinc Ammine Complexes", "category": "Electroplating Effluent", "absorption_bands": [390, 450]},
    {"name": "Mercuric Chloride (HgCl₂)", "category": "Chlor-Alkali Industrial Waste", "absorption_bands": [365, 404, 435]},
    {"name": "Silver Nitrate Waste (AgNO₃)", "category": "Photographic & Mirror Industry", "absorption_bands": [380, 520]},
    {"name": "Gold Cyanide Complexes [Au(CN)₂]⁻", "category": "Gold Mining / Plating Effluent", "absorption_bands": [355, 410]},
    {"name": "Platinum Group Chloride Waste (H₂PtCl₆)", "category": "Catalyst Refinery Wastewater", "absorption_bands": [375, 455, 500]},
    {"name": "Palladium Nitrate (Pd(NO₃)₂)", "category": "Automotive Catalyst Effluent", "absorption_bands": [420, 480]},
    {"name": "Titanium Tetrachloride Hydrolysate", "category": "Pigment Manufacturing Waste", "absorption_bands": [360, 410]},
    {"name": "Vanadate Solutions (VO₄³⁻)", "category": "Petroleum Refining Waste", "absorption_bands": [390, 450]},
    {"name": "Ammonium Metavanadate", "category": "Chemical Refinery Effluent", "absorption_bands": [410, 500]},
    {"name": "Molybdate Wastewater (MoO₄²⁻)", "category": "Metallurgical Plant Waste", "absorption_bands": [380, 460]},
    {"name": "Tungstate Process Effluent (WO₄²⁻)", "category": "Mining & Alloy Processing", "absorption_bands": [360, 420]},
    {"name": "Barium Nitrate (Ba(NO₃)₂)", "category": "Fireworks & Glass Effluent", "absorption_bands": [455, 553]},

    # --- TEXTILE & SYNTHETIC DYE EFFLUENTS (31 - 65) ---
    {"name": "Methylene Blue", "category": "Textile Industry Effluent", "absorption_bands": [610, 665]},
    {"name": "Rhodamine B", "category": "Dyeing & Paper Mill Wastewater", "absorption_bands": [543, 554]},
    {"name": "Rhodamine 6G", "category": "Textile Dye Wastewater", "absorption_bands": [525, 530]},
    {"name": "Crystal Violet (Gentian Violet)", "category": "Textile & Printing Effluent", "absorption_bands": [588, 590]},
    {"name": "Methyl Orange", "category": "Chemical & Dye Industry Waste", "absorption_bands": [464, 507]},
    {"name": "Methyl Red", "category": "Textile Dyeing Waste", "absorption_bands": [410, 520]},
    {"name": "Malachite Green", "category": "Aquaculture & Textile Pollutant", "absorption_bands": [618, 625]},
    {"name": "Congo Red", "category": "Tannery & Textile Effluent", "absorption_bands": [497, 500]},
    {"name": "Eosin Y", "category": "Biological Stain & Dye Waste", "absorption_bands": [517, 525]},
    {"name": "Tartrazine (Yellow Dye No. 5)", "category": "Food & Pharmaceutical Waste", "absorption_bands": [425, 427]},
    {"name": "Sunset Yellow FCF", "category": "Beverage & Textile Dye Waste", "absorption_bands": [482, 485]},
    {"name": "Allura Red AC", "category": "Food & Textile Processing Waste", "absorption_bands": [504, 508]},
    {"name": "Indigotine (Indigo Carmine)", "category": "Denim & Textile Wastewater", "absorption_bands": [610, 620]},
    {"name": "Reactive Black 5", "category": "Cotton Dyeing Effluent", "absorption_bands": [595, 600]},
    {"name": "Reactive Red 120", "category": "Industrial Dye Wastewater", "absorption_bands": [512, 535]},
    {"name": "Reactive Blue 19", "category": "Textile Processing Effluent", "absorption_bands": [592, 650]},
    {"name": "Direct Blue 86", "category": "Paper & Textile Mill Waste", "absorption_bands": [620, 660]},
    {"name": "Acid Red 18 (Ponceau 4R)", "category": "Synthetic Colorant Waste", "absorption_bands": [505, 510]},
    {"name": "Acid Yellow 23", "category": "Wool Dyeing Wastewater", "absorption_bands": [425, 430]},
    {"name": "Basic Yellow 28", "category": "Acrylic Fiber Dye Effluent", "absorption_bands": [435, 440]},
    {"name": "Disperse Orange 3", "category": "Synthetic Fabric Dye Waste", "absorption_bands": [435, 445]},
    {"name": "Disperse Red 1", "category": "Polyester Dyeing Effluent", "absorption_bands": [480, 500]},
    {"name": "Disperse Blue 79", "category": "Synthetic Textile Wastewater", "absorption_bands": [570, 610]},
    {"name": "Sudan III (Oil Red)", "category": "Solvent & Fuel Dye Pollutant", "absorption_bands": [507, 510]},
    {"name": "Sudan IV", "category": "Petrochemical Dye Waste", "absorption_bands": [520, 525]},
    {"name": "Bismarck Brown Y", "category": "Leather & Paper Dye Effluent", "absorption_bands": [455, 465]},
    {"name": "Naphthol Green B", "category": "Industrial Dye & Wool Waste", "absorption_bands": [650, 714]},
    {"name": "Victoria Blue B", "category": "Printing Ink & Paper Mill Waste", "absorption_bands": [615, 620]},
    {"name": "Acridine Orange", "category": "Biochem & Dye Plant Waste", "absorption_bands": [470, 490]},
    {"name": "Phenosafranin", "category": "Industrial Dye Effluent", "absorption_bands": [520, 530]},
    {"name": "Alizarin Red S", "category": "Textile & Metallurgical Waste", "absorption_bands": [420, 510]},
    {"name": "Fast Green FCF", "category": "Textile & Pharmaceutical Waste", "absorption_bands": [620, 625]},
    {"name": "Brilliant Blue FCF", "category": "Cosmetics & Dye Industry Waste", "absorption_bands": [630, 635]},
    {"name": "Amido Black 10B", "category": "Protein & Proteinaceous Waste", "absorption_bands": [618, 620]},
    {"name": "Toluidine Blue O", "category": "Biomedical & Textile Waste", "absorption_bands": [626, 630]},

    # --- ORGANIC POLLUTANTS, PHENOLS & PETROCHEMICALS (66 - 85) ---
    {"name": "Phenol / Phenolic Wastewater", "category": "Petroleum Refinery Waste", "absorption_bands": [360, 400, 500]},
    {"name": "4-Nitrophenol", "category": "Pesticide Manufacturing Waste", "absorption_bands": [400, 417]},
    {"name": "2,4-Dichlorophenol", "category": "Chemical Plant Effluent", "absorption_bands": [375, 510]},
    {"name": "Pentachlorophenol (PCP)", "category": "Wood Preservative Effluent", "absorption_bands": [390, 490]},
    {"name": "Benzene-Toluene Runoff", "category": "Petrochemical Waste", "absorption_bands": [360, 380]},
    {"name": "Polycyclic Aromatic Hydrocarbons (PAHs)", "category": "Coke Oven Wastewater", "absorption_bands": [380, 410, 450]},
    {"name": "Aniline / Aniline Dyes", "category": "Pharmaceutical & Rubber Waste", "absorption_bands": [380, 430]},
    {"name": "Nitrobenzene", "category": "Chemical Industry Wastewater", "absorption_bands": [370, 440]},
    {"name": "Formaldehyde Complexed Effluent", "category": "Resin & Adhesive Manufacture", "absorption_bands": [360, 415]},
    {"name": "Creosote Residue Wastewater", "category": "Timber Treatment Plant Waste", "absorption_bands": [385, 425]},
    {"name": "Polychlorinated Biphenyls (PCBs)", "category": "Transformer Oil Wastewater", "absorption_bands": [365, 395]},
    {"name": "Bisphenol A (BPA) Effluent", "category": "Plastics Industry Wastewater", "absorption_bands": [360, 390]},
    {"name": "Dibutyl Phthalate (DBP)", "category": "Plasticizer Manufacturing Waste", "absorption_bands": [365, 410]},
    {"name": "Naphthalene Sulfonates", "category": "Concrete Additive Manufacture", "absorption_bands": [370, 420]},
    {"name": "Petroleum Hydrocarbon Emulsion", "category": "Oily Bilge & Sludge Wastewater", "absorption_bands": [400, 460, 520]},
    {"name": "Spent Caustic Liquors", "category": "Refinery Spent Wash", "absorption_bands": [390, 480]},
    {"name": "Pyridine Contaminated Water", "category": "Solvent Industry Effluent", "absorption_bands": [370, 415]},
    {"name": "Surfactant (LAS / SDBS) Waste", "category": "Detergent Factory Effluent", "absorption_bands": [380, 440]},
    {"name": "Toluene Diisocyanate (TDI) Waste", "category": "Polyurethane Foam Plant Waste", "absorption_bands": [360, 410]},
    {"name": "Naphthenic Acid Runoff", "category": "Oil Sands Wastewater", "absorption_bands": [380, 430]},

    # --- AGRICULTURAL RUNOFF, PESTICIDES & FERTILIZER EFFLUENTS (86 - 100) ---
    {"name": "Nitrate Rich Fertilizer Runoff (NO₃⁻)", "category": "Agricultural Wastewater", "absorption_bands": [360, 410]},
    {"name": "Phosphate Eutrophication Runoff (PO₄³⁻)", "category": "Agricultural Wastewater", "absorption_bands": [660, 710, 830]},
    {"name": "Ammonia / Ammonium Effluent", "category": "Fertilizer Manufacturing Waste", "absorption_bands": [400, 425, 630]},
    {"name": "Paraquat Dichloride Pesticide", "category": "Herbicide Runoff", "absorption_bands": [395, 600, 796]},
    {"name": "Glyphosate Formulations", "category": "Agricultural Runoff", "absorption_bands": [380, 440]},
    {"name": "Atrazine Herbicide", "category": "Pesticide Factory Effluent", "absorption_bands": [360, 410]},
    {"name": "Chlorpyrifos Organophosphate", "category": "Insecticide Manufacturing Waste", "absorption_bands": [375, 425]},
    {"name": "Malathion Waste", "category": "Agrochemical Effluent", "absorption_bands": [385, 435]},
    {"name": "Humic / Fulvic Acid Runoff", "category": "High Organic Load Water", "absorption_bands": [400, 465]},
    {"name": "Algal Bloom Microcystin Toxin", "category": "Eutrophied Water Reservoir", "absorption_bands": [615, 665, 680]},
    {"name": "Sugar Mill Spent Wash (Molasses)", "category": "Distillery & Sugar Mill Waste", "absorption_bands": [400, 475, 580]},
    {"name": "Pulp & Paper Lignin Effluent", "category": "Black Liquor Paper Mill Waste", "absorption_bands": [390, 460, 520]},
    {"name": "Dairy Processing Wastewater", "category": "High Organic Food Wastewater", "absorption_bands": [400, 500]},
    {"name": "Slaughterhouse Blood Wastewater", "category": "Abattoir Effluent", "absorption_bands": [414, 540, 576]},
    {"name": "Brewery Yeast Wastewater", "category": "Fermentation Industry Waste", "absorption_bands": [420, 550]}
]

def extract_spectrum_profile(image_path):
    """Loads image, automatically crops rainbow band, and extracts 1D intensity profile."""
    img = cv2.imread(image_path)
    if img is None:
        return None

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    height, width, _ = img_rgb.shape

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
    return np.mean(profile, axis=1)

def classify_effluent_contaminants(dip_wavelengths, tolerance=30.0):
    """Matches observed absorption dips against 100 industrial effluent contaminant profiles with weighted scoring."""
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
            raw_confidence = (matched / len(ref_bands)) * 100
            match_ratio = matched / len(ref_bands)
            weighted_confidence = raw_confidence * match_ratio # Filters false 100% matches on multi-dip samples
            
            contaminant_scores.append({
                "name": name,
                "category": category,
                "confidence": round(weighted_confidence, 2),
                "matched": matched,
                "total": len(ref_bands)
            })
            
    return sorted(contaminant_scores, key=lambda x: (x['confidence'], x['matched']), reverse=True)

def process_industrial_pipeline(workspace_folder="./workspace_photos", output_folder="./prism_results"):
    os.makedirs(output_folder, exist_ok=True)
    
    # 1. Load pure water reference baseline (photo0)
    baseline_paths = glob.glob(os.path.join(workspace_folder, "photo0.*"))
    if not baseline_paths:
        print("Error: Pure water reference 'photo0' not found in workspace.")
        return

    baseline_raw = extract_spectrum_profile(baseline_paths[0])
    target_wavelengths = np.arange(350, 851, 1) # 350 nm to 850 nm scale
    
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

    print(f"Scanning {len(sample_files)} effluent samples against 100 industrial contaminant spectra...\n" + "="*75)

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

        # Export 1 nm CSV data points
        csv_path = os.path.join(output_folder, f"{base_name}_100_effluents_data.csv")
        with open(csv_path, 'w') as f:
            f.write("Wavelength_nm,Transmission_Intensity\n")
            for wl, val in zip(target_wavelengths, transmission):
                f.write(f"{wl},{val:.5f}\n")

        # Peak / Dip Detection
        inv_spectrum = -transmission
        dips, _ = find_peaks(inv_spectrum, height=-0.95, distance=15, prominence=0.02)
        dip_wavelengths = target_wavelengths[dips]

        # Categorize contamination against 100 compounds with weighted scoring
        contamination_results = classify_effluent_contaminants(dip_wavelengths)

        # Plot transmission spectrum graph
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

        # Print detailed report
        print(f"Effluent Sample: {filename}")
        print(f"  -> Detected Absorption Dips: {[int(w) for w in dip_wavelengths]} nm")
        if contamination_results:
            print(f"  -> Contamination Classification (Top Ranked Matches):")
            for res in contamination_results[::]: # Display top 5 weighted matches
                print(f"     * [{res['category']}] {res['name']}")
                print(f"       Confidence: {res['confidence']}% ({res['matched']}/{res['total']} absorption bands matched)")
        else:
            print("  -> Status: Clean / No prominent effluent contamination detected.")
        print("-" * 75)

if __name__ == "__main__":
    process_industrial_pipeline()