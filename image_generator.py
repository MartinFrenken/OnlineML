import threading
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from sklearn.linear_model import LinearRegression

class BuyIndicator:
    def __init__(self, date, bought, holding):
        self.date = date
        self.bought = bought
        self.holding = holding

print("block")
action_date=1
bought = True
sold = False
holding = False
speed = 5
initial_credit = 1000
stock_amount =0
trades_done = 0
BuyIndicators = []
desc =""
def emit_update():
    initial_row =7300
    timespan = 1000
    delta = 200
    buy_and_hold(init_row=initial_row,end_row=initial_row+timespan)
    while initial_row<initial_row+timespan:
        final_row = initial_row+delta
        time.sleep(0.1)
        plot_stock(end_row=final_row,init_row=initial_row)
        predict_stock(end_row=final_row,init_row=initial_row)
        initial_row+=speed
        print("update")


def plot_stock(init_row,end_row):
    msft = pd.read_csv(r"C:\Users\win 10\rpggame\AAPL.csv", sep=',')
    msft = msft[['date', 'open']]
    msft = msft.rename(columns={"open": "Apple's Stock Value"});
    msft.set_index('date', inplace=True)
    msft.index = pd.to_datetime(msft.index)
    msft = msft.iloc[init_row:end_row]
    ax = msft.plot(title="Predictions of Apples stocks")
    for x in BuyIndicators:
        if(x.bought == True and x.holding == False):
            ax.axvline(x.date,color= "green",linestyle='dashed')
        if(x.bought == False and x.holding == False):
            ax.axvline(x.date, color="red",linestyle='dashed')


    ax.set_ylabel("Apples's stock value")
    ax.set_xlabel(desc)
    fig = ax.get_figure()
    fig.savefig("static/output.png")
    plt.close(fig)

def predict_stock(init_row,end_row):
    msft = pd.read_csv(r"C:\Users\win 10\rpggame\AAPL.csv", sep=',')
    msft = msft[['date', 'open']]
    msft = msft.rename(columns={"open": "Microsofts's Stock Value"});
    model = LinearRegression()
    msft['date'] = pd.to_datetime(msft['date'])
    msft['date_delta'] = (msft['date'] - msft['date'].min()) / np.timedelta64(1, 'D')
    origin_msft=msft
    msft = msft.iloc[end_row-speed:end_row]
    x = msft['date_delta']
    y = msft['Microsofts\'s Stock Value']
    x= x.values
    x = x.reshape(-1,1)
    results= model.fit(x,y)
    results= model.score(x, y)
    pdct = origin_msft.iloc[end_row+speed]['date_delta']
    pdct = [pdct]
    pdct = np.asarray(pdct)
    pdct=pdct.reshape(1,-1)
    predicted_value= model.predict(pdct)
    base_value = origin_msft.iloc[end_row]['Microsofts\'s Stock Value']
    global bought
    global sold
    global holding
    global trades_done
    global stock_amount
    global initial_credit
    global desc
    if(predicted_value>base_value):

        if(bought == False):
            print("bought stocks!")
            bought=True
            holding =False
            sold=False;
            trades_done = trades_done + 1
            stock_amount = initial_credit/base_value
            initial_credit =initial_credit % base_value
        else:
            holding=True

    else:
        bought=False
        if(sold==False):
            print("sold stocks!!")
            sold =True
            holding = False
            trades_done=trades_done+1
            initial_credit =initial_credit+ stock_amount*base_value
            stock_amount = 0
        else:
            holding =True
    global action_date
    action_date =origin_msft.iloc[end_row]['date']
    desc ="Spending capacity ($): ",round(initial_credit)," Stocks: ",round(stock_amount)," Amount of trades: ",trades_done
    print(desc)
    BuyIndicators.append(BuyIndicator(action_date,bought,holding))

def buy_and_hold(init_row,end_row):
    msft = pd.read_csv(r"C:\Users\win 10\rpggame\AAPL.csv", sep=',')
    msft = msft[['date', 'open']]
    msft = msft.rename(columns={"open": "Microsofts's Stock Value"});
    msft['date'] = pd.to_datetime(msft['date'])
    origin_msft = msft
    initial_bh_value = msft.iloc[init_row]['Microsofts\'s Stock Value']
    final_bh_value = msft.iloc[end_row]['Microsofts\'s Stock Value']

    init_bh_stock_amount =1000/initial_bh_value
    init_bh_credit = 1000%initial_bh_value

    end_bh_credit= init_bh_stock_amount*final_bh_value + init_bh_credit
    print(end_bh_credit)
emit_update()

