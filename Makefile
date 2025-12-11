.DEFAULT_GOAL := help

## Show this help message
.PHONY: help
help: 
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

## download and extract data
data/raw/diabetes.dat: scripts/download_data.py
	python scripts/download_data.py \
		--url=https://sci2s.ugr.es/keel/dataset/data/regression/diabetes.zip \
		--data-dir=data/raw

## clean and validate data
data/processed/clean_diabetes.csv: data/raw/diabetes.dat scripts/clean_data.py
	python scripts/clean_data.py \
		--input-path=data/raw/diabetes.dat \
		--output-dir=data/processed \
		--output-file=clean_diabetes.csv
	python scripts/data_validation.py \
		--cleaned-data=data/processed/clean_diabetes.csv

## perform EDA and save tables and plots
results/tables/data_summary.txt results/tables/descriptive_stats.md results/figures/c_peptide_distribution.png results/figures/scatterplot_matrix.png results/figures/correlation_heatmap.png: data/processed/clean_diabetes.csv scripts/eda.py
	python scripts/eda.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--plot-output=results/figures \
		--table-output=results/tables

## create and save model information
results/models/lr_model.pickle results/tables/model_summary.csv: data/processed/clean_diabetes.csv scripts/modelling.py
	python scripts/modelling.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--model-output=results/models \
		--table-output=results/tables

## create model diagnostic test results and plots
results/tables/shapiro_wilk.csv results/figures/qq_plot.png results/figures/resid_plot.png: data/processed/clean_diabetes.csv \
results/models/lr_model.pickle \
scripts/diagnostics.py
	python scripts/diagnostics.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--model=results/models/lr_model.pickle \
		--plot-output=results/figures \
		--table-output=results/tables

## render quarto report to html
reports/diabetes-analysis.html: reports/diabetes-analysis.qmd \
reports/references.bib \
data/processed/clean_diabetes.csv \
results/tables/model_summary.csv \
results/figures/c_peptide_distribution.png \
results/figures/scatterplot_matrix.png \
results/figures/correlation_heatmap.png \
results/tables/shapiro_wilk.csv \
results/figures/qq_plot.png \
results/figures/resid_plot.png
	quarto render reports/diabetes-analysis.qmd --to html

## alias for reports/diabetes-analysis.html target
.PHONY: all
all:
	make reports/diabetes-analysis.html

## remove all generated files
.PHONY: clean
clean: 
	rm -f data/raw/* \
	data/processed/* \
	results/figures/* \
	results/models/* \
	results/tables/* \
	reports/diabetes-analysis.html

## create conda lock for multiple platforms
.PHONY: cl
cl: 
	# the linux-aarch64 is used for ARM Macs using linux docker container
	conda-lock lock \
		--file environment.yml \
		-p linux-64 \
		-p osx-64 \
		-p osx-arm64 \
		-p win-64 \
		-p linux-aarch64

## remove previous and create environment from lock file
.PHONY: env
env: 
	# remove the existing env, and ignore if missing
	conda env remove dockerlock || true
	conda-lock install -n dockerlock conda-lock.yml

## build the docker image from the Dockerfile
.PHONY: build
build: 
	docker build -t dockerlock --file Dockerfile .

## alias for the up target
.PHONY: run
run: 
	make up

## stop and start docker-compose services
.PHONY: up
up: ## stop and start docker-compose services
	# by default stop everything before re-creating
	make stop
	docker-compose up -d
	docker exec -it dockerlock bash

## stop docker-compose services and remove conatiner
.PHONY: stop
stop: 
	docker-compose stop
	docker-compose rm

# docker multi architecture build rules (from Claude) -----

.PHONY: docker-build-push
docker-build-push: ## Build and push multi-arch image to Docker Hub (amd64 + arm64)
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		--tag farkasvic/CPeptide-Diabetes-Regression-Group-42:latest \
		--tag farkasvic/CPeptide-Diabetes-Regression-Group-42:local-$(shell git rev-parse --short HEAD) \
		--push \
		.

.PHONY: docker-build-local
docker-build-local: ## Build single-arch image for local testing (current platform only)
	docker build \
		--tag farkasvic/CPeptide-Diabetes-Regression-Group-42:local \
		.