import os
import tensorflow as tf
from flask import Flask
from flask_restful import Resource, Api, reqparse
import joblib
from pandas import DataFrame
from helpers import series_to_supervised
from numpy import concatenate

app = Flask(__name__)
api = Api(app)

"""
Sample Data
        # data = {
        #     "close_price": [6350.0,
        #                     6356.48,
        #                     6361.93,
        #                     6368.78,
        #                     6456.0,
        #                     6365.43,
        #                     6327.94,
        #                     6326.98,
        #                     6339.5,
        #                     6333.05],
        #     "polarity": [0.10265670748614598,
        #                  0.09800395297609978,
        #                  0.0966881579841847,
        #                  0.10399680386738332,
        #                  0.09438312650721571,
        #                  0.10083589375817453,
        #                  0.1119643429977597,
        #                  0.1058881862567765,
        #                  0.10811700734669419,
        #                  0.10666706633974722]
        #
        #     ,
        #     "sensitivity": [0.21614845947129513,
        #                     0.21861239516350178,
        #                     0.23134226427071872,
        #                     0.21773906718462835,
        #                     0.19525553005949395,
        #                     0.22307632548845868,
        #                     0.19504306787217293,
        #                     0.20993930342403333,
        #                     0.20800324193424663,
        #                     0.21723050559221563]
        #
        #     ,
        #     "tweet_vol": [4354.0,
        #                   4432.0,
        #                   3980.0,
        #                   3830.0,
        #                   3998.0,
        #                   12435.0,
        #                   3843.0,
        #                   3831.0,
        #                   3743.0,
        #                   3480.0]
        #
        #     ,
        #     "volume_btc": [986.73, 126.46, 259.1, 81.54, 124.55, 141.5, 141.3, 162.37, 58.62, 74.75]
        # }           
"""

parser = reqparse.RequestParser()
parser.add_argument('close_price', type=int, action='append', required=True)
parser.add_argument('polarity', type=int, action='append', required=True)
parser.add_argument('sensitivity', type=int, action='append', required=True)
parser.add_argument('tweet_vol', type=int, action='append', required=True)
parser.add_argument('volume_btc', type=int, action='append', required=True)

class PricePredictorView(Resource):
    """
    This view will eventually integrate the model.
    For now it sends sample json data 
    """

    def post(self):
        args = parser.parse_args()
        data = dict(args)
        df = DataFrame(data)
        model = tf.keras.models.load_model('./bitcoin_lstm_prediction_model.h5')
        scaler = joblib.load('./scalar_data.joblib')
        scaled = scaler.transform(df.values)
        reframed = series_to_supervised(scaled, 4, 2)
        input_data = reframed.values
        input_data.shape = (1, input_data.shape[0], input_data.shape[1])
        prediction = model.predict(input_data[:, 1:, :5])
        prediction_for_inv_transform = concatenate(
            (prediction, reframed[:1][["var2(t+1)", "var3(t+1)", "var4(t+1)", "var5(t+1)"]]), axis=1)
        inv_transform = scaler.inverse_transform(prediction_for_inv_transform)[0]
        return {
            "close_price": inv_transform[0],
            "polarity": inv_transform[1],
            "sensitivity": inv_transform[2],
            "tweet_vol": inv_transform[3],
            "volume_btc": inv_transform[4]
        }


api.add_resource(PricePredictorView, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000", debug=True)
