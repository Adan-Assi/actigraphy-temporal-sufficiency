# Assessing Temporal Sufficiency of Circadian Actigraphy Features

## Overview
This project investigates a fundamental methodological question in digital phenotyping: **When does a temporal segment of actigraphy data become sufficient to support meaningful circadian representations?**

The motivation stems from clinical monitoring—such as the early phases of SSRI treatment—where risk assessment must rely on limited data. While short observation periods are necessary for rapid intervention, they often produce noisy and unreliable representations. 

---

## The Core Thesis: The Inverse Trade-off

Through an analysis of the **DEPRESJON** dataset (23 Depressed, 32 Control), this project identifies a critical **Inverse Trade-off**:
* **Stable features (e.g., Amplitude)** are often the least clinically informative.
* **Informative features (e.g., Acrophase)** are often the least stable.

**Representation sufficiency is feature-dependent.** There is no single "sufficient" window length; instead, the optimal window must be balanced between the mathematical stability of the feature and its discriminative power.

---

## Key Results at a Glance

* **The 5-Day "Sweet Spot":** Most circadian features reach a reliability threshold ($ICC > 0.60$) at exactly 5 days. 
* **Phase Paradox:** Timing metrics (**Acrophase**) are the strongest group discriminators but require the most data (7+ days) to achieve individual stability.
* **Clinical Recommendation:** 5 days represents the optimal balance between high feature reliability and participant data retention ($N=51$).

> **For a detailed breakdown of findings, statistical tables, and stability plots, see [results/README.md](./results/README.md).**

---

## Methodology: The Dual-Feature Approach

We analyze activity signals through two distinct lenses:

1. **Naive Baseline (Parametric):** Uses a **Cosinor Model** (Sine Fit) to extract Mesor, Amplitude, and Acrophase.
2. **Non-Naive Analysis (Non-Parametric):** Extracts rhythm "quality" metrics including Interdaily Stability ($IS$), Intradaily Variability ($IV$), and Relative Amplitude ($RA$).

---

## Dataset & Preprocessing

* **Dataset:** DEPRESJON (Publicly available via [Zenodo](https://zenodo.org/records/1219550)).
* **Subjects:** 23 Depressed patients, 32 Matched controls.
* **Segmentation:** Raw actigraphy is segmented into day-aligned windows (2, 3, 5, and 7 days).
* **Completeness:** Windows with **$<80\%$ data completeness** per calendar day are excluded to maintain signal integrity.

---
## Getting Started

### 1. Environment Setup
This project requires Python 3.8+ and the dependencies listed in `requirements.txt`. It is recommended to use a virtual environment to manage dependencies:

```bash
# Clone the repository
git clone https://github.com/Adan-Assi/actigraphy-temporal-sufficiency.git
cd actigraphy-temporal-sufficiency

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
### 2. Data Acquisition
The **DEPRESJON** dataset is not included in this repository due to licensing.
1. Download the raw data from [Zenodo](https://zenodo.org/records/1219550).
2. Extract the contents into the `data/` folder.
3. Your directory structure should look like this:

```text
data/
├── condition/       # Patient data from Zenodo
├── control/         # Control data from Zenodo
└── scores.csv       # Metadata file
```
### 3. Running the Analysis
The analysis is structured to be run sequentially within the provided Jupyter Notebooks:

* **`notebooks/sanity_checks.ipynb`**: Run this first to verify data loading, completeness filtering, and to visualize the raw activity signals.
* **`notebooks/temporal_sufficiency_analysis.ipynb`**: The primary analysis engine. This notebook:
    * Extracts **Naive** (Cosinor) and **Non-Naive** (IS/IV/RA) features.
    * Calculates within-subject stability ($ICC$).
    * Computes group separation power (Cohen's $d$).
    * Generates final plots and exports the master results to `results/`.
---

## Repository Structure

```text
actigraphy-temporal-sufficiency/
├── README.md
├── results/
│   ├── README.md                       # Technical findings & interpretations
│   ├── final_stability_profile.png      # Stability Profile (Smoking Gun)
│   └── thesis_feature_comparison.csv    # Master Results Table
├── src/
│   ├── windowing.py      # Window segmentation & completeness checks
│   ├── baselines.py      # Cosinor and Non-parametric feature extraction
│   ├── analysis.py       # Stability (ICC) and Effect Size (Cohen's d) calculations
│   └── features.py       # Feature utility functions
├── notebooks/
│   ├── sanity_checks.ipynb
│   └── temporal_sufficiency_analysis.ipynb # Primary analysis, visualizations, and master export
└── requirements.txt
