# -*- coding: utf-8 -*-
"""
Created on Mon May 10 02:27:07 2021

@author: Admin
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


data = pd.read_excel ("deaths.xlsx")

date = pd.DataFrame(data, columns= ['date'])
cases = pd.DataFrame(data, columns= ['newDeaths28DaysByDeathDate'])

fig = plt.figure()

plt.title("Daily Deaths in the UK")
plt.xlabel("Date")
plt.ylabel("Deaths")

plt.gcf().autofmt_xdate()

plt.plot(date, cases)
plt.savefig("Plot of daily Covid-19 deaths in the UK")