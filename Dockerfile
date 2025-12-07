# use the miniforge base, make sure you specify a version
FROM condaforge/miniforge3:latest
RUN apt-get update && apt-get install -y make

# copy the lockfile into the container
COPY conda-lock.yml conda-lock.yml

# setup conda-lock
RUN conda install -n base -c conda-forge conda-lock -y

# install packages from lockfile into dockerlock environment
RUN conda-lock install -n dockerlock conda-lock.yml

# make dockerlock the default environment
RUN echo "source /opt/conda/etc/profile.d/conda.sh && conda activate dockerlock" >> ~/.bashrc

# set the default shell to use bash with login to pick up bashrc
# this ensures that we are starting from an activated dockerlock environment
SHELL ["/bin/bash", "-l", "-c"]

# expose JupyterLab port
EXPOSE 8888

# sets the default working directory
# this is also specified in the compose file
WORKDIR /workplace

# run JupyterLab on container start
# uses the jupyterlab from the install environment
CMD ["conda", "run", "--no-capture-output", "-n", "dockerlock", "jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--IdentityProvider.token=''", "--ServerApp.password=''"]

# Install Quarto

ARG QUARTO_VERSION=1.8.26

USER root


RUN apt-get update && apt-get install -y wget gdebi-core && \
    echo "Installing Quarto version ${QUARTO_VERSION} for architecture $(uname -m)" && \
    if [ "$(uname -m)" = "aarch64" ] || [ "$(uname -m)" = "arm64" ]; then \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-arm64.deb ; \
    else \
        wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.deb ; \
    fi && \
    gdebi -n quarto-${QUARTO_VERSION}-linux-*.deb && \
    rm quarto-${QUARTO_VERSION}-linux-*.deb && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
