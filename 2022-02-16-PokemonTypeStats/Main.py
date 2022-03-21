import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("Data/Gen6+Chart.csv")
size = [i*50 for i in data["value"]]
data.plot(x="attack",y="defend",kind="scatter",s=size)
plt.show()
