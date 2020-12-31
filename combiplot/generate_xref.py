#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate short timeline videos based on C19 data for England

Dec 28 2020

@author: jah-photoshop
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import os, csv
from requests import get
from io import StringIO

print("________________________________________________________________________________")
print("Generate OA cross references    -    version 1.0    -    @jah-photoshop Dec 2020")
print("________________________________________________________________________________")

debug = True

#Parse a CSV file and read data lines into list
def read_file(filename):
    data = []
    if(debug): print ("Opening file %s" % (filename))
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
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


data_path = "data"

print("________________________________________________________________________________")
print("LOADING MAP DATA")
oa_map_filename = "zip://" + data_path + os.path.sep + "Output_Areas__December_2011__Population_Weighted_Centroids-shp.zip"
xref_sheet_filename = data_path + os.path.sep + "Output_Area_to_Ward_to_Local_Authority_District_(December_2019)_Lookup_in_England_and_Wales.csv"

print("Loading output area map data from " + oa_map_filename)
oa = gpd.read_file(oa_map_filename)
map_oa_names = oa.OA11CD.tolist()
map_oa_geos = oa.geometry.tolist()
map_oa_x = [el.x for el in map_oa_geos]
map_oa_y = [el.y for el in map_oa_geos]

print("Loading cross reference spreadsheet from " + xref_sheet_filename)
xr = read_file(xref_sheet_filename)

oa_xr_ids = [el[1] for el in xr]
la_xr_ids = [el[4] for el in xr]

#Data API: https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeathsByDeathDate&format=csv
data_string= get_data("https://api.coronavirus.data.gov.uk/v2/data?areaType=ltla&metric=newCasesBySpecimenDate&metric=newDeathsByDeathDate&format=csv")
local_data=[]
data_reader = csv.reader(StringIO(data_string), delimiter=',')
for line in data_reader:
    local_data.append(line)
    
print("Creating list of LTLA areas")
ltla_ids=[]
for el in local_data[1:]:
    if el[2] not in ltla_ids: 
        ltla_ids.append(el[2])
ltla_ids.sort()

#Create blank list of lists for ltla_oa xrefs
no_ltla = len(ltla_ids)
ltla_oa_list = []
ltla_oa_coords = []
for i in range(no_ltla):
    ltla_oa_list.append([])
    ltla_oa_coords.append([])
    
print("Cross-referencing OAs to LTLAs")
for index,el in enumerate(la_xr_ids):
    if el in ltla_ids:
        ix = ltla_ids.index(el)
        ltla_oa_list[ix].append(oa_xr_ids[index])
        
print("Cross-referencing centroids to OAs")
for index, oal in enumerate(ltla_oa_list):
    print("Processing LTLA %03d of %03d" % (index+1,no_ltla),end='\r')
    for el in oal:
        if el in map_oa_names:
            el_index = map_oa_names.index(el)
            ltla_oa_coords[index].append([map_oa_x[el_index],map_oa_y[el_index]])
    
output_filename = data_path+os.path.sep+"ltla_coord_list.csv"
with open(output_filename,'w') as f:
    for ind,el in enumerate(ltla_oa_coords):
        f.write("%s;%d;%s\n" % (ltla_ids[ind],len(el),el))
#england=gpd.read_file(map_filename,rows=6791)
"""
https://geoportal.statistics.gov.uk/datasets/output-areas-december-2011-population-weighted-centroids-1
https://opendata.arcgis.com/datasets/b0c86eaafc5a4f339eb36785628da904_0.zip?outSR=%7B%22latestWkid%22%3A27700%2C%22wkid%22%3A27700%7D

"""

