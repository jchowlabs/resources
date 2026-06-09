from flask import Flask, render_template, request
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

# Store data for training the model
shoe_data = {'sizes': [], 'prices': []}
trained_model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enter_data', methods=['POST'])
def enter_data():
    size = float(request.form['size'])
    price = float(request.form['price'])

    shoe_data['sizes'].append(size)
    shoe_data['prices'].append(price)

    return render_template('index.html', shoe_data=shoe_data)

@app.route('/train_model', methods=['POST'])
def train_model():
    global trained_model
    X = np.array(shoe_data['sizes']).reshape(-1, 1)
    y = np.array(shoe_data['prices'])

    model = LinearRegression()
    model.fit(X, y)
    trained_model = model

    return render_template('index.html', shoe_data=shoe_data, model_trained=True)

@app.route('/predict_price', methods=['POST'])
def predict_price():
    size_to_predict = float(request.form['size_to_predict'])

    if trained_model is None:
        return render_template('index.html', shoe_data=shoe_data, model_trained=False, prediction=None)

    predicted_price = trained_model.predict([[size_to_predict]])[0]

    return render_template('index.html', shoe_data=shoe_data, model_trained=True, prediction=predicted_price)

if __name__ == '__main__':
    app.run(debug=True)
