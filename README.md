## GlobeAnim
GlobeAnim is a Python tool that projects a GeoTIFF file onto a globe and rotates it, outputting an animated GIF. GlobeAnim uses ```gdal``` to read and process GeoTIFF data, and ```PIL```, ```matplotlib``` and ```imageio``` to create an animated GIF. 

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/land_shallow_topo_8192_georef.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/BlackMarble_2016_01deg_geo.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/Beck_KG_V1_present_0p5.gif" width="200" />    <img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.gif" width="200" />

Code works as follows: 
- Given a GeoTiff of global coverage, use ```gdalwarp``` to reproject from the source CRS into an orthographic projection, centered at the Equator and for steps of 5 degree longitude, from -180 to 180 degree longitude.
- Render all warped raster datasets, add the "back side" of the globe (optionally).
- Output them as an animated GIF.
- Delete temporary files.

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.gif" width="500" />

Data source: European Commission, Joint Research Centre.

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/land_shallow_topo_8192_georef.gif" width="500" />

Data source: NASA Visible Earth - Blue marble.

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/BlackMarble_2016_01deg_geo.gif" width="500" />

Data source: NASA Visible Earth - Earth at night.

<img src="https://github.com/johannesuhl/globeanim/blob/main/outputs/Beck_KG_V1_present_0p5.gif" width="500" />

Data source: Beck et al. (2018).

In the provided .py file, three examples are shown: GeoTiffs representing an RGB image, a categorical, or a continuous gridded surface.

###References

NASA Visible Earth - Earth at Night: https://www.visibleearth.nasa.gov/images/144898/earth-at-night-black-marble-2016-color-maps
NASA Visible Earth - Blue Marble: https://visibleearth.nasa.gov/collection/1484/blue-marble
Beck et al. (2018): Present and future Köppen-Geiger climate classification maps at 1-km resolution. figshare. Dataset. https://doi.org/10.6084/m9.figshare.6396959
Schiavina et al. (2023): GHS-POP R2023A - GHS population grid multitemporal (1975-2030). European Commission, Joint Research Centre (JRC). https://doi.org/10.2905/2FF68A52-5B5B-4A22-8F40-C41DA8332CFE; Dataset: https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/GHSL/GHS_POP_GLOBE_R2023A/GHS_POP_E2020_GLOBE_R2023A_4326_30ss/V1-0/GHS_POP_E2020_GLOBE_R2023A_4326_30ss_V1_0.zip
