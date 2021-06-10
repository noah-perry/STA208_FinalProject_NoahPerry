# -*- coding: utf-8 -*-
"""
Created on Mon May 10 22:40:23 2021

@author: noahj
"""

import numpy as np
import os
import pandas as pd

##### Import and Clean Data #####
# Read in files for selected cryptos and merge
os.chdir("C:/Users/noahj/Documents/UCD/2021 Spring Classes/STA 208/Project/STA208_FinalProject_NoahPerry/Data")

selected_files = ["ADAUSD_1440.csv", "ETHUSD_1440.csv", "XBTUSD_1440.csv", "XMRUSD_1440.csv"]
selected_cryptos = ["ADA", "ETH", "XBT", "XMR"]

counter = 0
for f in selected_files:
    crypto = selected_cryptos[counter]
    
    temp = pd.read_csv(f, names=['time_sec','open','high','low','close','volume','trades'])
    temp['time'] = pd.to_datetime(temp['time_sec'], unit="s", origin=pd.Timestamp("1970-01-01"))
    temp = temp[['time','close','volume','trades']]
    temp = temp.rename(columns = {'close':('pr_' + crypto), 'volume':('vol_' + crypto), 'trades':('tr_' + crypto)})
    
    if counter == 0:
        main = temp
    else:
        main = pd.merge(main, temp, how = "outer", on = "time")
    counter = counter + 1

del(counter)
del(crypto)
del(f)
del(temp)

main = main.sort_values(by = 'time', ascending = True)
main = main.reset_index(drop = True)

# Check start dates and missing values in each time series
pr_vars = ["pr_" + c for c in selected_cryptos]
for i in np.arange(0, len(selected_cryptos),1):
    p = pr_vars[i]
    temp_index1 = main[p].first_valid_index()
    temp_index2 = main[p].last_valid_index()
    print(selected_cryptos[i])
    print("start date:", main["time"][temp_index1])
    print("end date:", main["time"][temp_index2])
    print("------")

del(p)
del(pr_vars)
del(temp_index1)
del(temp_index2)


# Fill missing values after series starts using last observation carried forward
main = main.fillna(method = "ffill")

# Calculate log difference
for p in ["pr_" + c for c in selected_cryptos]:
    for i in [1,7,14]:
        if i == 1:
            main[p.replace("pr", "logdif")] = np.log(main[p] / main[p].shift(i))
        else:
            main[p.replace("pr", "logdif" + str(i))] = np.log(main[p] / main[p].shift(i))
            
del(p)

# save main dataset
main.to_pickle("main.pkl")

