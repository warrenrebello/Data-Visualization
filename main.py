from time_series import TimeSeries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)

data = TimeSeries()

@app.route("/")
def mainPage():
    data.getTimeSeries()
    new_data = data.stateData()
    length = len(new_data)
    
    return render_template("index.html", states=new_data, length=length)


@app.route("/state_data/<state>")
def stateInfo(state):
    state_name = state
    state_data = data.stateData()
    length = len(state_data)
    file_name = state_name + ".png"
    # file_path = "ITVedant/Assignments/01 - Python/Week 10/Data Visualization/static/"
    file_path = "static/"
    try:
        os.remove(file_path + file_name)
    except:
        pass

    for n in range(0,length):
        if state_data['state'][n+1] == state_name:

            plt.figure(figsize=(20,10))
            # plt.title(state_data.iloc[n].iloc[3])
            plt.pie(state_data.iloc[n].iloc[0:3], labels=state_data.iloc[n].index[0:3], wedgeprops=dict(width=0.4), startangle=0)
            plt.savefig(file_path + file_name)            

            return render_template("state.html", file_name=file_name, state_name=state_name)
        else:
            pass


if __name__ == "__main__":
    app.run(debug=True)
