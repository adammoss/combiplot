#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate short timeline videos based on C19 data for England

Dec 28 2020

@author: jah-photoshop
"""

import geopandas as gpd
import matplotlib.pyplot as plt,numpy as np
import os,ast,csv,random, math
from datetime import datetime, timedelta

from requests import get
from io import StringIO


print("________________________________________________________________________________")
print("Covid Timeline Video Plotter    -    version 1.0    -    @jah-photoshop Dec 2020")
print("________________________________________________________________________________")

debug=True

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
    

data_path = "data"

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
data_string= get_data("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeaths28DaysByDeathDate&format=csv")

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
            cc.extend(get_list_of_coords(area,case_dataset[ind][day]))
            dc.extend(get_list_of_coords(area,death_dataset[ind][day]))
    random.shuffle(cc)
    random.shuffle(dc)
    case_coordinates.append(cc)
    death_coordinates.append(dc)
    case_counts.append(len(cc))
    death_counts.append(len(dc))
print("________________________________________________________________________________")


print("PRODUCING PLOTS")


#Original set
frames_per_day = 6
frame_margins = [133000,658000,10600,655000]
plot_eng_ltla_boundaries = True
plot_wales_ltla_boundaries = True
plot_scot_ltla_boundaries = True
ltla_linewidth = 2.0
ltla_colour='#888888'
f_ltla_colour='#CCCCCC'
cases_marker='.'
cases_colour = '#00CC00'
cases_hist_window_size = frames_per_day * 7
cases_hist_window_index = 0
cases_markersize =120
deaths_marker='X'
deaths_colour = '#EE0000'
deaths_hist_window_size = frames_per_day * 3
deaths_hist_window_index = 0
deaths_markersize=360
background_overlay = "background.png"
background_overlay = "cumulative.png"
y_date = 600000
y_cases = 516000
y_deaths = 450000
resize=True
use_background=True
target_width = 1080 
target_height = 1324
death_counter = 0
cases_counter = 0
date_size = 150
counter_size = 100
log_filename="framelog.csv"
counter_start_date = datetime(2020,1,1)
output_path = "output"
use_overlay = False
plot_start_date = datetime(2020,1,11) 


#
#
##Test set
#frames_per_day = 8
#frame_margins = [133000,658000,10600,712022]
#plot_eng_ltla_boundaries = True
#plot_wales_ltla_boundaries = True
#plot_scot_ltla_boundaries = True
#ltla_linewidth = 3.0
#ltla_colour='#888888'
#f_ltla_colour='#DDDDDD'
#cases_marker='.'
#cases_colour = '#00CC00'
#cases_hist_window_size = frames_per_day * 7
#cases_hist_window_index = 0
#cases_markersize = 160
#deaths_marker='X'
#deaths_colour = '#EE0000'
#deaths_hist_window_size = frames_per_day * 5
#deaths_hist_window_index = 0
#deaths_markersize=480
#background_overlay = "tabloid-bg.png"
#y_date = 620000
#y_cases = 538000
#y_deaths = 465000
#resize=True
#use_background=True
#target_width = 1080 
#target_height = 1440
#death_counter = 0
#cases_counter = 0
#date_size = 148
#counter_size = 116
#log_filename="tframelog.csv"
#counter_start_date = datetime(2020,9,1)
#output_path = "output_tab"
#plot_start_date = datetime(2020,2,1) 
#use_overlay = True
#overlay = 'backgrounds/bg01.png'
#



bg_list = ['backgrounds/bg01.png','backgrounds/bg02.png','backgrounds/bg03.png','backgrounds/bg04.png','backgrounds/bg05.png','backgrounds/bg06.png','backgrounds/bg07.png','backgrounds/bg08.png',
           'backgrounds/bg09.png','backgrounds/bg10.png','backgrounds/bg11.png','backgrounds/bg10.png','backgrounds/bg12.png','backgrounds/bg13.png','backgrounds/bg14.png','backgrounds/bg15.png','backgrounds/bg16.png','backgrounds/bg17.png','backgrounds/bg18.png']
#19 backgrounds[10 is repeated]
bg_dates = [datetime(2020,9,1),datetime(2020,9,18),datetime(2020,9,25),datetime(2020,9,29),
            datetime(2020,10,4),datetime(2020,10,7),datetime(2020,10,9),datetime(2020,10,11),
            datetime(2020,10,13),datetime(2020,10,15),datetime(2020,10,16),datetime(2020,10,28),           
            datetime(2020,10,29),datetime(2020,11,10),datetime(2020,11,11),datetime(2020,11,23),
            datetime(2020,11,24),datetime(2020,12,9),datetime(2020,12,10)            
            ]



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
for day in range (no_days - day_offset):
    day_index = day + day_offset
    date = start_date + timedelta(days=day_index)
    
    if use_overlay:
        for inx,bgd in enumerate(bg_dates):
            if (date >= bgd): overlay = bg_list[inx]
    
    datestring = datetime.strftime(date,"%b %d")
    fdatestring = datetime.strftime(date,"%Y%m%d")
    print("Producing plots for %s [Cases:%05d Deaths:%04d]" % (datetime.strftime(date,"%d %B %Y"),case_counts[day_index],death_counts[day_index]))
    #Use numpy array split to split the case + death lists by day 
    split_cases = np.array_split(case_coordinates[day_index],frames_per_day)
    split_deaths = np.array_split(death_coordinates[day_index],frames_per_day)
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
            m_size = cases_markersize * ((h_fact * 8) + 1)
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
        while len(c_str)<7: c_str="-"+c_str
        d_str = "%d" % death_counter
        while len(d_str)<5: d_str="-"+d_str
        plt.text(648000,y_date,datestring,horizontalalignment='right',fontsize=date_size)
        plt.text(648000,y_cases,c_str,horizontalalignment='right',fontsize=counter_size)
        plt.text(648000,y_deaths,d_str,horizontalalignment='right',fontsize=counter_size)

        #Save figure
        plt.savefig(f_string, bbox_inches='tight')
        fig.clf()
        if(resize):os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
        if(use_background):os.system('composite %s %s %s' % (background_overlay, f_string,f_string))   
        if(use_overlay):os.system('composite %s %s %s' % (overlay, f_string,f_string))   

        #Update log file [for making soundtrack etc]
        with open(log_filename,"a") as file_object:
            file_object.write("%d,%s,%d,%d,%d\n" % (frame_count,fdatestring,frame,cases_counter,death_counter))
#        #divider = make_axes_locatable(ax)
#        #cax = divider.append_axes("bottom",size="5%",pad=0.1)
#        if(plot_laa_names or plot_laa_values):
#            #laa_centroids.plot(ax=ax,zorder=6,color='#33CC44')
#            for name in target_places:
#                count=laa_names.index(name)
#                val=laa_rates[count][day]
#                kx = laa_centroids[count][0]
#                ky = laa_centroids[count][1]
#                if kx > frame_margins[0] and kx < frame_margins[1] and ky > frame_margins[2] and ky < frame_margins[3]:                
#                    #Plot labels text centered unless within 10% of RHS or LHS margin
#                    al_mode = 'center'
#                    if kx > ( (frame_margins[1] - frame_margins[0]) * 0.95) + frame_margins[0]: al_mode = 'right'
#                    if kx < ( (frame_margins[1] - frame_margins[0]) * 0.05) + frame_margins[0]: al_mode = 'left'
#                    y_shift = 0
#                    if ky > ( (frame_margins[3] - frame_margins[2]) * 0.95) + frame_margins[2]: y_shift = -2 * (y_step * laa_fontsize)
#                    if ky < ( (frame_margins[3] - frame_margins[2]) * 0.05) + frame_margins[2]: y_shift = 2 * (y_step * laa_fontsize)
#                    yy_shift = 0
#                    if plot_laa_names: 
#                        yy_shift = y_step * laa_fontsize
#                        plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift+yy_shift,name,horizontalalignment=al_mode,fontsize=laa_fontsize*0.6,bbox=dict(boxstyle='square',color='#AAAA8855'))
#                    if plot_laa_values: plt.text(laa_centroids[count][0],laa_centroids[count][1]+y_shift-yy_shift,"%3.1f" % val,horizontalalignment=al_mode,fontsize=laa_fontsize) #bbox=dict(boxstyle='square',color='#FFFFEE11')
#        if add_date: plt.text(label_x,label_y,c_date.strftime("%B %d"), horizontalalignment=text_align_mode, style='italic',fontsize=date_font_size)
#        if add_title:plt.text(title_x,title_y,title_string,horizontalalignment=text_align_mode,fontsize=title_font_size)
#        if add_footer:    
#            footer = file_date.strftime(footer_message + " Data set published %d/%m/%y. github.com/jah-photoshop/autocovid")
#            fr_scale = f_scale
#            if(plot_laa_values): 
#                footer = "Values are cases/100K/week. "+footer
#                fr_scale = f_scale * 1.2
#            plt.text(frame_margins[1]-( (frame_margins[1] - frame_margins[0]) * 0.01),frame_margins[2]+( (frame_margins[3] - frame_margins[2]) * 0.01),footer,horizontalalignment='right',fontsize=title_font_size / fr_scale, bbox=dict(boxstyle='square',color='#AAAA8844'))
#        plt.savefig(f_string, bbox_inches='tight')
#        if post_process:
#            if resize_output: os.system('convert %s -resize %dx%d\! %s' % (f_string,target_width,target_height,f_string))
#            if add_background: os.system('composite %s %s %s' % (f_string,background_file,f_string))
#            if add_overlay: 
#                for count, of in enumerate(overlay_filenames):
#                    if of[-1]==os.path.sep: of+=c_date.strftime("map-%Y%m%d.png")
#                    print(of)
#                    if overlay_positions[count] == [0,0]: os.system('composite %s %s %s' % (of, f_string,f_string))                    
#                    else: os.system('composite %s -geometry +%d+%d %s %s' % (of, overlay_positions[count][0],overlay_positions[count][1],f_string,f_string))
#        fig.clf()   
#        #Copy file to googledrive
#        if(archive):
#            if not os.path.exists(archive_path + short_name): os.makedirs(archive_path+short_name)
#            shutil.copyfile(f_string,archive_path + short_name + os.path.sep + c_date.strftime("map-%Y%m%d.png"))
    print("________________________________________________________________________________")
print("Operation complete.")

