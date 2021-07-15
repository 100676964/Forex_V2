import numpy as np
from statistics import mean,stdev
# def get_closing_prices(rates:np.array):

def get_action(rates:np.array, avaliable_funs, current_pl):
    x = 20
    y = 1.5
    z = 1.5
    current_rate = rates[-1]
    moving_average = mean(rates[-x:])
    H_band = stdev(rates[-x:])*y + moving_average
    L_band = stdev(rates[-x:])*z + moving_average

    history_average = mean(rates)
    pass