#FROM python:3.8-rc-alpine
FROM tensorflow/tensorflow
COPY ./requirements.txt /requirements.txt
COPY ./bitcoin_lstm_prediction_model.h5 /bitcoin_lstm_prediction_model.h5
COPY ./scalar_data.joblib /scalar_data.joblib
COPY ./index.py /index.py
COPY ./helpers.py /helpers.py
RUN pip install -r requirements.txt