# CPeptide Diabetes Regression

- authors: Jennifer Onyebuchi, Michael Kmetiuk, Victoria Farkas, & Julia Zhang

## About

This repository contains a regression analysis of a Diabetes Mellitus dataset. We built a simple Linear Regression model, using Patient Age and Base Deficit as estimators of the target variable C_Peptide, which is used as a proxy to assess how much insuslin is being produced by the body. The overall analysis was quite simplistic due to the small dataset size and low number of features, with little data cleaning/wrangling needed aside from the initial dataframe setup.

This analysis was created to answer the inferential question: 'When studying patterns of insulin-dependent diabetes mellitus in children, is there a relationship between levels of serum C-Peptide and the factors of patient age and base deficit?', so predictive analysis was excluded. We found no clear outliers or indication of complex relationships between features, and found that both Age and Base Deficit have a medium positive relationship with C-Peptide concentration (Pearson = 0.46 and 0.49). The normality of residuals was assessed through a Shapiro-Wilk test and Q-Q plot and found no indication of abnormality. The final linear equation was determined to be C_peptide = 4.47 + 0.07(Age) + 0.04(Base Deficit).

The data was sourced from KEEL (Knowledge Extraction based on Evolutionary Learning), which is an open source software tool containing datasets that can be used for knowledge data discovery. The chosen dataset is designed for regression analysis, taken from LIACC's repository. The objective of this data is to investigate how factors such as patient age and base deficit (a measure of metabolic acidosis) are associated with concentration of C-peptide, in order to further understand patterns of insulin-resistant Diabetes Mellitus in children.

KEEL Diabetes Dataset (By KEEL). (n.d.). [Dataset]. https://sci2s.ugr.es/keel/dataset.php?cod=45

## Running the analysis

- how to run your data analysis

## Dependencies

- a list of the dependencies needed to run your analysis

## License

The CPeptide Diabetes Regression report contained herein are licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. . If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.

## References

- references
