## IMU Gesture detection with a Neural Network
### Using an XinaBox CW01 (ESP8266) and XinaBox SI01 (LMS9DS1 9 DoF IMU)

This Project uses the [CW01](https://xinabox.cc/collections/core/products/cw01) and [SI01](https://xinabox.cc/collections/sensors/products/si01) to collect a total of 1350 samples from the IMU in 1.5 seconds (split between the Magnetometor, Accelerometer, and Gyroscope)
This data is then sent via a POST request to a server which is run with `predict.py`, which reads in the data and makes a prediction using `classifier.model`,
which is a pre-trained neural network which can be downloaded [here](https://www.mediafire.com/file/tdck3th4ebmcaed/classifier.model/file) (131MB)

If you want to train the model to recognize different gestures, use getData to get the POST request and read the data to a csv, you can then use `TrainGestures.ipynb` to train the data. 

#### Files
 * `SendData/SendData.ino`
    * Reads and sends the 1350 samples to the server   
 * `getData.py`
    * Runs a server and appends the contents of the POST request to a csv
 * `predict.py`
    * Runs a server and makes a prediction based on `classifier.model`
 * `TrainGestures.ipynb`
    * Use to plot data from the csv, train and save the neural network model
 * `classifier.model`
    * The saved trained neural network 
    * Download [here](https://www.mediafire.com/file/tdck3th4ebmcaed/classifier.model/file) (131MB)

#### Libraries 
 - #### Arduino
   - ESP8266WiFi.h
   - ESP8266HTTPClient.h
   - [xCore.h]()
   - [xSI01.h]()
 - #### Python
   - http.server
   - pickle
   - pandas
   - numpy
   - scipy 
   - logging
   - matplotlib
   - seaborn
   - sklearn
