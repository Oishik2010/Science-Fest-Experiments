"""
database.py — Industrial Effluent Spectral Database
====================================================
Single source of truth for all 100 contaminant entries.

Each entry contains:
    name                 - compound / effluent name
    category             - industry / source category
    absorption_bands     - list of characteristic wavelengths (nm)
    relative_intensities - normalised absorptivity per band (1.0 = strongest peak)
                           Must be the same length as absorption_bands.

To add or edit a compound, change only this file.
main.py will pick up the changes automatically on the next run.
"""

INDUSTRIAL_CONTAMINANTS_DATABASE = [

    # =========================================================
    # SECTION 1 — HEAVY METALS & TOXIC INORGANIC EFFLUENTS (1-30)
    # =========================================================
    {
        "name": "Copper Sulfate / Copper Ion (Cu²⁺)",
        "category": "Heavy Metal Contamination",
        "absorption_bands":     [600, 650, 700, 800],
        "relative_intensities": [1.0, 0.9, 0.7, 0.5],
    },
    {
        "name": "Copper Nitrate Cu(NO₃)₂",
        "category": "Heavy Metal Contamination",
        "absorption_bands":     [620, 680, 810],
        "relative_intensities": [1.0, 0.8, 0.5],
    },
    {
        "name": "Copper Chloride CuCl₂",
        "category": "Heavy Metal Contamination",
        "absorption_bands":     [650, 750, 830],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Hexavalent Chromium (Cr⁶⁺ / Dichromate)",
        "category": "Toxic Industrial Pollutant",
        "absorption_bands":     [370, 420, 450],
        "relative_intensities": [0.8, 1.0, 0.6],
    },
    {
        "name": "Potassium Chromate (K₂CrO₄)",
        "category": "Electroplating Contaminant",
        "absorption_bands":     [375, 440],
        "relative_intensities": [0.7, 1.0],
    },
    {
        "name": "Trivalent Chromium (Cr³⁺)",
        "category": "Tanneries & Metal Finishing",
        "absorption_bands":     [400, 570],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Nickel Sulfate (NiSO₄)",
        "category": "Electroplating Contaminant",
        "absorption_bands":     [390, 650, 720],
        "relative_intensities": [0.6, 1.0, 0.8],
    },
    {
        "name": "Nickel Chloride (NiCl₂)",
        "category": "Electroplating Contaminant",
        "absorption_bands":     [410, 730],
        "relative_intensities": [0.7, 1.0],
    },
    {
        "name": "Cobalt Nitrate Co(NO₃)₂",
        "category": "Heavy Metal Contamination",
        "absorption_bands":     [510, 525, 580],
        "relative_intensities": [0.9, 1.0, 0.7],
    },
    {
        "name": "Cobalt Chloride (CoCl₂)",
        "category": "Chemical Synthesis Effluent",
        "absorption_bands":     [520, 660],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Ferric Chloride (FeCl₃)",
        "category": "Etching & PCB Effluent",
        "absorption_bands":     [420, 490, 530],
        "relative_intensities": [0.7, 0.9, 1.0],
    },
    {
        "name": "Ferrous Sulfate (FeSO₄)",
        "category": "Steel Pickling Effluent",
        "absorption_bands":     [430, 680],
        "relative_intensities": [1.0, 0.5],
    },
    {
        "name": "Iron Potassium Cyanide / Prussian Blue",
        "category": "Chemical Industry Waste",
        "absorption_bands":     [690, 710],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Permanganate Wastewater (MnO₄⁻)",
        "category": "Chemical Plant Effluent",
        "absorption_bands":     [525, 545, 565],
        "relative_intensities": [0.8, 1.0, 0.9],
    },
    {
        "name": "Manganous Salt Runoff (Mn²⁺)",
        "category": "Mining & Industrial Runoff",
        "absorption_bands":     [400, 530],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Lead Nitrates & Complexes (Pb²⁺)",
        "category": "Battery Factory Wastewater",
        "absorption_bands":     [364, 405],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Cadmium Chloride (CdCl₂)",
        "category": "Solar & Battery Manufacturing",
        "absorption_bands":     [380, 468, 480],
        "relative_intensities": [1.0, 0.7, 0.8],
    },
    {
        "name": "Zinc Sulfate / Zinc Ion (Zn²⁺)",
        "category": "Galvanizing Industry Effluent",
        "absorption_bands":     [370, 480],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Zinc Ammine Complexes",
        "category": "Electroplating Effluent",
        "absorption_bands":     [390, 450],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Mercuric Chloride (HgCl₂)",
        "category": "Chlor-Alkali Industrial Waste",
        "absorption_bands":     [365, 404, 435],
        "relative_intensities": [1.0, 0.8, 0.6],
    },
    {
        "name": "Silver Nitrate Waste (AgNO₃)",
        "category": "Photographic & Mirror Industry",
        "absorption_bands":     [380, 520],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Gold Cyanide Complexes [Au(CN)₂]⁻",
        "category": "Gold Mining / Plating Effluent",
        "absorption_bands":     [355, 410],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Platinum Group Chloride Waste (H₂PtCl₆)",
        "category": "Catalyst Refinery Wastewater",
        "absorption_bands":     [375, 455, 500],
        "relative_intensities": [0.7, 1.0, 0.8],
    },
    {
        "name": "Palladium Nitrate (Pd(NO₃)₂)",
        "category": "Automotive Catalyst Effluent",
        "absorption_bands":     [420, 480],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Titanium Tetrachloride Hydrolysate",
        "category": "Pigment Manufacturing Waste",
        "absorption_bands":     [360, 410],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Vanadate Solutions (VO₄³⁻)",
        "category": "Petroleum Refining Waste",
        "absorption_bands":     [390, 450],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Ammonium Metavanadate",
        "category": "Chemical Refinery Effluent",
        "absorption_bands":     [410, 500],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Molybdate Wastewater (MoO₄²⁻)",
        "category": "Metallurgical Plant Waste",
        "absorption_bands":     [380, 460],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Tungstate Process Effluent (WO₄²⁻)",
        "category": "Mining & Alloy Processing",
        "absorption_bands":     [360, 420],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Barium Nitrate (Ba(NO₃)₂)",
        "category": "Fireworks & Glass Effluent",
        "absorption_bands":     [455, 553],
        "relative_intensities": [1.0, 0.8],
    },

    # =========================================================
    # SECTION 2 — TEXTILE & SYNTHETIC DYE EFFLUENTS (31-65)
    # =========================================================
    {
        "name": "Methylene Blue",
        "category": "Textile Industry Effluent",
        "absorption_bands":     [610, 665],
        "relative_intensities": [0.5, 1.0],  # 665 nm is the primary peak
    },
    {
        "name": "Rhodamine B",
        "category": "Dyeing & Paper Mill Wastewater",
        "absorption_bands":     [543, 554],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Rhodamine 6G",
        "category": "Textile Dye Wastewater",
        "absorption_bands":     [525, 530],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Crystal Violet (Gentian Violet)",
        "category": "Textile & Printing Effluent",
        "absorption_bands":     [588, 590],
        "relative_intensities": [1.0, 0.9],
    },
    {
        "name": "Methyl Orange",
        "category": "Chemical & Dye Industry Waste",
        "absorption_bands":     [464, 507],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Methyl Red",
        "category": "Textile Dyeing Waste",
        "absorption_bands":     [410, 520],
        "relative_intensities": [0.7, 1.0],
    },
    {
        "name": "Malachite Green",
        "category": "Aquaculture & Textile Pollutant",
        "absorption_bands":     [618, 625],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Congo Red",
        "category": "Tannery & Textile Effluent",
        "absorption_bands":     [497, 500],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Eosin Y",
        "category": "Biological Stain & Dye Waste",
        "absorption_bands":     [517, 525],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Tartrazine (Yellow Dye No. 5)",
        "category": "Food & Pharmaceutical Waste",
        "absorption_bands":     [425, 427],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Sunset Yellow FCF",
        "category": "Beverage & Textile Dye Waste",
        "absorption_bands":     [482, 485],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Allura Red AC",
        "category": "Food & Textile Processing Waste",
        "absorption_bands":     [504, 508],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Indigotine (Indigo Carmine)",
        "category": "Denim & Textile Wastewater",
        "absorption_bands":     [610, 620],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Reactive Black 5",
        "category": "Cotton Dyeing Effluent",
        "absorption_bands":     [595, 600],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Reactive Red 120",
        "category": "Industrial Dye Wastewater",
        "absorption_bands":     [512, 535],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Reactive Blue 19",
        "category": "Textile Processing Effluent",
        "absorption_bands":     [592, 650],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Direct Blue 86",
        "category": "Paper & Textile Mill Waste",
        "absorption_bands":     [620, 660],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Acid Red 18 (Ponceau 4R)",
        "category": "Synthetic Colorant Waste",
        "absorption_bands":     [505, 510],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Acid Yellow 23",
        "category": "Wool Dyeing Wastewater",
        "absorption_bands":     [425, 430],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Basic Yellow 28",
        "category": "Acrylic Fiber Dye Effluent",
        "absorption_bands":     [435, 440],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Disperse Orange 3",
        "category": "Synthetic Fabric Dye Waste",
        "absorption_bands":     [435, 445],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Disperse Red 1",
        "category": "Polyester Dyeing Effluent",
        "absorption_bands":     [480, 500],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Disperse Blue 79",
        "category": "Synthetic Textile Wastewater",
        "absorption_bands":     [570, 610],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Sudan III (Oil Red)",
        "category": "Solvent & Fuel Dye Pollutant",
        "absorption_bands":     [507, 510],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Sudan IV",
        "category": "Petrochemical Dye Waste",
        "absorption_bands":     [520, 525],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Bismarck Brown Y",
        "category": "Leather & Paper Dye Effluent",
        "absorption_bands":     [455, 465],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Naphthol Green B",
        "category": "Industrial Dye & Wool Waste",
        "absorption_bands":     [650, 714],
        "relative_intensities": [0.7, 1.0],
    },
    {
        "name": "Victoria Blue B",
        "category": "Printing Ink & Paper Mill Waste",
        "absorption_bands":     [615, 620],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Acridine Orange",
        "category": "Biochem & Dye Plant Waste",
        "absorption_bands":     [470, 490],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Phenosafranin",
        "category": "Industrial Dye Effluent",
        "absorption_bands":     [520, 530],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Alizarin Red S",
        "category": "Textile & Metallurgical Waste",
        "absorption_bands":     [420, 510],
        "relative_intensities": [0.6, 1.0],
    },
    {
        "name": "Fast Green FCF",
        "category": "Textile & Pharmaceutical Waste",
        "absorption_bands":     [620, 625],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Brilliant Blue FCF",
        "category": "Cosmetics & Dye Industry Waste",
        "absorption_bands":     [630, 635],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Amido Black 10B",
        "category": "Protein & Proteinaceous Waste",
        "absorption_bands":     [618, 620],
        "relative_intensities": [0.9, 1.0],
    },
    {
        "name": "Toluidine Blue O",
        "category": "Biomedical & Textile Waste",
        "absorption_bands":     [626, 630],
        "relative_intensities": [0.9, 1.0],
    },

    # =========================================================
    # SECTION 3 — ORGANIC POLLUTANTS, PHENOLS & PETROCHEMICALS (66-85)
    # =========================================================
    {
        "name": "Phenol / Phenolic Wastewater",
        "category": "Petroleum Refinery Waste",
        "absorption_bands":     [360, 400, 500],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "4-Nitrophenol",
        "category": "Pesticide Manufacturing Waste",
        "absorption_bands":     [400, 417],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "2,4-Dichlorophenol",
        "category": "Chemical Plant Effluent",
        "absorption_bands":     [375, 510],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Pentachlorophenol (PCP)",
        "category": "Wood Preservative Effluent",
        "absorption_bands":     [390, 490],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Benzene-Toluene Runoff",
        "category": "Petrochemical Waste",
        "absorption_bands":     [360, 380],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Polycyclic Aromatic Hydrocarbons (PAHs)",
        "category": "Coke Oven Wastewater",
        "absorption_bands":     [380, 410, 450],
        "relative_intensities": [1.0, 0.8, 0.6],
    },
    {
        "name": "Aniline / Aniline Dyes",
        "category": "Pharmaceutical & Rubber Waste",
        "absorption_bands":     [380, 430],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Nitrobenzene",
        "category": "Chemical Industry Wastewater",
        "absorption_bands":     [370, 440],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Formaldehyde Complexed Effluent",
        "category": "Resin & Adhesive Manufacture",
        "absorption_bands":     [360, 415],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Creosote Residue Wastewater",
        "category": "Timber Treatment Plant Waste",
        "absorption_bands":     [385, 425],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Polychlorinated Biphenyls (PCBs)",
        "category": "Transformer Oil Wastewater",
        "absorption_bands":     [365, 395],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Bisphenol A (BPA) Effluent",
        "category": "Plastics Industry Wastewater",
        "absorption_bands":     [360, 390],
        "relative_intensities": [0.8, 1.0],
    },
    {
        "name": "Dibutyl Phthalate (DBP)",
        "category": "Plasticizer Manufacturing Waste",
        "absorption_bands":     [365, 410],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Naphthalene Sulfonates",
        "category": "Concrete Additive Manufacture",
        "absorption_bands":     [370, 420],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Petroleum Hydrocarbon Emulsion",
        "category": "Oily Bilge & Sludge Wastewater",
        "absorption_bands":     [400, 460, 520],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Spent Caustic Liquors",
        "category": "Refinery Spent Wash",
        "absorption_bands":     [390, 480],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Pyridine Contaminated Water",
        "category": "Solvent Industry Effluent",
        "absorption_bands":     [370, 415],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Surfactant (LAS / SDBS) Waste",
        "category": "Detergent Factory Effluent",
        "absorption_bands":     [380, 440],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Toluene Diisocyanate (TDI) Waste",
        "category": "Polyurethane Foam Plant Waste",
        "absorption_bands":     [360, 410],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Naphthenic Acid Runoff",
        "category": "Oil Sands Wastewater",
        "absorption_bands":     [380, 430],
        "relative_intensities": [1.0, 0.8],
    },

    # =========================================================
    # SECTION 4 — AGRICULTURAL RUNOFF, PESTICIDES & FERTILIZERS (86-100)
    # =========================================================
    {
        "name": "Nitrate Rich Fertilizer Runoff (NO₃⁻)",
        "category": "Agricultural Wastewater",
        "absorption_bands":     [360, 410],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Phosphate Eutrophication Runoff (PO₄³⁻)",
        "category": "Agricultural Wastewater",
        "absorption_bands":     [660, 710, 830],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Ammonia / Ammonium Effluent",
        "category": "Fertilizer Manufacturing Waste",
        "absorption_bands":     [400, 425, 630],
        "relative_intensities": [1.0, 0.8, 0.5],
    },
    {
        "name": "Paraquat Dichloride Pesticide",
        "category": "Herbicide Runoff",
        "absorption_bands":     [395, 600, 796],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Glyphosate Formulations",
        "category": "Agricultural Runoff",
        "absorption_bands":     [380, 440],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Atrazine Herbicide",
        "category": "Pesticide Factory Effluent",
        "absorption_bands":     [360, 410],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Chlorpyrifos Organophosphate",
        "category": "Insecticide Manufacturing Waste",
        "absorption_bands":     [375, 425],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Malathion Waste",
        "category": "Agrochemical Effluent",
        "absorption_bands":     [385, 435],
        "relative_intensities": [1.0, 0.8],
    },
    {
        "name": "Humic / Fulvic Acid Runoff",
        "category": "High Organic Load Water",
        "absorption_bands":     [400, 465],
        "relative_intensities": [1.0, 0.7],
    },
    {
        "name": "Algal Bloom Microcystin Toxin",
        "category": "Eutrophied Water Reservoir",
        "absorption_bands":     [615, 665, 680],
        "relative_intensities": [0.6, 1.0, 0.9],
    },
    {
        "name": "Sugar Mill Spent Wash (Molasses)",
        "category": "Distillery & Sugar Mill Waste",
        "absorption_bands":     [400, 475, 580],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Pulp & Paper Lignin Effluent",
        "category": "Black Liquor Paper Mill Waste",
        "absorption_bands":     [390, 460, 520],
        "relative_intensities": [1.0, 0.7, 0.4],
    },
    {
        "name": "Dairy Processing Wastewater",
        "category": "High Organic Food Wastewater",
        "absorption_bands":     [400, 500],
        "relative_intensities": [1.0, 0.6],
    },
    {
        "name": "Slaughterhouse Blood Wastewater",
        "category": "Abattoir Effluent",
        "absorption_bands":     [414, 540, 576],
        "relative_intensities": [1.0, 0.7, 0.8],  # haemoglobin Q-bands
    },
    {
        "name": "Brewery Yeast Wastewater",
        "category": "Fermentation Industry Waste",
        "absorption_bands":     [420, 550],
        "relative_intensities": [1.0, 0.6],
    },
]

