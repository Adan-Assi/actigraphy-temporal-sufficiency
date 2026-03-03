# Assessing Temporal Sufficiency of Circadian Actigraphy Features

## Overview

This project investigates how much actigraphy data is required for circadian features to become stable and informative. 

The motivation stems from real-world clinical monitoring, such as the early phases of SSRI treatment, where risk assessment must rely on limited data. In such settings, waiting for long observation periods is often infeasible, yet very short windows may produce noisy and unreliable representations.

Rather than building a classification system, this project addresses a fundamental methodological question:
**When does a temporal segment of actigraphy data become sufficient to support meaningful circadian representations?**

---

## Methodology: The Dual-Feature Approach

We analyze the activity signal through two distinct lenses to evaluate sufficiency across different mathematical representations:

### 1. Naive Baseline (Parametric)
Uses a **Cosinor Model** (Least-Squares Sine Fit) to extract standard circadian parameters based on the assumption of periodicity:
* **Mesor:** The 24-hour rhythm-adjusted mean activity level.
* **Amplitude:** The peak-to-average difference of the fitted wave.
* **Acrophase:** The timing of peak activity (Phase position).

### 2. Non-Naive Analysis (Non-Parametric)
Captures rhythm characteristics that do not assume a sinusoidal shape, reflecting the "quality" of the rhythm:
* **Interdaily Stability ($IS$):** The degree of pattern consistency across days (Regularity).
* **Intradaily Variability ($IV$):** The fragmentation of the rhythm (Rest-activity transitions).
* **Relative Amplitude ($RA$):** The contrast between the most active 10 hours ($M10$) and least active 5 hours ($L5$).

---

## Key Findings & Research Questions

### Q1: When do circadian features become stable within a person?
* **The 5-Day Sweet Spot:** Activity volume metrics (**Amplitude/Mesor**) reach "Excellent" reliability (**$ICC \approx 0.80$**) at exactly **5 days**.
* **Phase Instability:** Timing metrics (**Acrophase**) remain erratic within-subject, showing poor reliability across all windows (**$ICC < 0.40$**).

### Q2: At what window length do features reliably separate groups?
* **The Phase Paradox:** Despite its low individual stability, **Acrophase** is the strongest group discriminator, peaking with a large effect size (**Cohen's $d \approx 0.70$**) at short durations.
* **The Volume Gap:** Conversely, the highly stable **Amplitude** metric demonstrates negligible power in distinguishing depressed patients from controls (**Cohen's $d \approx 0.06$**).

### Q3: How does representation sufficiency change over time?
* **Activity Volume** reaches sufficiency at **5 days**.
* **Circadian Phase** and **Fragmentation ($IV$)** require **7+ days** to balance discriminative power with stable reliability.



---

## Discussion: Clinical Robustness vs. Simple Discovery

The analysis reveals a distinct functional split between the two approaches. While both provide value, they serve different roles in research and clinical deployment.

### 1. The Naive Baseline for "Simple Discovery"
The **Cosinor** approach is highly effective for identifying broad, population-level differences:
* **Insight:** Depressed patients exhibit a significantly earlier and more constrained peak activity timing compared to controls.
* **Limitation:** Acrophase acts as a powerful "snapshot" of group differences but lacks the stability required for individual tracking over time.

### 2. Non-Naive Analysis for "Clinical Robustness"
The **Non-Parametric** indices are preferred for applications requiring consistent, real-world monitoring:
* **Insight:** These features measure regularity and fragmentation, which are biologically representative of circadian decay in mental health.
* **Reliability Advantage:** Non-Naive features avoid the mathematical instability of the sine-fit. They provide a more balanced profile of moderate separation paired with stability trajectories that favor longer-term (7-day) monitoring.

### Final Methodological Conclusion
* **Naive Features** are superior for **discovery** and identifying high-level phase shifts in small datasets.
* **Non-Naive Features** are superior for **clinical robustness**, providing the stable, ecologically valid metrics necessary for real-world monitoring.

---

## Interpretation: The Inverse Trade-off

The analysis demonstrates an **Inverse Trade-off**: features that are the most stable (Amplitude) are the least clinically informative, while the most informative features (Acrophase) are the least stable. This project emphasizes that **representation sufficiency is feature-dependent**; there is no single "sufficient" window length for all circadian metrics.

---

## Dataset & Preprocessing

* **Dataset:** DEPRESJON (Publicly available via [Zenodo](https://zenodo.org/records/1219550)).
* **Subjects:** 23 Depressed patients, 32 Matched controls.
* **Segmentation:** Raw actigraphy is segmented into day-aligned windows (2, 3, 5, 7, and 14 days).
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
│   └── thesis_feature_comparison.csv  # Final Master Table (ICC & Cohen's d)
├── src/
│   ├── windowing.py      # Window segmentation & completeness checks
│   ├── baselines.py      # Cosinor and Non-parametric feature extraction
│   ├── analysis.py       # Stability (ICC) and Effect Size (Cohen's d) calculations
│   └── features.py       # Feature utility functions
├── notebooks/
│   ├── sanity_checks.ipynb
│   └── temporal_sufficiency_analysis.ipynb  # Primary analysis, visualizations, and master export
└── requirements.txt
