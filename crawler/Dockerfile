FROM continuumio/miniconda3:4.7.12-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /home/anaconda/

COPY ./environment.yml ./environment.yml
RUN /opt/conda/bin/conda env update -n base -f environment.yml && /opt/conda/bin/conda clean -afy \
    && find /opt/conda/ -follow -type f -name '*.a' -delete \
    && find /opt/conda/ -follow -type f -name '*.pyc' -delete \
    && find /opt/conda/ -follow -type f -name '*.js.map' -delete

COPY . /home/anaconda/

CMD /opt/conda/bin/conda init > /dev/null && source /home/anaconda/.bashrc && python main.py
