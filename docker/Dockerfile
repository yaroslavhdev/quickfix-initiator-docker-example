FROM python:3

WORKDIR /root

RUN git clone https://github.com/quickfix/quickfix.git
WORKDIR /root/quickfix
RUN git checkout 0b88788
RUN ./bootstrap
RUN ./configure --with-python3 --with-postgresql
RUN make -j4
RUN make install

WORKDIR /root
RUN rm -rf quickfix
RUN ldconfig


ENV WORKING_DIR /app
WORKDIR ${WORKING_DIR}
COPY ./requirements.txt ${WORKING_DIR}/requirements.txt

# Remove quickfix from requirements.txt
RUN sed '/quickfix/d' ${WORKING_DIR}/requirements.txt > ${WORKING_DIR}/requirements_docker.txt
RUN cat ${WORKING_DIR}/requirements_docker.txt
RUN pip install -U pip && pip install -r ${WORKING_DIR}/requirements_docker.txt
RUN rm ${WORKING_DIR}/requirements_docker.txt
ADD . ${WORKING_DIR}
