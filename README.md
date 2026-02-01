# Assessing Temporal Sufficiency of Circadian Actigraphy Features

## Overview

This project investigates how much actigraphy data is required for circadian features to become stable and informative.

The motivation comes from real-world monitoring scenarios, such as early phases of SSRI treatment, where risk assessment must rely on limited amounts of data. In such settings, waiting for long observation periods is often infeasible, while very short windows may produce noisy and unreliable representations.

Rather than building a detection or deployment system, this project focuses on a methodological question:

**When does a temporal segment of actigraphy data become sufficient to support meaningful circadian representations?**

---

## Research Questions

Using minute-level actigraphy data, we ask:

- When do circadian features become stable within a person?
- At what window length do these features reliably separate depressed and control groups?
- How does classification performance change as a function of window length?

---

## Dataset

- **Dataset:** DEPRESJON  
- **Signal:** Raw actigraphy (single sensor)
- **Resolution:** Minute-level activity data
- **Subjects:** Depressed patients and matched controls

> Note: The dataset is not included in this repository.  
> The DEPRESJON dataset is publicly available via Zenodo:  
> https://zenodo.org/records/1219550  
>  
> Please download the raw data from Zenodo and place the files according to the directory structure described below.

---

## Preprocessing

- Segment raw actigraphy into **day-aligned windows** of varying lengths:
  - 2, 3, 5, 7, and 14 days
- Exclude windows with **<80% data completeness**
- **No imputation** is performed

Each window is treated as a candidate temporal representation.

---

## Feature Extraction

For each window, we compute three core, interpretable circadian features:

- **Circadian Amplitude**
- **Interdaily Stability (IS)**
- **Intradaily Variability (IV)**

Additional features (e.g., L5/M10/RA) are reserved for supplementary robustness checks and are not part of the main analysis.

---

## Analysis Plan

### A. Feature Stability
- Primary metric: **ICC(2,1)** across windows within subjects
- Supplementary metric: within-subject **coefficient of variation (CV%)**

### B. Group Separation
- Compare depressed vs. control groups per window length
- Using either:
  - Linear mixed-effects model, or
  - Cluster-robust t-test
- Report effect sizes and confidence intervals

### C. Classification Performance
- Model: **Logistic regression**
- Separate model per window length
- **Subject-wise 5-fold cross-validation**
- Report:
  - AUC
  - Model coefficients
- Optional subject-level bootstrap for confidence intervals

---

## Interpretation Focus

The analysis aims to identify:

- The **minimum window length** required for stable circadian features
- The **minimum window length** required for reliable group separation

The emphasis is on **representation sufficiency**, not early detection, clinical prediction, or deployment.

---

## Repository Structure

```text
actigraphy-temporal-sufficiency/
├── README.md
├── data/
│   └── README.md        # Instructions for placing DEPRESJON data
├── src/
│   ├── windowing.py     # Window segmentation and completeness checks
│   ├── features.py      # Circadian feature extraction
│   ├── analysis.py      # Stability, separation, and classification analyses
│   └── utils.py
├── notebooks/
│   └── sanity_checks.ipynb
└── requirements.txt
```