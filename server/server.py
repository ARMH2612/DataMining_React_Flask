# Import flask and datetime module for showing date and time
import pandas as pd
import statistics
import json
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

data = pd.read_excel('./Datasets/Dataset1.xlsx')


# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/get_data', methods=['GET'])
def fetch_data():
    return data.to_json(orient='records')


@app.route('/get_header', methods=['GET'])
def fetch_header():
    return jsonify({'header': data.columns.to_list()})


@app.route('/get_stats/<attribute>', methods=['GET'])
def fetch_stats(attribute):
    return jsonify({'moyenne': getMoyenneOf(attribute), 'mode': mode(attribute), 'variance': variance(attribute), 'mediane': mediane(attribute), 'ecart_type': ecart_type(attribute)})


def getMoyenneOf(attribute):
    sum = 0
    for d in data[attribute]:
        sum = sum + d
    return sum/len(data)


def mode(attribute):
    return statistics.mode(data[attribute])


def variance(attribute):
    return statistics.variance(data[attribute])


def mediane(attribute):
    return statistics.median(data[attribute])


def etendue(attribute):
    pass


def ecart_type(attribute):
    return statistics.pstdev(data[attribute])


if __name__ == '__main__':
    app.run(debug=True)
