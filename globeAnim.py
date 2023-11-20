# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 17:25:33 2023

@author: Johannes H. Uhl, European Commission Joint Research Centre, Ispra, Italy.
"""

### GlobeAnim - a Python script to animate global raster datasets on a rotating globe
### Parameters: 
###   intif: a geotiff file of global coverage
###   datadir: folder for temp and output data

import matplotlib.pyplot as plt
import os,sys
import subprocess
import numpy as np
from PIL import Image,ImageOps
import imageio
from osgeo import gdal

# Examples: ###########################
# Ex. 1) RGB image (NASA's blue marble image)
# Ex. 2) Categorical raster dataset (Climate zones)
# Ex. 3) Contiuous raster dataset (Gridded population data)
#######################################

# 1st example: NASA's blue marble RGB image #########################################################################        
# Data source: https://visibleearth.nasa.gov/search?q=geotiff
intif = 'land_shallow_topo_8192_georef.tif'
datadir='./outputs'
output_gif=datadir+os.sep+os.path.split(intif)[-1].replace('.tif','.gif')
frame_duration = 0.15 #seconds per frame
lat_center=0
lons=np.arange(-180,180.01,5)
currfiles_warped=[] 
for i,lon_center in enumerate(lons):
    lat_center=lat_center#lats[i]
    proj_str = '+proj=ortho +lon_0=%s +lat_0=%s' %(lon_center,lat_center)
    outtif = datadir+os.sep+'warped_ortho_%s_%s.tif' %(np.round(lon_center,2),np.round(lat_center,2))
    if os.path.exists(outtif):
        os.remove(outtif)
    cmd = 'gdalwarp -t_srs "%s" -tr 25000 25000 %s %s' %(proj_str,intif,outtif) #k=1
    subprocess.run(cmd)
    if os.path.exists(outtif):
        currfiles_warped.append(outtif)
    print('warped %s to orthographic' %intif,lon_center,lat_center)
currfiles_rendered=[] 
for i,imfile in enumerate(currfiles_warped):
    im = ImageOps.expand(Image.open(imfile),border=50,fill='black')
    fig,ax=plt.subplots(figsize=(7,7))
    ax.imshow(im)
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    currfile_rendered = datadir+os.sep+'gif_input_%s.png' %i
    fig.savefig(currfile_rendered,bbox_inches='tight', pad_inches = 0,dpi=150)
    plt.show() 
    plt.clf() 
    currfiles_rendered.append(currfile_rendered) 
with imageio.get_writer(output_gif, mode='I',duration=frame_duration) as writer:
    for filename in currfiles_rendered:
        if os.path.exists(filename):
            image = imageio.imread(filename)
            writer.append_data(image)
# Remove temporary files
for filename in set(currfiles_warped):
    if os.path.exists(filename):
        os.remove(filename)      
for filename in set(currfiles_rendered):
    if os.path.exists(filename):
        os.remove(filename)  
        
#########################################################################   
# 2nd example: Koeppen-Geiger climate zones (categorical raster dataset)
# Data source: https://figshare.com/articles/dataset/Present_and_future_K_ppen-Geiger_climate_classification_maps_at_1-km_resolution/6396959/2    
intif='Beck_KG_V1_present_0p5.tif'
datadir='./outputs'
output_gif=datadir+os.sep+os.path.split(intif)[-1].replace('.tif','.gif')
frame_duration = 0.15 #seconds per frame
lat_center=0
lons=np.arange(-180,180.01,5)
currfiles_warped=[] 
for i,lon_center in enumerate(lons):
    lat_center=lat_center#lats[i]
    proj_str = '+proj=ortho +lon_0=%s +lat_0=%s' %(lon_center,lat_center)
    outtif = datadir+os.sep+'warped_ortho_%s_%s.tif' %(np.round(lon_center,2),np.round(lat_center,2))
    if os.path.exists(outtif):
        os.remove(outtif)
    cmd = 'gdalwarp -t_srs "%s" -tr 25000 25000 %s %s' %(proj_str,intif,outtif) #k=1
    subprocess.run(cmd)
    if os.path.exists(outtif):
        currfiles_warped.append(outtif)
    print('warped %s to orthographic' %intif,lon_center,lat_center)

def white_to_transparency(img):
    x = np.asarray(img.convert('RGBA')).copy()
    x[:, :, 3] = (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)
    return Image.fromarray(x)

currfiles_rendered=[] 
for i,imfile in enumerate(currfiles_warped):       
    currlon=float(imfile.split('_')[-2])
    if currlon<0:
        otherlon=currlon+180 
    else:
        otherlon=currlon-180             
    img2 = imfile.replace(str(np.round(currlon,2)),str(np.round(otherlon,2)))               
    im = ImageOps.expand(Image.open(imfile),border=25,fill='white')
    im2 = ImageOps.mirror(ImageOps.expand(Image.open(img2),border=25,fill='white')) 
    im2g = ImageOps.grayscale(im2)         
    im2g_arr = np.array(im2g)
    im2g_arr[im2g_arr<255]=220
    im2g = Image.fromarray(im2g_arr.astype('uint8'))        
    im2gt  = white_to_transparency(im2g)
    imt  = white_to_transparency(im)
    fig,ax=plt.subplots(figsize=(7,7))
    ax.imshow(imt,zorder=2)         
    ax.imshow(im2gt,zorder=1)  
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    currfile_rendered = datadir+os.sep+'gif_input_%s.png' %i
    fig.savefig(currfile_rendered,bbox_inches='tight', pad_inches = 0,dpi=150)
    plt.show() 
    plt.clf() 
    currfiles_rendered.append(currfile_rendered) 
with imageio.get_writer(output_gif, mode='I',duration=frame_duration) as writer:
    for filename in currfiles_rendered:
        if os.path.exists(filename):
            image = imageio.imread(filename)
            writer.append_data(image)
# Remove temporary files
for filename in set(currfiles_warped):
    if os.path.exists(filename):
        os.remove(filename)      
for filename in set(currfiles_rendered):
    if os.path.exists(filename):
        os.remove(filename)     

#########################################################################
# 3rd example: Global Human Settlement Layer, gridded population data (continuous raster dataset)        
# Source: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.zip
intif='GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.tif' 
datadir='./outputs'
output_gif=datadir+os.sep+os.path.split(intif)[-1].replace('.tif','.gif')
frame_duration = 0.15 #seconds per frame
lat_center=0
lons=np.arange(-180,180.01,5)
currfiles_warped=[] 
for i,lon_center in enumerate(lons):
    lat_center=lat_center#lats[i]
    proj_str = '+proj=ortho +lon_0=%s +lat_0=%s' %(lon_center,lat_center)
    outtif = datadir+os.sep+'warped_ortho_%s_%s.tif' %(np.round(lon_center,2),np.round(lat_center,2))
    if os.path.exists(outtif):
        os.remove(outtif)
    cmd = 'gdalwarp -t_srs "%s" -tr 25000 25000 -r sum %s %s' %(proj_str,intif,outtif) #k=1
    subprocess.run(cmd)
    if os.path.exists(outtif):
        currfiles_warped.append(outtif)
    print('warped %s to orthographic' %intif,lon_center,lat_center)
currfiles_rendered=[] 
for i,imfile in enumerate(currfiles_warped):       
    currlon=float(imfile.split('_')[-2])
    if currlon<0:
        otherlon=currlon+180 
    else:
        otherlon=currlon-180             
    imfile2 = imfile.replace(str(np.round(currlon,2)),str(np.round(otherlon,2)))               
    im_arr=np.pad(gdal.Open(imfile).ReadAsArray(),25)
    im_arr2=np.pad(gdal.Open(imfile2).ReadAsArray(),25)
    im_arr2=np.fliplr(im_arr2)
    im_arr[np.isin(im_arr,np.max(im_arr,axis=1))]=0 #remove stripe at datum border
    im_arr2[np.isin(im_arr2,np.max(im_arr2,axis=1))]=0 #remove stripe at datum border   
    im_arr2[im_arr2>0]=1
    fig,ax=plt.subplots(figsize=(7,7))
    ax.imshow(im_arr,zorder=2,vmin=1,vmax=1000000,cmap='inferno',alpha=0.9)            
    ax.imshow(im_arr2,zorder=1,cmap='Greys',alpha=0.2)  
    plt.axis('off')
    ax.axes.get_xaxis().set_visible(False)
    ax.axes.get_yaxis().set_visible(False)
    currfile_rendered = datadir+os.sep+'gif_input_%s.png' %i
    fig.savefig(currfile_rendered,bbox_inches='tight', pad_inches = 0,dpi=150)
    plt.show() 
    plt.clf() 
    currfiles_rendered.append(currfile_rendered) 
with imageio.get_writer(output_gif, mode='I',duration=frame_duration) as writer:
    for filename in currfiles_rendered:
        if os.path.exists(filename):
            image = imageio.imread(filename)
            writer.append_data(image)
# Remove temporary files
for filename in set(currfiles_warped):
    if os.path.exists(filename):
        os.remove(filename)      
for filename in set(currfiles_rendered):
    if os.path.exists(filename):
        os.remove(filename)           
        
