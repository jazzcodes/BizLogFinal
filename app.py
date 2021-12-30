import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import joblib
from database import DB

app = Flask(__name__)
my_db = DB()
model = joblib.load("predictor.pkl")

df = pd.DataFrame()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    global df

    input_features = [int(x) for x in request.form.values()]
    features_value = np.array(input_features)

    # validate input hours
    if input_features[0] < 0 or input_features[0] > 24:
        return render_template('bizpredict.html',
                               prediction_text='Please enter valid hours between 1 to 24 if you live on the Earth')

    output = model.predict([features_value])[0][0].round(2)

    # input and predicted value store in df then save in csv file
    df = pd.concat([df, pd.DataFrame({'Working Hours': input_features, 'Predicted Output': [output]})],
                   ignore_index=True)
    print(df)
    df.to_csv('smp_data_from_app.csv')

    return render_template('bizpredict.html',
                           prediction_text='You will get [{}%] profit, when you work for [{}] extra hours per day '.format(
                               output, int(features_value[0])))


@app.route("/query")
def query():
    return render_template("query.html")


@app.route("/query-save", methods=["POST"])
def query_save():
    query = {
        "name": request.form['name'],
        "phone": request.form['phone'],
        "subject": request.form['subject']
    }
    print(query)
    my_db.insert_operation(collection="queries", document=query)
    return render_template("Thanks.html")


@app.route("/bizpredict")
def bizpredict():
    return render_template("bizpredict.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
