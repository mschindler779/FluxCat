#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""FVSorption.py: Simulation of poisoning / degradation for catalytic fixed beds - Estimation of end of bed life"""

__author__ = "Markus Schindler"
__copyright__ = "Copyright 2025"

__license__ = "MIT License"
__version__ = "0.1.0"
__maintainer__ = "Markus Schindler"
__email__ = "schindlerdrmarkus@gmail.com"
__status__ = "Development"

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from math import exp, log, pi
class ChemiSorption:
    def __init__(self, temperature, fluid_density, contaminant, outlet, feed_flow, diameter, length, bed_density, void_fraction, bodenstein, film, total_capacity):
        # Fluid properties
        self.temperature = temperature # Kelvin
        self.fluid_density = fluid_density # kg per cubic meter
        self.C_i = contaminant # catalyst poison in ppm
        #self.effective_diffusivity = 0.001 # square meter per second
        self.bodenstein_number = bodenstein # dimensionless number
        self.gas_constant = 8.314462
        # Bed characteristics
        self.feed_flow = feed_flow # cubic meter per second
        self.film_diffusion_parameter = film # dimensionless parameter
        self.reactor_diameter = diameter # meter
        self.reactor_length = length # meter
        self.bed_density = bed_density # bulk density in kg per cubic meter
        self.outlet = outlet # maximum tolerable contaminant level in ppm
        self.langmuir_affinity = 700 # value kept constant - for most systems applicable
        self.langmuir_capacity = total_capacity # Chemisorption capacity in mg sorptive per mg catalyst
        self.void_bed_fraction = void_fraction # value for the compacted bed
        self.superficial_velocity = self.feed_flow / (pi / 4 * self.reactor_diameter**2)
        self.reactor_volume = self.reactor_diameter**2 / 4 * pi * self.reactor_length
        self.bed_mass = self.bed_density * self.reactor_volume
        self.concentration = self.C_i * 1E-6 * self.fluid_density
        # Simulation parameters
        self.D_ax = self.superficial_velocity / (self.bodenstein_number * self.reactor_length)
        self.limiter_function = 'UMIST' # several functions can be applied
        
    def film_diffusion(self, parameter):
        # dimensionless parameter for film diffusion ranging from k > 0 to infinity
        z = 2 * (exp(parameter) / (1 + exp(parameter)) - 0.5)
        # parameters for time coordinate transformation
        # function return shift to the left and applied multiplicator
        if z > 0:
            return (1 - z) / 2, 1 / z
        else:
            return 0, 1 # results in no change

    def langmuir_derivative(self, C):
        return self.langmuir_affinity / (1 + self.langmuir_affinity * C)**2

    # Function for estimating the advection velocity in the finite volume scheme
    def velocity(self, C):
        return self.u / (1 + (1 - self.void_bed_fraction) * self.langmuir_derivative(C) / self.void_bed_fraction)

    # Function for calculation of Upwind or Downwind scheme
    def wind(self, Q0, Q1, Q2, CFL, u):
        if (u > 0):
            return Q1 - CFL * (Q1 - Q0)
        else:
            return Q1 + CFL * (Q2 - Q1)

    # Slope calculation
    def flux(self, Q0, Q1, Q2, Q3, u):
        if (Q2 - Q1 == 0):
            return 10
        else:
            if (u > 0):
                # For velocity greater zero u > 0
                return (Q1 - Q0) / (Q2 - Q1)
            else:
                # For velocity smaller zero u < 0
                return (Q3 - Q2) / (Q2 - Q1)

    # Function for the Flux-Limiter function
    def limiter(self, theta, type = 'monotonized central'):
        if type == 'minmod':
            return max(0, min(1, theta))
        elif type == 'superbee':
            return max(0, min(1, 2 * theta), min(2, theta))
        elif type == 'monotonized central':
            return max(0, min((1 + theta) / 2, 2, 2 * theta))
        elif type == 'UMIST':
            return max(0, min(2 * theta, 0.25 + 0.75 * theta, 0.75 + 0.25 * theta, 2))
        elif type == 'van Leer':
            return (theta + abs(theta)) / (1 + abs(theta))
        else:
            # 'Upwind'
            return 0

    # Finite Volume Approach
    def flux_lim(self, Q0, Q1, Q2, Q3, Q4, CFL, u):
        if (u > 0):
            return Q2 - CFL * (Q2 - Q1) - 0.5 * CFL * (1 - CFL) * \
            (self.limiter(self.flux(Q1, Q2, Q3, Q4, u), self.limiter_function) * (Q3 - Q2) - self.limiter(self.flux(Q0, Q1, Q2, Q3, u), self.limiter_function) * (Q2 - Q1))
        else:  
            return Q2 + CFL * (Q3 - Q2) + 0.5 * CFL * (CFL - 1) * \
            (self.limiter(self.flux(Q1, Q2, Q3, Q4, u), self.limiter_function) * (Q3 - Q2) - self.limiter(self.flux(Q0, Q1, Q2, Q3, u), self.limiter_function) * (Q2 - Q1))

    # Dispersion Term
    def dispersion(self, Q0, Q1, Q2, D_ax):
        return -D_ax * self.dt / (2 * self.dx**2) * (Q2 - 2 * Q1 + Q0)

    # Simulation Task
    def simulation(self):
        # Spatial Step, Courant-Friedrichs-Lewy Number, Interstitial Velocity
        self.CFL, self.u = 0.7, 2
        # Spatial Step and time step
        self.dx = max(self.D_ax / self.u, 0.005)
        self.dt = self.CFL * self.dx / abs(self.u)

        # Discretization
        # Number of spatial grid points, Number of time grid points
        self.mdx = int(1 / self.dx)
        self.ndt = int(2 / (self.u * self.dt))

        # Creation of the fixed bed matrices
        self.C = np.zeros((self.mdx, self.ndt), dtype = float)

        # Initalize boundary conditions: C[x][t]; C[x=0][t=0] = 0, C[x=0][t>0] = 1
        for itervar in range(1, self.ndt):
            self.C[0, itervar], self.C[1, itervar] = 1, 1

        # Calculation of Finite Volume Scheme
        for i in range(1, self.ndt):
            for j in range(4, self.mdx):
                self.C[j-2][i] = self.flux_lim(self.C[j-4][i-1], self.C[j-3][i-1], self.C[j-2][i-1], self.C[j-1][i-1], self.C[j][i-1], self.CFL, \
                                               self.velocity(self.C[j-2][j-1])) - self.dispersion(self.C[j-4][i-1], self.C[j-3][i-1], self.C[j-2][i-1], self.D_ax)

        # Proper boundary calculation
        for k in range(1, self.ndt):
            for l in range(self.mdx - 2, self.mdx):
                self.C[l][k] = self.wind(self.C[l-2][k-1], self.C[l-1][k-1], self.C[l][k-1], self.CFL, self.velocity(self.C[l][k-1])) - \
                self.dispersion(self.C[l-2][k-1], self.C[l-1][k-1], self.C[l][k-1], self.D_ax)
            self.C[1][k] = self.wind(self.C[4][k-1], self.C[3][k-1], self.C[2][k-1], self.CFL, self.velocity(self.C[1][k-1])) - \
            self.dispersion(self.C[4][k-1], self.C[3][k-1], self.C[2][k-1], self.D_ax)
            self.C[0][k] = self.wind(self.C[3][k-1], self.C[2][k-1], self.C[1][k-1], self.CFL, self.velocity(self.C[0][k-1])) - \
            self.dispersion(self.C[3][k-1], self.C[2][k-1], self.C[1][k-1], self.D_ax)

        # Transformation of time domain using film diffusion
        self.shift, self.multiplicator = self.film_diffusion(self.film_diffusion_parameter)
        self.level = self.C_i * self.C[self.mdx-1] # Transformed concentration domain
        self.time = np.zeros((self.ndt), dtype = float) # Transformed time domain
        
        # Time is calculated in hours
        self.stoichiometric_time = 2 * self.langmuir_capacity * self.bed_mass / (self.concentration * self.feed_flow * 3600)
        for itervar in range(self.ndt):
            self.time[itervar] = (itervar * self.dt - self.shift) * self.multiplicator * self.stoichiometric_time
    
    # Time for reaching outlet specification
    def outlet_time(self):
        for itervar in range(self.ndt):
            if self.level[itervar] >= self.outlet and self.time[itervar] >= 0:
                return float(self.time[itervar])
