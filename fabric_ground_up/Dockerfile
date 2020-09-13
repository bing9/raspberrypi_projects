FROM resin/raspberrypi3-python:3.6

USER root

WORKDIR /home/pi

# Update pip and install jupyter
RUN apt-get update && apt-get install -y libncurses5-dev libzmq-dev libfreetype6-dev libpng-dev

RUN pip3 install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
    rm -f requirements.txt


# RUN sed -i "/c.NotebookApp.open_browser/c c.NotebookApp.open_browser = False" /root/.jupyter/jupyter_notebook_config.py \
#     && sed -i "/c.NotebookApp.ip/c c.NotebookApp.ip = '*'" /root/.jupyter/jupyter_notebook_config.py \
#     && sed -i "/c.NotebookApp.notebook_dir/c c.NotebookApp.notebook_dir = '/root/notebooks'" /root/.jupyter/jupyter_notebook_config.py

RUN jupyter labextension install jupyterlab_scheduler --no-build &&\
    jupyter serverextension enable --py jupyterlab &&\
    # jupyter labextension install @jupyterlab/toc --no-build && \
    #     # jupyter labextension install dask-labextension --no-build &&\
    #     # jupyter serverextension enable dask_labextension && \
    #     jupyter serverextension enable --py jupyterlab_git && \
    jupyter lab build && \
    jupyter lab clean && \
    jlpm cache clean && \
    npm cache clean --force && \
    rm -rf $HOME/.node-gyp && \
    rm -rf $HOME/.local

# Add Tini. Tini operates as a process subreaper for jupyter. This prevents kernel crashes.
ENV TINI_VERSION 0.18.0
ENV CFLAGS="-DPR_SET_CHILD_SUBREAPER=36 -DPR_GET_CHILD_SUBREAPER=37"

ADD https://github.com/krallin/tini/archive/v${TINI_VERSION}.tar.gz /root/v${TINI_VERSION}.tar.gz
RUN apt-get install -y cmake
RUN tar zxvf v${TINI_VERSION}.tar.gz \
    && cd tini-${TINI_VERSION} \
    && cmake . \
    && make \
    && cp tini /usr/bin/. \
    && cd .. \
    && rm -rf "./tini-${TINI_VERSION}" \
    && rm "./v${TINI_VERSION}.tar.gz"


ENTRYPOINT ["/usr/bin/tini", "--"]

EXPOSE 8888

CMD ["jupyter", "lab", "--allow-root"]


