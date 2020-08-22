import requests
import json

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


class TimeSeries():

    def __init__(self):
        pass

    def getData(self):
        data = requests.get("https://api.covid19india.org/data.json")
        data_text = data.text
        data_json = json.loads(data_text)
        return data_json
    

    def dailyData(self, days=20):

        data_json = self.getData()

        daily_time = pd.DataFrame(data_json['cases_time_series'])

        daily_time.dailyconfirmed = daily_time.dailyconfirmed.astype('int32')
        daily_time.dailydeceased = daily_time.dailydeceased.astype('int32')
        daily_time.dailyrecovered = daily_time.dailyrecovered.astype('int32')

        dc = daily_time['dailyconfirmed'].tail(days)
        dd = daily_time['dailydeceased'].tail(days)
        dr = daily_time['dailyrecovered'].tail(days)

        x = daily_time.date.tail(days)

        return x, dc, dd, dr


    def totalData(self, days=20):

        data_json = self.getData()

        total_time = pd.DataFrame(data_json['cases_time_series'])

        total_time.totalconfirmed = total_time.totalconfirmed.astype('int32')
        total_time.totaldeceased = total_time.totaldeceased.astype('int32')
        total_time.totalrecovered = total_time.totalrecovered.astype('int32')

        tc = total_time['totalconfirmed'].tail(days)
        td = total_time['totaldeceased'].tail(days)
        tr = total_time['totalrecovered'].tail(days)

        return tc, td, tr


    def getTimeSeries(self, days=20):

        x, dc, dd, dr = self.dailyData()
        tc, td, tr = self.totalData()
        
        fig, (daily, total) = plt.subplots(2, figsize=(20,10))

        daily.plot(x,dc, linewidth=1, marker='o')
        daily.plot(x,dd, linewidth=1, linestyle='--', marker='o')
        daily.plot(x,dr, linewidth=1, linestyle='-.', marker='o')

        total.plot(x,tc, linewidth=1, marker='o')
        total.plot(x,td, linewidth=1, linestyle='--', marker='o')
        total.plot(x,tr, linewidth=1, linestyle='-.', marker='o')

        plt.setp(daily.get_xticklabels() + total.get_xticklabels(), rotation=45)

        daily.legend(labels=["Confirmed","Deaths","Recovered"])
        total.legend(labels=["Confirmed","Deaths","Recovered"])

        # file_path = "ITVedant/Assignments/01 - Python/Week 10/Data Visualization/static/"
        file_path = "static/"
        
        plt.savefig(file_path + "covid.png")
    

    def stateData(self):
        data_json = self.getData()
        data_state = pd.DataFrame(data_json['statewise'])

        data_state = data_state.drop(0)

        data_state.active = data_state.active.astype('int32')
        data_state.confirmed = data_state.confirmed.astype('int32')
        data_state.deaths = data_state.deaths.astype('int32')
        data_state.recovered = data_state.recovered.astype('int32')

        data_state.rename(columns={"active":"Active", "confirmed":"Confirmed", "deaths":"Deaths"}, inplace=True)
        col = ['Active', 'Confirmed', 'Deaths', 'state']
        new_data = pd.DataFrame(data_state, columns=col)

        return new_data
