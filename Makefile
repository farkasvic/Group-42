.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: all
all: ## runs the targets: cl, build
	make cl
	make build

.PHONY: cl
cl: ## create conda lock for multiple platforms
	# the linux-aarch64 is used for ARM Macs using linux docker container
	conda-lock lock \
		--file environment.yml \
		-p linux-64 \
		-p osx-64 \
		-p osx-arm64 \
		-p win-64 \
		-p linux-aarch64

.PHONY: env
env: ## remove previous and create environment from lock file
	# remove the existing env, and ignore if missing
	conda env remove dockerlock || true
	conda-lock install -n dockerlock conda-lock.yml

.PHONY: build
build: ## build the docker image from the Dockerfile
	docker build -t dockerlock --file Dockerfile .

.PHONY: run
run: ## alias for the up target
	make up

.PHONY: up
up: ## stop and start docker-compose services
	# by default stop everything before re-creating
	make stop
	docker-compose up -d
	docker exec -it dockerlock bash

.PHONY: stop
stop: ## stop docker-compose services and remove conatiner
	docker-compose stop
	docker-compose rm

.PHONY: clean
clean: ## remove all generated files
	rm -rf data/raw/* \
	data/processed/* \
	data/raw/* \
	results/figures/* \
	results/models/* \
	results/tables/* \
	reports/diabetes-analysis.html

.PHONY: files
files: ## runs the scripts and renders the report
	make clean
	python scripts/download_data.py \
		--url=https://sci2s.ugr.es/keel/dataset/data/regression/diabetes.zip \
		--data-dir=data/raw
	python scripts/clean_data.py \
		--input-path=data/raw/diabetes.dat \
		--output-dir=data/processed \
		--output-file=clean_diabetes.csv
	python scripts/data_validation.py \
		--cleaned-data=data/processed/clean_diabetes.csv
	python scripts/eda.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--plot-output=results/figures \
		--table-output=results/tables
	python scripts/modelling.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--model-output=results/models \
		--table-output=results/tables
	python scripts/diagnostics.py \
		--cleaned-data=data/processed/clean_diabetes.csv \
		--model=results/models/lr_model.pickle \
		--plot-output=results/figures \
		--table-output=results/tables
		
	quarto render reports/diabetes-analysis.qmd --to html

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