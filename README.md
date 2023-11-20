## GlobeAnim
GlobeAnim is a Python tool that projects a GeoTIFF file onto a globe and rotates it, outputting an animated GIF. GlobeAnim uses ```gdal``` to read and process GeoTIFF data, and ```PIL```, ```matplotlib``` and ```imageio``` to create an animated GIF. 

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/land_shallow_topo_8192_georef.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/BlackMarble_2016_01deg_geo.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/Beck_KG_V1_present_0p5.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.gif" width="200" />

Code works as follows: 
- Given a GeoTiff of global coverage, use ```gdalwarp``` to reproject from the source CRS into an orthographic projection, centered at the Equator and for steps of 5 degree longitude, from -180 to 180 degree longitude.
- Render all warped raster datasets, add the "back side" of the globe (optionally).
- Output them as an animated GIF.
- Delete temporary files.
<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.gif" width="500" />
<img src="https://github.com/johannesuhl/blob/main/outputs/land_shallow_topo_8192_georef.gif" width="500" />
<img src="https://github.com/johannesuhl/blob/main/outputs/BlackMarble_2016_01deg_geo.gif" width="500" />
<img src="https://github.com/johannesuhl/blob/main/outputs/Beck_KG_V1_present_0p5.gif" width="500" />
In the provided .py file, three examples are shown: GeoTiffs representing an RGB image, a categorical, or a continuous gridded surface.
