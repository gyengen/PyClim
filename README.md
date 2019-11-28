# PyClim: PyClim produces a range of graphs and statistics to support the analysis of climate data, to support architectural / engineering / technology students to develop their early-stage bioclimatic design concepts. PyClim is organised arounnd a suite of modules:

- ClimAnalFunctions: functions relating to solar geometry, psychrometry and illumination.
- Psychros: creates psychrometric charts for the plotting ot climate data {and of transformed data to mimic evaporative cooling}
- SolarIrradiation_Aniso: creates solar irradiation surface plots [contour plots, for 10deg bins of azimuth and 5deg bins of altitude] or annual irradiation incident on a tilted plane solar collector.
- Sunpath: creates sunpath diagrams in stereographic projection; plotting time lines either according to solar or clock time; this latter representing the Analemma, calculated using the equation of time (EqT).
- SolarGeo_subplots: creates a 3x2 grid of subplots: the first three plotting daily variations in declination, EqT and solar daylength; the latter three plotting hourly solar altitude, azimuth and cosine of the angle of incidence on a collector.
- WeatherAnalysis: creates a range of plots and statistics of climate variables: 1) temporal solar irradiance / maps, 2) violin plots of key synoptic variables, 3) Monthly degree-day bar charts, 4) inverse illuminance cumulative distribution function: determines light switch-off hours, 5) wind speed / temperature frequency histograms, 6) ground temperature profile.
- WindRose: plots a user-controllable wind rose, with theta segments of azimuthal sectors falsecoloured either according to the hours that the wind approaches that direction and in the indicated (theta) speed, or at the indicated (theta) temperature. 


