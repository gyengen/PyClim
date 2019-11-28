import matplotlib.pyplot as plt
import warnings as wr
import pandas as pd
import numpy as np
import math

from ClimAnalFunctions import * 

__author__ = ["Prof. Darren Robinson"]
__contributor__ = ["Norbert Gyenge"]
__contact__ = "d.robinson1@sheffield.ac.uk"
__institude__ = "University of Sheffield"
__date__ = 2019

class SI_Aniso():

    '''This module creates solar irradiation surface plots, either for an isotropic or for an
    anisotropic sky. A prior version also calculated a quotient of the two, to demonstrate the
    importance of modelling anisotropy.

    THIS SURFACE PLOT CALCULATION WOULD PROBABLY BE 'MUCH' QUICKER USING A GLOBAL RADIANCE 
    DISTRIBUTION MODEL. THE DISTRIBUTION ONLY NEEDS TO BE CALCULATED ONCE. ONLY THE PATCH
    VIEW FACTORS NEED TO BE RE-CALCULATED. THIS WILL NEED A MECHANISM TO ESTIMATE THE VIEW
    FACTOR FOR CUTS THROUGH PATCHES FROM A PROGRESSIVELY TILTED PLANE. 

    EXAMPLE:
    
        >>> import SolaIrradiation_Aniso as SIA
        >>> ci = SIA.SI_Aniso(lat = 50.7, lon = -30, tz = 1, ts = -1)
        >>> ci.parameters(DiffuseOnly = False, isotropic = False, FirstSweep = True)
        >>> ci.read_data(fn = Finningley.csv)
        >>> ci.calculate_SI()
        >>> ci.plot()

    PARAMETERS:

        DiffuseOnly:

        isotropic:  
        
        FirstSweep:

        lat:

        lon:

        tz:

        ts:'''

    def __init__(self, lat = 53.7, lon = -1, tz = 0, ts = -0.5):

        #Missing COMMENT, default = 53.7 degrees converted to radians
        self.lat = np.radians(lat)

        # Longitude
        self.lon = lon

        # Timezone
        self.tz = tz

        # Timeshift, for the hour-centred time convention
        self.ts = ts

        # Load default parameters
        self.parameters()

    def parameters(self, DiffuseOnly = False, isotropic = False):

        #Missing COMMENT
        self.DiffuseOnly = DiffuseOnly

        #Missing COMMENT
        self.isotropic = isotropic


    def read_data(dat):

        '''This method reads data from a Python Pandas dataframe

        PARAMETERS: dat - Pandas dataframe

        RETURNS: None'''

        self.dat = dat

    def read_file(self, fn = None, header = 0, g_inx = 5, d_inx=6):

        ''' This method reads a csv file.

        PARAMETERS:

            fn: string - The name of the file to be read with path

            header: int - Number of header rows. 0 if no header, default.

        '''

        if fn == None:

            wr.warning('Filename could not be found.')

        else:
            if header == 0:

                self.dat = pd.read_csv(fn, header = None) 

            else:

                self.dat = pd.read_csv(fn, skiprows=range(header), header = None) 

        # Select rows global_list amd diffuse_list
        self.global_list = self.dat.iloc[:, g_inx].values
        self.diffuse_list = self.dat.iloc[:, d_inx].values

    def calculate_SI(self):


        ''' Documentation

        '''

        # Comment
        self.annualirrad_list = []
        
        # Convert numpy arrays to list for speed-up
        global_list = self.global_list.tolist()
        diffuse_list = self.diffuse_list.tolist()

        # Calculating declination over the year and Time difference between solar and Earth time
        buff = [[declin_angle(i), time_diff(i, False, self.lon, self.tz, self.ts)] for i in range(1,366)]

        # Extract dec and timediff
        dec_list, timediff_list = list(zip(*buff))
        
        # Solar ephemeris: altitude
        solalt_list = [solar_altitude(i, j+timediff_list[i-1], self.lat, dec_list[i-1])
                       for i in range(1,366)
                       for j in range(1,25)]

        # Solar ephemeris: azimuth

        solaz_list = [solar_azimuth(i, j+timediff_list[i-1], self.lat, solalt_list[(j+(24*(i-1)))-2], dec_list[i-1])
                       for i in range(1,366)
                       for j in range(1,25)]

        # Creating spatial mash in radians
        spatial_mesh = [[wallaz * np.pi/180, tilt * np.pi/180]
                         for tilt in range(0,95,10)
                         for wallaz in range (0,360,10)]

        # Iterate over spatial dimension
        for i in range(len(spatial_mesh)):
           
            # New globalirradbeta for each iteration
            globalirradbeta=0

            # Iterate over temporal dimension
            for j in range(len(solaz_list)):

                # Calculate CAI
                incidence = cai(spatial_mesh[i][0], spatial_mesh[i][1], solalt_list[j], solaz_list[j])

                # Calculate global irradiance
                globalirradbeta += igbeta(int(j/366)+1,   incidence,
                                          global_list[j], diffuse_list[j],
                                          solalt_list[j], spatial_mesh[i][1],
                                          self.isotropic, self.DiffuseOnly)

            # Annual irradiance
            self.annualirrad_list.append(globalirradbeta)

    def plot(self, fname=None, n=128, **kwargs):
        #This creates a 2D irradiation surface plot

        if self.isotropic==True:
            title = "Isotropic Sky"

        else:
            title = "Anisotropic Sky"

        # Generate mesgrid
        X, Y = np.meshgrid(np.linspace(0, 350, 36), np.linspace(0, 90, 10))

        # Initalision plotting
        fig, ax=plt.subplots(1,1)

        # Missing comment
        Z = (np.array(self.annualirrad_list)*10**-6).reshape(10,36)

        #NB: 16 sets number of division; alpha sets opacity; 'magma', 'jet' and 'viridis' are also good cmaps
        cp = ax.contourf(X, Y, Z, n, cmap='plasma', alpha=1.0) 

        # Adds a colorbar
        fig.colorbar(cp, label = 'Solar irradiation, MWh/m^2') 

        # Title
        ax.set_title('Annual Solar Irradiation Surface Plot: ' + title)

        # X and Y label
        ax.set_xlabel('Collector azimuth, deg')
        ax.set_ylabel('Collector tilt, deg')

        plt.tight_layout()

        if fname is None:
            plt.show()

        else:
            plt.savefig(fname, **kwargs)


# ----------- To be REMOVE, testing only
ci = SI_Aniso()
ci.read_file(fn = 'Finningley.csv', header = 3)
ci.calculate_SI()
ci.plot(n=16)
# ----------- 
