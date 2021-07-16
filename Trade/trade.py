import numpy as np
from statistics import mean,stdev
# def get_closing_prices(rates:np.array):

def get_action(rates:np.array, avaliable_funs, current_pl):
    

    
    pass
def __calculate_score(rates,current_pl,number_of_days,H_multiplier,L_multiplier):
    x = number_of_days
    y = H_multiplier
    z = L_multiplier
    
    
    current_rate = rates[-1]
    moving_average = mean(rates[-x:])
    H_band = stdev(rates[-x:])*y + moving_average
    L_band = stdev(rates[-x:])*z + moving_average
    
    history_average = mean(rates)
    pass