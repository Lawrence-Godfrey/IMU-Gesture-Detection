#!/usr/bin/env python3
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
from sklearn.neural_network import MLPClassifier
import pandas as pd
import numpy as np
from scipy import signal

num_samples = 150

with open('classifier.model', 'rb') as classifier: 
    clf = pickle.load(classifier)

print("Model Loaded")

def centre(plot):
    return (np.sum([np.abs(m)*i for m, i in zip(plot, range(len(plot)))])/np.sum(np.abs(plot)))

def centreplot(plot):
    return np.roll(plot, int(len(plot)/2 - centre(plot))) 

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def allData(x, i):
    all_data = []
    for key, value in x.items():
        value = value[num_samples*(i) : num_samples*(i) + num_samples]
        data_filtered = butter_highpass_filter(value, 0.1, 100)
        value = np.roll(value, int(len(value)/2 - centre(data_filtered)))
        value = [float(k)/max(abs(value)) for k in value]
        all_data = [*all_data, *value]

    return all_data

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        f = open("temp.csv", "w")
        f.write("\"GX\",\"GY\",\"GZ\",\"AX\",\"AY\",\"AZ\",\"MX\",\"MY\",\"MZ\"\n")
        f.write(post_data.decode('utf-8'))
        f.close()

        samples = pd.read_csv('temp.csv', sep=',')

        prediction = clf.predict([allData(samples, 0)])[0]
        print("That was a Wave!" if prediction==0 else "That was a Punch!")
        
        os.remove("temp.csv")

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
