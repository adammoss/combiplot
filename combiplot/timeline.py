#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate short timeline videos based on C19 data for England

Dec 28 2020

@author: jah-photoshop
"""

import geopandas as gpd
import matplotlib.pyplot as plt,numpy as np
import os,ast,csv,random, math, pickle
from datetime import datetime, timedelta

from requests import get
from io import StringIO


print("________________________________________________________________________________")
print("Covid Timeline Video Plotter    -    version 1.0    -    @jah-photoshop Dec 2020")
print("________________________________________________________________________________")

debug=True
data_path = "data"
preset_path = "presets"

preset = "new"
deaths_colour='#FF0000'

#Parse a CSV file and read data lines into list
def read_file(filename, delim=','):
    data = []
    if(debug): print ("Opening file %s" % (filename))
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=delim)
        for row in csv_reader:
          data.append(row)
    if(debug): print(f'Processed {len(data)} lines.')
    return (data)


def get_data(url):
    print("Downloading data from URL " + url)
    response = get(url,timeout=10)
    if response.status_code >= 400:
        raise RuntimeError(f'Request failed: { response.text }')
    return response.text

def get_list_of_coords(ltla_id,sample_size):
    ind = oa_coord_ids.index(ltla_id)
    coord_i_list = oa_coords[ind]
    try:
        ret = random.sample(coord_i_list,sample_size)
    except ValueError:
        #print ("Error: %s %d %d" % (ltla_id,sample_size,len(coord_i_list)))
        return []
    return ret


def load_parameters(preset_name):
    global short_name,api_url,frames_per_day,frame_margins,filter_data,filter_list,plot_eng_ltla_boundaries,plot_wales_ltla_boundaries,plot_scot_ltla_boundaries,ltla_linewidth,ltla_colour,f_ltla_colour,cases_marker,cases_colour,cases_hist_window_size,cases_markersize,deaths_marker,deaths_hist_window_size,deaths_markersize,background_overlay,y_date,y_cases,y_deaths,x_text,resize,use_background,target_width,target_height,date_size,counter_size,log_filename,counter_start_date,output_path,use_overlay,plot_start_date,overlay_list,overlay_dates,c_size
    with open(preset_path+os.path.sep+preset_name+".pickle","rb") as f: preset_data=pickle.load(f)        
    short_name,api_url,frames_per_day,frame_margins,filter_data,filter_list,plot_eng_ltla_boundaries,plot_wales_ltla_boundaries,plot_scot_ltla_boundaries,ltla_linewidth,ltla_colour,f_ltla_colour,cases_marker,cases_colour,cases_hist_window_size,cases_markersize,deaths_marker,deaths_hist_window_size,deaths_markersize,background_overlay,y_date,y_cases,y_deaths,x_text,resize,use_background,target_width,target_height,date_size,counter_size,log_filename,counter_start_date,output_path,use_overlay,plot_start_date,overlay_list,overlay_dates,c_size = preset_data

load_parameters(preset)

overlay_tweets=False
tweets=[]
if(overlay_tweets):
        tweets=os.listdir('tweets/tweets/')
        tweets.sort()
        


print("________________________________________________________________________________")
print("LOADING DATA")
oa_xref_filename = data_path+os.path.sep+"ltla_coord_list.csv"

print("Loading OA coordinate map from " + oa_xref_filename)
oa_coordinate_file = read_file(oa_xref_filename,delim=';')
oa_coord_ids = [el[0] for el in oa_coordinate_file]
oa_coords = [ast.literal_eval(el[2]) for el in oa_coordinate_file]

ltla_filename = "zip://" + data_path+os.path.sep + "Local_Authority_Districts__May_2020__UK_BUC-shp.zip"
print("Loading LTLA map file from " + ltla_filename)
eng_ltla_map = gpd.read_file(ltla_filename,rows=314)
scot_ltla_map = gpd.read_file(ltla_filename,rows=slice(326,357))
wales_ltla_map = gpd.read_file(ltla_filename,rows=slice(357,379))

#Download LTLA case and death data
#Data API: https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeathsByDeathDate&format=csv
#data_string= get_data("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeathsByDeathDate&format=csv")
#data_string= get_data("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeathsByDeathDate&format=csv")
data_string= get_data(api_url)

local_data=[]
data_reader = csv.reader(StringIO(data_string), delimiter=',')
for line in data_reader:
    local_data.append(line)
 
start_date = datetime(2020, 12, 30)
end_date = datetime(2020,1,30)
area_codes = []
for line in local_data[1:]:
    if line[2] not in area_codes: area_codes.append(line[2])
    l_date = datetime.strptime(line[0],"%Y-%m-%d")    
    if l_date > end_date: end_date = l_date
    if l_date < start_date: start_date = l_date
area_codes.sort()
ltla_count = len(area_codes)


start_date_string = datetime.strftime(start_date,"%Y-%m-%d")
end_date_string = datetime.strftime(end_date,"%Y-%m-%d")

no_days = (end_date - start_date).days + 1
print ("Data covers %d LTLAs, %d days (from %s until %s)" % (ltla_count, no_days, start_date_string, end_date_string))

print ("Creating daily data")
case_dataset = []
death_dataset = []

for index,en in enumerate(area_codes):
    case_dataset.append([0 for day in range(no_days)])
    death_dataset.append([0 for day in range(no_days)])

for line in local_data[1:]:
    line_date = datetime.strptime(line[0],"%Y-%m-%d")
    day_index = (line_date - start_date).days
    ltla_index = area_codes.index(line[2])
    #print("%d %d %s" % (day_index,ltla_index,line))
    try:
        cases=int(line[4])
    except ValueError:
        cases=0
    try:
        deaths=int(line[5])
    except ValueError:
        deaths=0
    case_dataset[ltla_index][day_index]=cases
    death_dataset[ltla_index][day_index]=deaths

case_coordinates = []
death_coordinates = []
case_counts = []
death_counts = []
for day in range(no_days):
    cc = []
    dc = []
    for ind,area in enumerate(area_codes):
        if(area.startswith('E')): #Filter out welsh data for now...
            if(not filter_data or area in filter_list):                 
                cc.extend(get_list_of_coords(area,case_dataset[ind][day]))
                dc.extend(get_list_of_coords(area,death_dataset[ind][day]))
    random.shuffle(cc)
    random.shuffle(dc)
    case_coordinates.append(cc)
    death_coordinates.append(dc)
    case_counts.append(len(cc))
    death_counts.append(len(dc))

if(not os.path.isdir(output_path)): os.makedirs(output_path)

print("________________________________________________________________________________")


print("PRODUCING PLOTS")


cases_hist_window_index = 0
deaths_hist_window_index = 0
death_counter = 0
cases_counter = 0

g_factor = 10



cases_history = []
for i in range(cases_hist_window_size):
    cases_history.append([])
deaths_history = []
for i in range(deaths_hist_window_size):
    deaths_history.append([])

fig=plt.figure(figsize=(36,36),frameon=True)
plt.rcParams['font.family']='sans-serif'
plt.rcParams['font.sans-serif']='FLIPclockBlack'
day_offset = (plot_start_date - start_date).days
frame_count = 0
tweet_index = 0
tweet_step = 5 * frames_per_day
#tweet_step=1
new_tweet = None
old_tweet = None
old_y = 0
new_y = 0

for day in range (no_days - day_offset):
    day_index = day + day_offset
    date = start_date + timedelta(days=day_index)
    
    if use_overlay:
        for inx,bgd in enumerate(overlay_dates):
            if (date >= bgd): overlay = overlay_list[inx]
    
    datestring = datetime.strftime(date,"%b %d")
    fdatestring = datetime.strftime(date,"%Y%m%d")
    print("Producing plots for %s [Cases:%05d Deaths:%04d]" % (datetime.strftime(date,"%d %B %Y"),case_counts[day_index],death_counts[day_index]))
    #Use numpy array split to split the case + death lists by day 
    split_cases = np.array_split(case_coordinates[day_index],frames_per_day)
    split_deaths = np.array_split(death_coordinates[day_index],frames_per_day)
    random.shuffle(split_cases)
    random.shuffle(split_deaths)
    for frame in range (frames_per_day):
        frame_count += 1
        cases_array = split_cases[frame]
        deaths_array = split_deaths[frame]
        
        if(date >= counter_start_date):
            death_counter += len(deaths_array)
            cases_counter += len(cases_array)

        print("Producing subplot %d of %d [cases:%05d deaths:%04d]" % (frame+1,frames_per_day,len(cases_array),len(deaths_array)))
        f_string = "%s%sF-%s-%02d.png" % (output_path,os.path.sep,fdatestring,frame)
        print("Creating file %s" % (f_string))
        ax=plt.gca()
        ax.set_aspect('equal')
        ax.axis(frame_margins)
        plt.axis('off')
        z=0
        if(plot_wales_ltla_boundaries):
            wales_ltla_map.boundary.plot(ax=ax,zorder=z,linewidth=ltla_linewidth,color=f_ltla_colour)
            z+=1
        if(plot_scot_ltla_boundaries):
            scot_ltla_map.boundary.plot(ax=ax,zorder=z,linewidth=ltla_linewidth,color=f_ltla_colour)
            z+=1
        if(plot_eng_ltla_boundaries):
            eng_ltla_map.boundary.plot(ax=ax,zorder=z,linewidth=ltla_linewidth,color=ltla_colour)
            z+=1
             
        #Add new cases to rolling buffer and plot from the oldest to newest
        cases_history[cases_hist_window_index]=cases_array
        cases_hist_window_index += 1;
        if cases_hist_window_index == cases_hist_window_size: cases_hist_window_index=0
        deaths_history[deaths_hist_window_index]=deaths_array
        deaths_hist_window_index += 1;
        if deaths_hist_window_index == deaths_hist_window_size: deaths_hist_window_index=0
        #Plot historical cases and deaths from oldest to newest
        #Plot cases from oldest to newest - size increases with age
        for i in range(cases_hist_window_size-1):
            s_index = (i + cases_hist_window_index) % cases_hist_window_size
            h_fact = 1.0 - ((1.0 + i) / cases_hist_window_size)
            h_fact = math.sqrt(h_fact)
            alpha_v = 1.0 - h_fact
            m_size = cases_markersize * ((h_fact * g_factor) + 1)
            plt.scatter([el[0] for el in cases_history[s_index]],[el[1] for el in cases_history[s_index]],color=cases_colour,alpha=alpha_v,s=m_size,marker=cases_marker,lw=0,zorder=z)
            z+=1
            
        plt.scatter([el[0] for el in cases_array],[el[1] for el in cases_array],color=cases_colour,marker=cases_marker,s=cases_markersize,edgecolors='#669900',lw=1,zorder=z)
        #z+=1
        #Plot deaths from oldest to newest
        for i in range(deaths_hist_window_size-1):
            s_index = (i + deaths_hist_window_index) % deaths_hist_window_size
            h_fact = 1.0 - ((1.0 + i) / deaths_hist_window_size)
            h_fact = math.sqrt(h_fact)
            alpha_v = 1.0 - h_fact
            m_size = (0.5 + ((0.5 / deaths_hist_window_size) * (i+1)) ) * deaths_markersize
            plt.scatter([el[0] for el in deaths_history[s_index]],[el[1] for el in deaths_history[s_index]],alpha=alpha_v,color=deaths_colour,marker=deaths_marker,s=m_size,lw=0,zorder=z)
            z+=1
             
        plt.scatter([el[0] for el in deaths_array],[el[1] for el in deaths_array],color=deaths_colour,marker=deaths_marker,s=deaths_markersize,edgecolors='#440000',lw=2,zorder=z)
        z+=1
        c_str = "%d" % cases_counter
        while len(c_str)<(c_size + 2): c_str="-"+c_str
        d_str = "%d" % death_counter
        while len(d_str)<(c_size): d_str="-"+d_str
        plt.text(x_text,y_date,datestring,horizontalalignment='right',fontsize=date_size)
        plt.text(x_text,y_cases,c_str,horizontalalignment='right',fontsize=counter_size)
        plt.text(x_text,y_deaths,d_str,horizontalalignment='right',fontsize=counter_size)

        #Save figure
        plt.savefig(f_string, bbox_inches='tight')
        fig.clf()
        if(resize):os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
        if(use_background):os.system('composite %s %s %s' % (background_overlay, f_string,f_string))   
        if(use_overlay):os.system('composite %s %s %s' % (overlay, f_string,f_string))   
        if(overlay_tweets):
            tweet_step -= 1
            if(tweet_step == 0):
                #Load new tweet
                tweet_step = int(3.5 * frames_per_day)
                old_tweet = new_tweet
                old_y = new_y
                new_tweet = tweet_index
                tweet_index+=1
                new_y=random.randint(244,1000)
                while(abs(new_y - old_y) < 300):
                     new_y=random.randint(244,1000)

            gamma = (0.5 * tweet_step) / (frames_per_day * 3)
            igam = int(100 * gamma) + 15
            if(old_tweet is not None and old_tweet < len(tweets)):
                mf_line = "composite -dissolve %d -geometry +60+%d " % (igam,old_y)
                mf_line += 'tweets/tweets/'+ tweets[old_tweet] + ' ' + f_string + " -alpha Set " + f_string
                print(mf_line)
                os.system(mf_line)
            if(new_tweet is not None and new_tweet < len(tweets)):
                d_gam = 50 + igam
                if(d_gam > 100):d_gam=100
                mf_line = "composite -dissolve %d -geometry +60+%d " % (d_gam,new_y)
                mf_line += 'tweets/tweets/'+ tweets[new_tweet] + ' ' + f_string + " -alpha Set " + f_string
                print(mf_line)
                os.system(mf_line)

                
        #Update log file [for making soundtrack etc]
        with open(log_filename,"a") as file_object:
            file_object.write("%d,%s,%d,%d,%d\n" % (frame_count,fdatestring,frame,cases_counter,death_counter))
    print("________________________________________________________________________________")
print("Operation complete.")

