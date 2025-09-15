#!/usr/bin/python
# -*- coding: utf-8 -*-

"""FluxCat.py: GUI for simulation of poisoning / degradation for catalytic fixed beds - Estimation of end of bed life"""

__author__ = "Markus Schindler"
__copyright__ = "Copyright 2025"

__licence__ = "MIT License"
__version__ = "0.1.0"
__maintainer__ = "Markus Schindler"
__email__ = "schindlerdrmarkus@gmail.com"
__status__ = "Development"

# Built-in / Generic Imports
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.factory import Factory

# Libs
from math import pi

# Own modules
from FVSorption import ChemiSorption 

# Load the kv file
Builder.load_file('content.kv')

class Designtool(FloatLayout):
    #############################################
    # Input Mask & Toggle Buttons - Temperature #
    #############################################
    feed_temperature_input = ObjectProperty(None)
    feed_celsius_toggle = ObjectProperty(None)
    feed_fahrenheit_toggle = ObjectProperty(None)
    feed_kelvin_toggle = ObjectProperty(None)
    ### Unit conversion functions
    def fahrenheit_kelvin(self, temperature):
        return (temperature - 32) / 1.8 + 273.15
        
    def celsius_kelvin(self, temperature):
        return temperature + 273.15

    def convert_temperature(self, temperature):
        if self.feed_celsius_toggle.state == 'down':
            return self.celsius_kelvin(temperature)
        elif self.feed_fahrenheit_toggle.state == 'down':
            return self.fahrenheit_kelvin(temperature)
        elif self.feed_kelvin_toggle.state == 'down':
            return temperature
        else:
            return 'None'

    ###############################################
    # Input Mask & Toggle Buttons - Fluid Density #
    ###############################################
    feed_density_input = ObjectProperty(None)
    feed_kilogrampercubicmeter_toggle = ObjectProperty(None)
    feed_kilogramperliter_toggle = ObjectProperty(None)
    feed_poundpercubicfeet_toggle = ObjectProperty(None)    
    ### Unit conversion functions
    def kilogramperliter_kilogrampercubicmeter(self, density):
        return density * 1000

    def poundpercubicfeet_kilogrampercubicmeter(self, density):
        return density * 0.453592 / (0.3048)**3
    
    def convert_density(self, density):
        if self.feed_kilogrampercubicmeter_toggle.state == 'down':
            return density
        elif self.feed_kilogramperliter_toggle.state == 'down':
            return self.kilogramperliter_kilogrampercubicmeter(density)
        elif self.feed_poundpercubicfeet_toggle.state == 'down':
            return self.poundpercubicfeet_kilogrampercubicmeter(density)
        else:
            return 'None'
    
    ##############################################
    # Input Mask & Toggle Buttons - Poison Level #
    ##############################################
    feed_level_input = ObjectProperty(None)
    feed_ppm_toggle = ObjectProperty(None)
    feed_milligramperliter_toggle = ObjectProperty(None)
    feed_percent_toggle = ObjectProperty(None)
    ### Unit conversion functions
    def milligramperliter_ppm(self, level, density):
        return level * 1000 / density

    def percent_ppm(self, level):
        return level * 10000

    def convert_level(self, level, density):
        if self.feed_ppm_toggle.state == 'down':
            return level
        elif self.feed_milligramperliter_toggle.state == 'down':
            return self.milligramperliter_ppm(level, density)
        elif self.feed_percent_toggle.state == 'down':
            return self.percent_ppm(level)
        else:
            return 'None'

    ########################################
    # Input Mask & Toggle Buttons - Outlet #
    ########################################
    feed_outlet_input = ObjectProperty(None)
    feed_ppm_toggle2 = ObjectProperty(None)
    feed_milligramperliter_toggle2 = ObjectProperty(None)
    feed_percent_toggle2 = ObjectProperty(None)
    ### Unit conversion functions
    def convert_outlet(self, outlet, density):
        if self.feed_ppm_toggle2.state == 'down':
            return outlet
        elif self.feed_milligramperliter_toggle2.state == 'down':
            return self.milligramperliter_ppm(outlet, density)
        elif self.feed_percent_toggle2.state == 'down':
            return self.percent_ppm(outlet)
        else:
            return 'None'

    ######################################
    # Input Mask & Toggle Buttons - Flow #
    ######################################
    process_flow_input = ObjectProperty(None)
    process_kilogramperhour_toggle = ObjectProperty(None)
    process_literpermin_toggle = ObjectProperty(None)
    process_poundperhour_toggle = ObjectProperty(None)
    ### Unit conversion functions
    def literpermin_kilogramperhour(self, density, flow):
        return flow * density / 60

    def poundperhour_kilogramperhour(self, flow):
        return flow / 0.453592
    
    def convert_flow(self, flow, density):
        if self.process_kilogramperhour_toggle.state == 'down':
            return flow
        elif self.process_literpermin_toggle.state == 'down':
            return self.literpermin_kilogramperhour(flow, density)
        elif self.process_poundperhour_toggle.state == 'down':
            return self.poundperhour_kilogramperhour(flow)
        else:
            return 'None'

    ##########################################
    # Input Mask & Toggle Buttons - Diameter #
    ##########################################
    process_diameter_input = ObjectProperty(None)
    process_meter_toggle = ObjectProperty(None)
    process_feet_toggle = ObjectProperty(None)
    process_inch_toggle = ObjectProperty(None)
    ### Unit conversion functions
    def feet_meter(self, size):
        return size * 0.3048

    def inch_meter(self, size):
        return size * 0.0254

    def convert_diameter(self, diameter):
        if self.process_meter_toggle.state == 'down':
            return diameter
        elif self.process_feet_toggle.state == 'down':
            return self.feet_meter(diameter)
        elif self.process_inch_toggle.state == 'down':
            return self.inch_meter(diameter)
        else:
            return 'None'

    ########################################
    # Input Mask & Toggle Buttons - Length #
    ########################################
    process_length_input = ObjectProperty(None)
    process_meter_toggle2 = ObjectProperty(None)
    process_feet_toggle2 = ObjectProperty(None)
    process_inch_toggle2 = ObjectProperty(None)
    ### Unit conversion functions
    def convert_length(self, length):
        if self.process_meter_toggle2.state == 'down':
            return length
        elif self.process_feet_toggle2.state == 'down':
            return self.feet_meter(length)
        elif self.process_inch_toggle2.state == 'down':
            return self.inch_meter(length)
        else:
            return 'None'

    ##############################################
    # Input Mask & Toggle Buttons - Bulk Density #
    ##############################################
    process_density_input = ObjectProperty(None)
    process_kilogrampercubicmeter_toggle = ObjectProperty(None)
    process_kilogramperliter_toggle = ObjectProperty(None)
    process_poundpercubicfeet_toggle = ObjectProperty(None)
    ### Unit conversion functions
    def convert_bulk_density(self, bulk_density):
        if self.process_kilogrampercubicmeter_toggle.state == 'down':
            return bulk_density
        elif self.process_kilogramperliter_toggle.state == 'down':
            return self.kilogramperliter_kilogrampercubicmeter(bulk_density)
        elif self.process_poundpercubicfeet_toggle.state == 'down':
            return self.poundpercubicfeet_kilogrampercubicmeter(bulk_density)
        else:
            return 'None'

    ##################################
    # Input Mask - Bed Void Fraction #
    ##################################
    bed_void_fraction = ObjectProperty(None)

    ##################################
    # Input Mask - Bodenstein Number #
    ##################################
    bed_bodenstein = ObjectProperty(None)
    
    #############################################
    # Input Mask - Dimensionless Film Diffusion #
    #############################################
    bed_film_diffusion = ObjectProperty(None)
    
    ###############################
    # Input Mask - Total Capacity #
    ###############################
    bed_capacity = ObjectProperty(None)

    ###############
    # Output Mask #
    ###############
    time_duration_hour = ObjectProperty(None)
    time_duration_day = ObjectProperty(None)
    time_duration_month = ObjectProperty(None)

    ################
    # Popup Window #
    ################

    def dismiss_popup(self):
        Factory.FailurePopup().open()
        
    # Simulation implementation
    def calculate(self):
        temperature = float(self.feed_temperature_input.text)
        fluid_temperature = self.convert_temperature(temperature)
        
        density = float(self.feed_density_input.text)
        fluid_density = self.convert_density(density)
        
        level = float(self.feed_level_input.text)
        contaminant_level = self.convert_level(level, fluid_density)

        outlet = float(self.feed_outlet_input.text)
        outlet_max = self.convert_outlet(outlet, fluid_density)

        flow = float(self.process_flow_input.text)
        fluid_flow = self.convert_flow(flow, fluid_density)
        
        diameter = float(self.process_diameter_input.text)
        reactor_diameter = self.convert_diameter(diameter)

        length = float(self.process_length_input.text)
        reactor_length = self.convert_length(length)

        bulk_density = float(self.process_density_input.text)
        bed_density = self.convert_bulk_density(bulk_density)

        void_fraction = float(self.bed_void_fraction.text)
        bodenstein = float(self.bed_bodenstein.text)
        film = float(self.bed_film_diffusion.text)
        total_capacity = float(self.bed_capacity.text)
                     
        # Change flow units from kilogram per hour to cubic meter per second
        fluid_flow /= 3600 * fluid_density

        model = ChemiSorption(fluid_temperature, fluid_density, contaminant_level, outlet_max, fluid_flow, reactor_diameter, reactor_length, bed_density, void_fraction, bodenstein, film, total_capacity)
        try:
            model.simulation()
            time_duration_hour = model.outlet_time()
            self.time_duration_hour.text = f'{time_duration_hour:.2f} hours'
            self.time_duration_day.text = f'{time_duration_hour / 24:.2f} days'
            self.time_duration_month.text = f'{time_duration_hour / (24 * 30.4375):.2f} months'
        except:
            self.dismiss_popup()
        
class FluxCatApp(App):
    def build(self):
        return Designtool()

if __name__ == '__main__':
    FluxCatApp().run()
