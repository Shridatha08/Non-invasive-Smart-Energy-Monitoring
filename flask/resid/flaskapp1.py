from flask import Flask, render_template, send_file, request
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import os
import math
import tensorflow as tf
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import pandas as pd
from array import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import *
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from keras.models import load_model
import warnings
warnings.filterwarnings("ignore")
#from keras.models import load_weights

app = Flask(__name__)

"""The default page will route to the form.html page where user can input
necessary variables for machine learning"""

@app.route('/')
def index():
    return render_template('form.html')

""" Once the data is keyed in by the user and the submit button is pressed,
the user will have to wait for the training of the model depending on the
epoch number. Once trained, the model will show the predicted output of this
time series data."""


@app.route('/data', methods=['POST'])
def hello():

    """Get the input names from form.html"""

    Epochs = request.form['Epochs']
    d = request.form['Days']

    Epochs = int(Epochs)
    d = int(d)


    """Parse historical data from CSV"""

    df = pd.read_csv('daily_updated.csv')

    #model = load_model('win_model.h5')

    df=df.set_index('Date')

    """Create training and test dataset. Training dataset is
    80% of the total data and the remaining 20% will be predicted"""

    data=df.filter(['Consumption (Kwh)'])
    dataset=data.values
    n=math.ceil(len(dataset)*0.8)


    """Scale and reshape the data"""

    sc = MinMaxScaler(feature_range = (0, 1))
    scaled_data=sc.fit_transform(dataset)

    train_data=scaled_data[0:n,:]
    x_train = []
    y_train = []
    for i in range(d, len(train_data)):
        x_train.append(train_data[i-d:i, 0])
        y_train.append(train_data[i, 0])

    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))


    test_data=scaled_data[n-d:,:]
    x_test=[]
    y_test=dataset[n:,:]
    for i in range(d,len(test_data)):
        x_test.append(test_data[i-d:i,0])

    x_test=np.array(x_test)
    x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

    """ LSTM Model"""
    model=Sequential()
    model.add(LSTM(60,return_sequences=True,input_shape=(x_train.shape[1],1))) 
    model.add(LSTM(60))
    model.add(Dropout(0.2))
    tf.keras.layers.Dense(10, activation="relu")
    model.add(Dense(1))

    optimizer = tf.keras.optimizers.SGD(lr=5e-2, momentum=0.9)
    model.compile(loss=tf.keras.losses.Huber(), optimizer=optimizer, metrics=["mae"])
    history = model.fit(x_train,y_train,batch_size=64,epochs=Epochs,verbose=1)  




    """Predict with the model on the test data"""

    predictions=model.predict(x_test)
    predictions=sc.inverse_transform(predictions)
    #df=df.reset_index(drop=True)


    """Plot the actual and predicted data"""

    train=data[:n]
    valid=data[n:]
    valid['Predictions']=predictions

    plt.figure(figsize=(12,8))
    plt.title("Daily Consumption Model")
    plt.xlabel('Date',fontsize=18)
    plt.ylabel('Consumption(KWh)',fontsize=18)
    plt.plot(train['Consumption (Kwh)'])
    plt.plot(valid[['Consumption (Kwh)','Predictions']])
    plt.legend(["Train","Val","Predictions"],loc='upper right')
    plt.xticks(rotation=35)
    plt.xticks(np.arange(0,1400,60))

    
    Consumption= BytesIO()
    plt.savefig(Consumption, format="png", bbox_inches="tight")


    #Predict for next days (ahead)
    last_n_days=data[-n:].values
    last_n_days_scaled=sc.transform(last_n_days)

    X_test=[]
    X_test.append(last_n_days_scaled)
    X_test=np.array(X_test)
    X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

    pred_consumption=model.predict(X_test)
    pred_consumption=sc.inverse_transform(pred_consumption)
    op=float(pred_consumption)
    output=round(op,2)

    errors=abs(predictions-y_test)
    mape=100*np.mean(errors/y_test)
    accuracy= 100-mape

    """Send the plot to plot.html"""

    Consumption.seek(0)
    plot_url = base64.b64encode(Consumption.getvalue()).decode('utf8')
    return render_template("plot.html", plot_url=plot_url,prediction_text='Forecast for tomorrow is {} KWh'.format(output),accuracy_of_model='Model Accuracy is {:0.2f}%'.format(accuracy))


if __name__ == "__main__":
    app.run(debug=True)