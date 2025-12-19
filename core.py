# coding: utf-8

# PACKAGES
import numpy as np
from copy import deepcopy

# MODULES
from tools.units_change_operations import change_unit


class UnitsConvertor:
    def __init__(self, data_array, unit_from, unit_to, ascending_order):
        self.class_setter(data_array, unit_from, unit_to, ascending_order)
        self.set_globals()

    def class_setter(self, data_array, unit_from, unit_to, ascending_order):
        self.data_array = data_array # nd-array with at least two lines, where the wavelength is in the first column
        self.unit_from = unit_from  # possible units: cm-1, micron, nm, A
        self.unit_to = unit_to  # possible units: cm-1, micron, nm, A
        self.ascending_order = ascending_order # True or False

    def set_globals(self):
        self.data_converted = np.zeros(0)

    def get_converted_data(self):
        return self.data_converted

    def convert_units(self):
        # deep-copy the initial data to data_converted
        self.data_converted = deepcopy(self.data_array)
        # convert wavelength
        converted_wavelength_data = change_unit(self.data_array[:, 0], self.unit_from, self.unit_to)
        # check order: if order in no Ok -> revers all data in data_converted
        if not ((converted_wavelength_data[0] < converted_wavelength_data[1] and self.ascending_order)
                or (converted_wavelength_data[0] > converted_wavelength_data[1] and not self.ascending_order)):
            self.data_converted = self.data_converted[::-1]
            converted_wavelength_data = converted_wavelength_data[::-1]
        # copy wavelength to data_converted
        self.data_converted[:, 0] = converted_wavelength_data


def demo_f():
    # input
    data_array = np.array([[1000.000000, 0.705083, 0.002189, 0.849915, 0.001760, 322.094034, 3.863321, 1000.000000,
                            35.000000, 3000000.000000, 188.767883, 0.000000, 0.000000],
                           [2000.000000, 0.678184, 0.001913, 0.410710, 0.000671, 354.525122, 7.726905, 1000.000000,
                            35.000000, 3000000.000000, 434.109033, 0.000000, 0.000000],
                           [3000.000000, 0.049520, 0.001497, 0.032695, 0.000530, 33.081305, 15.534905, 1000.000000,
                            35.000000, 100000.000000, 658.861883, 0.000000, 0.000000],
                           [4000.000000, 0.019943, 0.002312, 0.030155, 0.001532, 8.624264, 15.454073, 1000.000000,
                            35.000000, 10000.000000, 781.503750, 0.000000, 0.000000],
                           [5000.000000, 0.002913, 0.001491, 0.053155, 0.057989, 1.954467, 15.346796, 1000.000000,
                            100.000000, 1000.000000, 898.973733, 0.000000, 0.000000]])
    unit_from = "cm-1"
    unit_to = "micron"
    ascending_order = False
    # assert
    convert_action = UnitsConvertor(data_array, unit_from, unit_to, ascending_order)
    convert_action.convert_units()
    print(convert_action.get_converted_data())

# demo_f()
