# Analysis Results & Clinical Interpretations

This directory contains the primary outputs of the temporal sufficiency analysis, including the stability datasets and final visualizations.

## 📊 The "Smoking Gun": Stability Profile
The image `final_stability_profile.png` (generated in the analysis notebook) is the core visual proof of this study's conclusions.

### Clinical Conclusion
> **Methodological Standard:** While clinical studies often rely on 2-3 days of actigraphy, this analysis demonstrates that **5 days** is the minimum threshold required to achieve substantial reliability ($ICC > 0.6$) across both parametric and non-parametric circadian biomarkers. Beyond 5 days, participant attrition ($N=16$) introduces significant sampling bias, identifying the 5-day window as the optimal balance for temporal sufficiency.

---

## 📈 Key Findings

### 1. The 5-Day "Sweet Spot"
* **Reliability Peak:** Activity volume metrics (**Amplitude/Mesor**) reach "Excellent" reliability ($ICC \approx 0.80$) at exactly **5 days**.
* **Phase Instability:** Timing metrics (**Acrophase**) remain erratic within-subject, showing poor reliability across all windows ($ICC < 0.40$).

### 2. The Phase Paradox
* Despite its low individual stability, **Acrophase** is the strongest group discriminator, peaking with a large effect size (Cohen's $d \approx 0.70$) at short durations.
* Conversely, the highly stable **Amplitude** metric demonstrates negligible power in distinguishing depressed patients from controls (Cohen's $d \approx 0.06$).

### 3. The Inverse Trade-off
The analysis demonstrates that features that are the most stable (Amplitude) are often the least clinically informative, while the most informative features (Acrophase) are the least stable. **Representation sufficiency is feature-dependent**; there is no single "sufficient" window length for all circadian metrics.

---

## 📄 Data Files
* `thesis_feature_comparison.csv`: The raw results of the iterative window analysis, containing:
    * `days`: The observation window length (2, 3, 5, or 7 days).
    * `reliability_icc`: Intraclass Correlation Coefficient (ICC 3,1).
    * `n_subjects`: Remaining sample size after attrition filtering.
    * `cohen_d`: Effect size of the separation between Depressed and Control groups.