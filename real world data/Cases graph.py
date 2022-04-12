import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


data = pd.read_excel ("daycases.xlsx")

date = pd.DataFrame(data, columns= ['date'])
cases = pd.DataFrame(data, columns= ['newCasesBySpecimenDate'])

fig = plt.figure()

plt.title("Daily Cases in the UK")
plt.xlabel("Date")
plt.ylabel("Cases")

plt.gcf().autofmt_xdate()

plt.plot(date, cases)
plt.savefig("Plot of daily Covid-19 cases in the UK")