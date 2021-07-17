# Predictive-non-invasive-Energy-Management

Smart home devices and its applications have a great upside potential in successfully cutting
down the electricity consumption across households. This study focuses on the realisation of
the potential that the application provides. As an initial process, the current consumption is
measured and stored in a database with the help of PHP via the ESP32 microcontroller. The
AWS cloud services is used for the users to view consumption in real-time. Data acquired is
utilised by the server to run LSTM Neural Networks to predict the possible future usage. This
predicted future value is compared with the actual consumption to test the accuracy of the
model.

<h2><p style="text-align:center;">Algorithm</p></h2>

* Interfacing CT-013 Current sensor with ESP32, connected to a Access Point.
* Reading I<sub>rms</sub> values from sensor and calculating Power consumed in KWh.
* Pushing data to the AWS EC2 instance every 10 minutes and MCU goes to sleep mode.
* Setting up Apache, MySQL and phpmyadmin in EC2 instance for data acquisition.
* Creating table in MySQL to store incoming values with timestamp.
* Php Script to send data from database to webpage.
* Javascript and HTML5 based webpage for real-time consumption Visualization.
* Retrieving the collected data from MySQL table in the CSV format for forecasting.\
  *Since the data acquired was quite less for model. Electrcity Consumption dataset from kaggle was used.*\
  <https://www.kaggle.com/uciml/electric-power-consumption-data-set>
* Exploratory Data Analysis and pre-processing to prepare dataset for input to the forecasting model.\
      i. From the dataset Total consumption is computed and the values were converted from Wh to KWh.\
      ii. The original dataset's frequency of *15min* was converted to *daily* frequency to reduce the irregularity.
* Dividing the dataset into test (20%) and train (80%). 
* LSTM architecture implementation
* Hyper parameter tuning to improvise the LSTM.
* Saving the model's weight as a **H5** file.
* Flask Web-API for deep learning model deployment to provide interactive chart based forecast for the end-user. 
 
![]()



