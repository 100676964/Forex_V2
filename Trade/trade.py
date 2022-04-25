from tkinter.constants import N
import numpy as np
import math
from statistics import mean,stdev
LEVERAGE = 10
# def get_closing_prices(rates:np.array):
def get_actions(name_list,rates_list,NAV,avaliable_margin,positions):
    buy_candidates = []
    buy_list = []
    sell_list = []
    for i in range(len(name_list)):
        result = __get_individual_result(rates_list[i])
        if result[0] == 'sell' and len(positions) > 0:
            for position in positions:
                if position[0] == name_list[i]:
                    sell_list.append([name_list[i],int(position[1])*-1])
                    break
        if result[0] == 'buy':
            if len(positions) > 0:
                if name_list[i] in positions[:,0]:
                    pass
                else:
                    buy_candidates.append([name_list[i],result[1],rates_list[i][-1]])
            else:
                buy_candidates.append([name_list[i],result[1],rates_list[i][-1]])
    
    
    if len(buy_candidates) > 0 and len(positions) < 3:
        for i in range(1,len(buy_candidates)):
            for j in range(len(buy_candidates)):
                if buy_candidates[j][1] < buy_candidates[i][1]:
                    temp = buy_candidates[j]
                    buy_candidates[j] = buy_candidates[i]
                    buy_candidates[i] = temp

        for i in range(3 - len(positions)):
            if i < len(buy_candidates):
                buy_list.append([buy_candidates[i][0],(min(math.floor(NAV*0.31),avaliable_margin*0.95)*LEVERAGE)])
             
    return np.array(buy_list),np.array(sell_list)



def __get_individual_result(rates):
    m_average,H_band,L_band = calculate_bands(rates,number_of_days=20,H_multiplier=1.5,L_multiplier=1.5)
    current_rate = rates[-1]
    if current_rate > L_band and current_rate < H_band:
        return ['hold',-1,m_average,H_band,L_band]
    elif current_rate >= H_band:
        return ['sell',(current_rate - H_band)/(H_band-m_average),m_average,H_band,L_band]
    elif current_rate <= L_band:
        return ['buy',(L_band - current_rate)/(m_average-L_band),m_average,H_band,L_band]

def calculate_bands(rates,number_of_days=20,H_multiplier=1.5,L_multiplier=1.5):
    x = number_of_days
    y = H_multiplier
    z = L_multiplier
    
    moving_average = mean(rates[-x:])
    H_band = stdev(rates[-x:])*y + moving_average
    L_band = moving_average - stdev(rates[-x:])*z
    
    return moving_average,H_band,L_band