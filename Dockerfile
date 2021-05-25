FROM continuumio/anaconda3

COPY environment.yml /
RUN apt-get update && apt-get install -y procps && apt-get clean -y
RUN conda env create -f /environment.yml && conda clean -a
ENV PATH /opt/conda/envs/data-repo/bin:$PATH
RUN /bin/bash -c "source activate data-repo"
