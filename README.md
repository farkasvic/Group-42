# CPeptide Diabetes Regression

- authors: Jennifer Onyebuchi, Michael Kmetiuk, Victoria Farkas, & Julia Zhang

## About

This repository contains a regression analysis of a Diabetes Mellitus dataset. We built a simple Linear Regression model, using Patient Age and Base Deficit as estimators of the target variable C_Peptide, which is used as a proxy to assess how much insuslin is being produced by the body. The overall analysis was quite simplistic due to the small dataset size and low number of features, with little data cleaning/wrangling needed aside from the initial dataframe setup.

This analysis was created to answer the inferential question: 'When studying patterns of insulin-dependent diabetes mellitus in children, is there a relationship between levels of serum C-Peptide and the factors of patient age and base deficit?', so predictive analysis was excluded. We found no clear outliers or indication of complex relationships between features, and found that both Age and Base Deficit have a medium positive relationship with C-Peptide concentration (Pearson = 0.46 and 0.49). The normality of residuals was assessed through a Shapiro-Wilk test and Q-Q plot and found no indication of abnormality. The final linear equation was determined to be C_peptide = 4.47 + 0.07(Age) + 0.04(Base Deficit).

The data was sourced from KEEL (Knowledge Extraction based on Evolutionary Learning), which is an open source software tool containing datasets that can be used for knowledge data discovery. The chosen dataset is designed for regression analysis, taken from LIACC's repository. The objective of this data is to investigate how factors such as patient age and base deficit (a measure of metabolic acidosis) are associated with concentration of C-peptide, in order to further understand patterns of insulin-resistant Diabetes Mellitus in children.

## Dependencies

- [Docker](https://www.docker.com/) is a container solution 
used to manage the software dependencies for this project.
The Docker image used for this project is based on the
`condaforge/miniforge3:latest` image.
Additional dependencies are specified in the [`Dockerfile`](Dockerfile).

## Usage

### First Time Setup

1. [Install](https://www.docker.com/get-started/) and launch Docker on your computer.
2. Clone this GitHub repository.

### Running the Analysis

If using Windows or Mac, make sure that Docker Desktop is running.

1. Navigate to the root of this project on your computer using the command line and enter the following command:

``` 
make run
```

2. Launch Jupyter Lab by navigating to http://localhost:8888 on your web brower. Open `notebooks/diabetes-analysis.ipynb`.

3. Under the "Kernel" menu, click "Restart Kernel and Run All Cells...".

4. To stop running the Docker container and clean up the resources, enter the following command in the command line:

``` 
make clean
```

## Developer notes

### Developer dependencies

- `conda`

### Adding a new dependency

1. Add the dependency to the `environment.yml` on a new branch.

2. Run the following command to update the `conda-lock.yml` file and re-build the Docker image locally and ensure it runs properly:

``` 
make all
```

3. Push the changes to GitHub. A new Docker image will be built and pushed to Docker Hub automatically. It will be tagged with the `latest`.

4. Send a pull request to merge the changes into the `main` branch.


## License

The CPeptide Diabetes Regression report contained herein are licensed under the
[Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0) License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
See [the license file](LICENSE.md) for more information. . If
re-using/re-mixing please provide attribution and link to this webpage.
The software code contained within this repository is licensed under the
MIT license. See [the license file](LICENSE.md) for more information.

## References

KEEL Diabetes Dataset (By KEEL). (n.d.). [Dataset]. https://sci2s.ugr.es/keel/dataset.php?cod=45

Centers for Disease Control and Prevention. (2025, September 17). FASTSTATS - leading causes of death. Centers for Disease Control and Prevention. https://www.cdc.gov/nchs/fastats/leading-causes-of-death.htm

World Health Organization. (n.d.). Diabetes. https://www.who.int/news-room/fact sheets/detail/diabetes

Cleveland Clinic. (2025, July 22). C-peptide test: What it is, purpose, procedure & results. https://my.clevelandclinic.org/health/diagnostics/24242-c-peptide-test
