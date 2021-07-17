import numpy as np
from keras.models import load_model
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, render_template, send_file, request
import base64
from io import BytesIO
import os


app = Flask(__name__)

@app.route('/')
def form():

    """Load the pre-saved model and data to test"""

    model = load_model('model_new.h5')
    #stock = yf.Ticker("BTC-USD")


    """Create training and test dataset. Training dataset is
    80% of the total data and the remaining 20% will be predicted,
    The model is already trained. We just need this 80% finishing line to
    set the prediction starting point"""

    #hist = stock.history(period="5y")
    #hist.tail(10)
    dataset=pd.read_csv('rolling_new.csv')
    d=30
    df=dataset.filter(['Consumption (Kwh)'])
    n=int(df.shape[0]*0.8)
    sc = MinMaxScaler(feature_range = (0, 1))

    dataset_train = df.iloc[:n, 0:1]
    dataset_train_scaled = sc.fit_transform(dataset_train)
    dataset_test = df.iloc[n:, 0:1]
    dataset_total = pd.concat((dataset_train, dataset_test), axis = 0)
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - d:].values


    """Scale and reshape the data"""

    inputs = inputs.reshape(-1,1)
    inputs = sc.transform(inputs)

    X_test = []
    for i in range(d, inputs.shape[0]):
        X_test.append(inputs[i-d:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))


    """Predict with the model on the test data"""

    predicted = model.predict(X_test)
    predicted = sc.inverse_transform(predicted)

    df['datetime']=df.index
    df=df.reset_index(drop=True)


    """Plot the actual and predicted data"""

    plt.plot(df.loc[n:, 'datetime'],dataset_test.values, color = 'red', label = 'Actual')
    plt.plot(df.loc[n:, 'datetime'],predicted, color = 'blue', label = 'Predicted')
    plt.title('Energy Consumption Prediction')
    plt.xlabel('Time')
    plt.ylabel('Consumption(KWh)')
    plt.legend()
    plt.xticks(rotation=90)

    CONSUMPTION = BytesIO()
    plt.savefig(CONSUMPTION, format="png")


    """Send the plot to plot.html"""

    CONSUMPTION.seek(0)
    plot_url = base64.b64encode(CONSUMPTION.getvalue()).decode('utf8')
    return render_template("plot.html", plot_url=plot_url)


if __name__ == "__main__":
    app.run(debug=True)