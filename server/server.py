# Import flask and datetime module for showing date and time
from collections import Counter
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify
import math
import pandas as pd
import statistics
import json
import matplotlib.pyplot as plt
plt.switch_backend('agg')

data = pd.read_excel('./Datasets/Dataset1.xlsx')
data2 = data.copy()
datatypes = {}

# print(data.describe(()))
fig = plt.figure(figsize=(10, 7))
# plt.boxplot(data['Age'])
# plt.savefig('../client/src/plots/boxPlot.png')

# delete unusable cols:
data2["BusinessTravel"] = data2["BusinessTravel"].replace(
    ["Non-Travel", "Travel_Rarely", "Travel_Frequently"], [int(0), int(1), int(2)])

data2["Gender"] = data2["Gender"].replace(["Male", "Female"], [1, 0])

data2["Attrition"] = data2["Attrition"].replace(["Yes", "No"], [1, 0])
data2["OverTime"] = data2["OverTime"].replace(["Yes", "No"], [1, 0])


for att in data2.columns:
    cell = data2[att][0]
    if isinstance(cell, str):
        del data2[att]


# print(data2.columns)
# coding data


# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/get_data', methods=['GET'])
def fetch_data():
    return data2.to_json(orient='records')


@app.route('/get_header', methods=['GET'])
def fetch_header():
    return jsonify({'header': data2.columns.to_list()})


@app.route('/get_stats/<attribute>', methods=['GET'])
def fetch_stats(attribute):

    list = [int(i) for i in data2[attribute].to_list()
            if not(math.isnan(i)) == True]
    list.sort()
    plot_name = createBoxPlot(list, attribute)
    return jsonify({'moyenne': getMoyenneOf(list),
                    'mode': mode(list),
                    'variance': variance(list),
                    'mediane': mediane(list),
                    'ecart_type': ecart_type(list),
                    'etendue': etendue(list),
                    'q1': getQ1(list),
                    'q3': getQ3(list),
                    'min': getMin(list),
                    'max': getMax(list),
                    'outliers': getOutliers(list),
                    "plot_name": plot_name
                    })


def getMoyenneOf(list):
    sum = 0
    for d in list:
        sum = sum + d
    return sum/len(data)


def mode(list):
    freqs = Counter(list)
    return [k for k, v in freqs.items() if v == freqs.most_common(1)[0][1]]


def variance(list):
    m = getMoyenneOf(list)
    list2 = [(val-m)**2 for val in list]
    return sum(list2)/len(list)


def mediane(list):
    n = len(list)
    index = n // 2
    if n % 2:
        return sorted(list)[index]
    return sum(sorted(list)[index - 1:index + 1]) / 2


def etendue(list):
    list = list.copy()
    list.sort()
    return list[len(list)-1]-list[0]


def ecart_type(list):
    return math.sqrt(variance(list))
    # return statistics.pstdev(list)


def getQ1(list):
    return list[len(list)//4]


def getQ3(list):
    return list[3*len(list)//4]


def getMin(list):
    return list[0]


def getMax(list):
    return list[len(list)-1]


def getIQR(list):
    return getQ3(list) - getQ1(list)


def getOutliers(list):
    iqr15 = 1.5 * getIQR(list)
    q1 = getQ1(list)
    q3 = getQ3(list)
    s = set()
    for val in list:
        if val > (q3+iqr15) or val < (q1-iqr15):
            s.add(val)
    return [v for v in s]


def createBoxPlot(list, attribute):
    plt.boxplot(list)
    plt.savefig(f'../client/src/plots/{attribute}.png')
    return f"{attribute}.png"


if __name__ == '__main__':
    app.run(debug=True)
