# AwareDX: Using machine learning to identify drugs posing increased risk of adverse reactions to women

### Summary

Adverse drug reactions (ADRs) are the fourth leading cause of death in the US. Although women take longer to metabolize medications and experience twice the risk of developing ADRs compared to men, these sex differences are not comprehensively understood. Real-world clinical data provides an opportunity to estimate safety effects in otherwise understudied populations, ie. women. These data, however, are subject to confounding biases and correlated covariates. We present AwareDX, a pharmacovigilance algorithm that leverages advances in machine learning to study sex risks. Our algorithm mitigates these biases and quantifies the differential risk of a drug causing an adverse event in either men or women. We present a resource of 20,817 adverse drug effects posing sex specific risks. We independently validated our algorithm against known pharmacogenetic mechanisms of genes that are sex-differentially expressed. AwareDX presents an opportunity to minimize adverse events by tailoring drug prescription and dosage to sex.

### Setup

1. Install package requirements
    ```
    pip install -r requirements.txt
    ```
2. Copy the `config.ini.example` configuration template file into a new `config.ini` file.
    ```
    cp config.ini.example config.ini
    ```

### Execution

Running the file `pipeline.py` will execute the full pipeline. Individually, the steps are the followings:

1. `select_patients.py`: Pulls cohorts of male and female patients for analysis.
2. `psm_model_rf.py`: Runs propensity score matching on cohorts.
3. `run.py`: In parallel, calculates logROR scores for each drug-adr pair.
4. `important_sex_biased_adr.py`: Filters initial drug-adr pairs to ones that have been previously cited as a common and severe.