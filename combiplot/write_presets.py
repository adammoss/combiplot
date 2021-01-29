#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_presets.py

Generate preset (.pickle) files 

Created on Wed Oct  7 13:55:28 2020

"""
import os, pickle, numpy as np
from datetime import datetime
preset_folder = "presets"
background_file = ""

if(not os.path.isdir(preset_folder)): os.makedirs(preset_folder)


def write_pickle():
    d_list=[short_name,api_url,frames_per_day,frame_margins,filter_data,filter_list,plot_eng_ltla_boundaries,plot_wales_ltla_boundaries,plot_scot_ltla_boundaries,ltla_linewidth,ltla_colour,f_ltla_colour,cases_marker,
            cases_colour,cases_hist_window_size,cases_markersize,deaths_marker,deaths_hist_window_size,deaths_markersize,background_overlay,y_date,y_cases,y_deaths,x_text,resize,use_background,target_width,target_height,
            date_size,counter_size,log_filename,counter_start_date,output_path,use_overlay,plot_start_date,overlay_list,overlay_dates,c_size]
    with open(preset_folder+os.path.sep+short_name+".pickle","wb") as f: pickle.dump(d_list,f)        


#Original set
short_name="original"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 6
frame_margins = [133000,658000,10600,655000]
filter_data = False
filter_list = []
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 2.0
ltla_colour='#888888'
f_ltla_colour='#CCCCCC'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 7
cases_markersize =120
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 3
deaths_markersize=360
background_overlay = "background.png"
y_date = 600000
y_cases = 516000
y_deaths = 450000
x_text = 648000
resize=True
use_background=True
target_width = 1080 
target_height = 1324
date_size = 150
counter_size = 100
log_filename="framelog.csv"
counter_start_date = datetime(2020,1,1)
output_path = "output"
use_overlay = False
plot_start_date = datetime(2020,1,11) 
overlay_list = []
overlay_dates = []
c_size = 5 #Counter size [n width for deaths, n+2 for cases]
write_pickle()

#Original set
short_name="new"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 6
frame_margins = [133000,658000,10600,655000]
filter_data = False
filter_list = []
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 2.0
ltla_colour='#888888'
f_ltla_colour='#CCCCCC'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 1
cases_markersize =100
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 3
deaths_markersize=1200
background_overlay = "background.png"
y_date = 600000
y_cases = 516000
y_deaths = 450000
x_text = 648000
resize=True
use_background=True
target_width = 1080 
target_height = 1324
date_size = 150
counter_size = 100
log_filename="newout.csv"
counter_start_date = datetime(2020,9,1)
output_path = "newout"
use_overlay = False
plot_start_date = datetime(2020,9,1) 
overlay_list = []
overlay_dates = []
c_size = 5 #Counter size [n width for deaths, n+2 for cases]
write_pickle()

#Tabloid set
short_name="tabloid"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 8
frame_margins = [133000,658000,10600,712022]
filter_data = False
filter_list = []
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 3.0
ltla_colour='#888888'
f_ltla_colour='#DDDDDD'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 7
cases_markersize = 160
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 5
deaths_markersize=480
background_overlay = "tabloid-bg.png"
y_date = 620000
y_cases = 538000
y_deaths = 465000
x_text = 648000
resize=True
use_background=True
target_width = 1080 
target_height = 1440
date_size = 148
counter_size = 116
log_filename="tframelog.csv"
counter_start_date = datetime(2020,9,1)
output_path = "output_tab"
plot_start_date = datetime(2020,9,1) 
use_overlay = True
overlay_list = ['backgrounds/bg01.png','backgrounds/bg02.png','backgrounds/bg03.png','backgrounds/bg04.png','backgrounds/bg05.png','backgrounds/bg06.png','backgrounds/bg07.png','backgrounds/bg08.png',
           'backgrounds/bg09.png','backgrounds/bg10.png','backgrounds/bg11.png','backgrounds/bg10.png','backgrounds/bg12.png','backgrounds/bg13.png','backgrounds/bg14.png','backgrounds/bg15.png','backgrounds/bg16.png','backgrounds/bg17.png','backgrounds/bg18.png']
#19 backgrounds[10 is repeated]
overlay_dates = [datetime(2020,9,1),datetime(2020,9,18),datetime(2020,9,25),datetime(2020,9,29),
            datetime(2020,10,4),datetime(2020,10,7),datetime(2020,10,9),datetime(2020,10,11),
            datetime(2020,10,13),datetime(2020,10,15),datetime(2020,10,16),datetime(2020,10,28),           
            datetime(2020,10,29),datetime(2020,11,10),datetime(2020,11,11),datetime(2020,11,23),
            datetime(2020,11,24),datetime(2020,12,9),datetime(2020,12,10)            
            ]
c_size = 5
write_pickle()



#MegaTabloid set
short_name="megatabloid"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 18
frame_margins = [133000,658000,10600,712022]
filter_data = False
filter_list = []
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 3.0
ltla_colour='#888888'
f_ltla_colour='#DDDDDD'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 2
cases_markersize = 100
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 3
deaths_markersize=1500
background_overlay = "tabloid-bg.png"
y_date = 620000
y_cases = 538000
y_deaths = 465000
x_text = 648000
resize=True
use_background=True
target_width = 1080 
target_height = 1440
date_size = 148
counter_size = 116
log_filename="mega_tabframelog.csv"
counter_start_date = datetime(2020,9,1)
output_path = "mega_tab"
plot_start_date = datetime(2020,9,1) 
use_overlay = True
overlay_list = ['backgrounds/bg01.png','backgrounds/bg02.png','backgrounds/bg03.png','backgrounds/bg04.png','backgrounds/bg05.png','backgrounds/bg06.png','backgrounds/bg07.png','backgrounds/bg08.png',
           'backgrounds/bg09.png','backgrounds/bg10.png','backgrounds/bg11.png','backgrounds/bg10.png','backgrounds/bg12.png','backgrounds/bg13.png','backgrounds/bg14.png','backgrounds/bg15.png','backgrounds/bg16.png','backgrounds/bg17.png','backgrounds/bg18.png']
#19 backgrounds[10 is repeated]
overlay_dates = [datetime(2020,9,1),datetime(2020,9,24),datetime(2020,10,2),datetime(2020,10,7),
            datetime(2020,10,13),datetime(2020,10,17),datetime(2020,10,20),datetime(2020,10,23),
            datetime(2020,10,26),datetime(2020,10,29),datetime(2020,10,31),datetime(2020,11,13),           
            datetime(2020,11,15),datetime(2020,11,29),datetime(2020,12,1),datetime(2020,12,15),
            datetime(2020,12,17),datetime(2020,12,29),datetime(2021,1,1)            
            ]
c_size = 5
write_pickle()


#GIF Set
short_name="gif"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 1
frame_margins = [133000,658000,10600,712022]
filter_data = False
filter_list = []
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 4.0
ltla_colour='#888888'
f_ltla_colour='#DDDDDD'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 2
cases_markersize = 200
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 8
deaths_markersize=1000
background_overlay = "gifversion.png"
y_date = 620000
y_cases = 538000
y_deaths = 465000
x_text = 648000
resize=True
use_background=True
target_width = 1080 
target_height = 1440
death_counter = 0
cases_counter = 0
date_size = 148
counter_size = 116
log_filename="tframelog.csv"
counter_start_date = datetime(2020,9,1)
output_path = "output"
plot_start_date = datetime(2020,9,1) 
use_overlay = True
overlay_list = ['backgrounds/bg01.png','backgrounds/bg02.png','backgrounds/bg03.png','backgrounds/bg04.png','backgrounds/bg05.png','backgrounds/bg06.png','backgrounds/bg07.png','backgrounds/bg08.png',
           'backgrounds/bg09.png','backgrounds/bg10.png','backgrounds/bg11.png','backgrounds/bg10.png','backgrounds/bg12.png','backgrounds/bg13.png','backgrounds/bg14.png','backgrounds/bg15.png','backgrounds/bg16.png','backgrounds/bg17.png','backgrounds/bg18.png']
#19 backgrounds[10 is repeated]
overlay_dates = [datetime(2020,9,1),datetime(2020,9,18),datetime(2020,9,25),datetime(2020,9,29),
            datetime(2020,10,4),datetime(2020,10,7),datetime(2020,10,9),datetime(2020,10,11),
            datetime(2020,10,13),datetime(2020,10,15),datetime(2020,10,16),datetime(2020,10,28),           
            datetime(2020,10,29),datetime(2020,11,10),datetime(2020,11,11),datetime(2020,11,23),
            datetime(2020,11,24),datetime(2020,12,9),datetime(2020,12,10)            
            ]
c_size = 5
write_pickle()


#North Yorkshire
short_name="northyorkshire"
api_url="https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv"
frames_per_day = 8
frame_margins = [360000,520000,412000,520000]
#Ryedale=E07000167 
#Craven=E07000163 
#Harrogate=E07000165 
#Hambleton=E07000164 
#Richmondshire=E07000166 
#Selby=E07000169 
#Scarborough=E07000168
filter_data = True
filter_list = ['E07000163','E07000164','E07000165','E07000166','E07000167','E07000168','E07000169','E06000014']
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = False
plot_scot_ltla_boundaries = False
ltla_linewidth = 4.0
ltla_colour='#888888'
f_ltla_colour='#DDDDDD'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = int(frames_per_day * 1.5)
cases_markersize = 800
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 12
deaths_markersize=1800
background_overlay = "ny-bg2.png"
y_date = 515000
y_cases = 503500
y_deaths = 492500
x_text = 519000
resize=True
use_background=True
target_width = 1596
target_height = 1080
death_counter = 0
cases_counter = 0
date_size = 110
counter_size = 86
log_filename="nyorks_log.csv"
counter_start_date = datetime(2020,9,1)
output_path = "nyorks"
plot_start_date = datetime(2020,9,1) 
use_overlay = False
overlay_list = []
overlay_dates = []
c_size = 3
write_pickle()


