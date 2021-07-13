from statistics import stdev
from tkinter import Canvas
from datetime import datetime,timedelta

def plot(graphcanvas: Canvas,plotlist:list,**optional):
    graphcanvas.update()
    graphcanvas.grid_forget()
    graphcanvas.delete('all')
    p_w = graphcanvas.winfo_width()
    p_h = graphcanvas.winfo_height()
    padding = 100
    p_area_w = p_w - padding
    p_area_h = p_h - padding
    if len(plotlist) > 1:
        scaled_price = min_max_scale(0,p_area_h,plotlist)
        x_scale = p_area_w/len(scaled_price) 
        #plot prices graph
        for i in range(len(scaled_price)-1):
            graphcanvas.create_line(
                i*x_scale + padding/2, # x0
                p_area_h - scaled_price[i] + padding/2, #y0 
                (i+1)*x_scale + padding/2, #x1
                p_area_h - scaled_price[i+1] + padding/2, #y1
                fill = 'cyan2',
                width = 3)
            r = 4
            graphcanvas.create_oval(
                i*x_scale + padding/2 - r,
                p_area_h - scaled_price[i] + padding/2 - r,
                i*x_scale + padding/2 + r,
                p_area_h - scaled_price[i] + padding/2 + r,
                fill = 'light cyan',
                # dash=(1, 1) 
            )
        
        #plot date and date lines
        for i in range(len(scaled_price)-1,-1,-int(len(scaled_price)/(p_area_w/180))):
            i_time = datetime.now() - timedelta(hours = (len(scaled_price)-1) - i, minutes=0)
            # print(i_time)
            graphcanvas.create_text(
                i*x_scale + padding/2,
                p_area_h + padding/2 + 15,
                text = str(i_time)[0:13]+":00",
                fill = "spring green",
                anchor = 'n'
            )
            i_time = i_time 
            # print(x_scale)
            # if (i+1)%(len(scaled_price)/5) == 0:
            graphcanvas.create_line(
                i*x_scale + padding/2,
                padding/2,
                i*x_scale + padding/2,
                p_area_h + padding/2,
                fill = 'gray',
                dash=(1, 1) 
            )
        #plot max and min
        graphcanvas.create_text(
                padding/2-5,
                padding/2, 
                text = round(max(plotlist),6),
                fill = 'spring green',
                anchor = 'e'
                )
        graphcanvas.create_line(
                padding/2,
                padding/2,
                (len(scaled_price)-1)*x_scale + padding/2,
                padding/2,
                fill = 'cyan',
                dash=(1, 1)
            )

        graphcanvas.create_text(
                padding/2-5,
                p_area_h + padding/2, 
                text = round(min(plotlist),6),
                fill = 'spring green',
                anchor = 'e'
                )
        graphcanvas.create_line(
                padding/2,
                p_area_h + padding/2,
                (len(scaled_price)-1)*x_scale + padding/2,
                p_area_h + padding/2,
                fill = 'cyan',
                dash=(1, 1)
            )
        #plot mean line and mean value + bands
        if optional.get('parameters') != [0,0,0]:
            max_number = max(plotlist)
            min_number = min(plotlist)
            prices = optional.get('prices')
            N_of_days = int(optional.get('parameters')[0])
            mean = sum(prices[-N_of_days:])/N_of_days
            std = stdev(prices[-N_of_days:])
            U_band = mean + optional.get('parameters')[1]*std
            L_band = mean - optional.get('parameters')[2]*std 
            
            scaled_mean = scale_number(mean,max_number,min_number,p_area_h,0)
            #mean
            # print(optional.get('parameters'))
            graphcanvas.create_line(
                    padding/2,
                    p_area_h - scaled_mean + padding/2,
                    (len(scaled_price)-1)*x_scale + padding/2,
                    p_area_h - scaled_mean + padding/2,
                    fill = 'cyan',
                    dash=(1, 1)
                )
        
            graphcanvas.create_text(
                    padding/2-5,
                    p_area_h - scaled_mean + padding/2,
                    text = round(mean,4),
                    fill = "spring green",
                    anchor = 'e'
                )
            #Upper 
            if U_band > max_number:
                scaled_U_band = p_area_h+10
            else:
                scaled_U_band = scale_number(U_band,max_number,min_number,p_area_h,0) 
            
            if L_band < min_number:
                scaled_L_band = 0-10
            else:
                scaled_L_band = scale_number(L_band,max_number,min_number,p_area_h,0) 
            
            graphcanvas.create_line(
                padding/2,
                p_area_h - scaled_U_band + padding/2,
                (len(scaled_price)-1)*x_scale + padding/2,
                p_area_h - scaled_U_band + padding/2,
                fill = 'white'
            )
            graphcanvas.create_text(
                ((len(scaled_price)-1)*x_scale)/2 + padding/2,
                p_area_h - scaled_U_band + padding/2 - 10,
                text = round(U_band,4),
                fill = 'white',
                anchor = 'e'
            )
            #Lower band
            graphcanvas.create_line(
                padding/2,
                p_area_h - scaled_L_band + padding/2,
                (len(scaled_price)-1)*x_scale + padding/2,
                p_area_h - scaled_L_band + padding/2,
                fill = 'white'
            )
            graphcanvas.create_text(
                ((len(scaled_price)-1)*x_scale)/2 + padding/2,
                p_area_h - scaled_L_band + padding/2 - 10,
                text = round(L_band,4),
                fill = 'white',
                anchor = 'e'
            )
        
        #plot current price
        graphcanvas.create_text(
                (len(scaled_price)-1)*x_scale + padding/2+5,
                p_area_h - scaled_price[-1] + padding/2, 
                text = round(plotlist[-1],6),
                fill = 'spring green',
                anchor = 'w'
                )
        #plot open position
        if optional.get('position') is not None:
            if optional['position'] > max(plotlist):
                position_y = p_area_h
            elif optional['position'] < min(plotlist):
                position_y = 0
            else:
                position_y = (((optional['position']-min(plotlist))/(max(plotlist)-min(plotlist)))*p_area_h)
            
            position_x = (len(scaled_price)-1)*x_scale + padding/2 
            graphcanvas.create_text(
                position_x + 10,
                p_area_h - position_y + padding/2,
                text = optional['position'],
                fill = 'tomato',
                anchor = 'w',
                )
            graphcanvas.create_line(
                padding/2,
                p_area_h - position_y + padding/2,
                position_x,
                p_area_h - position_y + padding/2,
                fill = 'tomato',
                dash=(1, 1)
            )
    graphcanvas.grid(row = 2, rowspan = 2, column = 1, sticky = "nsew")

def min_max_scale(min_value,max_value,data):
        result = []
        min_p = min(data)
        max_p = max(data)
        for i in range(len(data)):
            result.append(((data[i] - min_p)/(max_p-min_p))*(max_value-min_value)) 
        return result

def scale_number(data,max_p,min_p,max_value,min_value):
    return ((data - min_p)/(max_p-min_p))*(max_value-min_value)
           
