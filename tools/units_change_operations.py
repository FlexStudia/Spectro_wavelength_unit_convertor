# coding: utf-8

"""
    This module contains auxiliary functions used to change the unit.
"""

# PACKAGES
import numpy as np

def units_conversion(value_to_convert, unit_from, unit_to):  # possible units: cm-1, micron, nm, A
    def do_conversion(value, factor, operation):
        return value * factor if operation == "multiply" else factor / value

    try:
        UNITS = ["cm-1", "micron", "nm", "A"]
        CONVERSION_FACTORS = {
            ("cm-1", "micron"): (10000, "divide"),
            ("micron", "cm-1"): (10000, "divide"),
            ("cm-1", "nm"): (10000000, "divide"),
            ("nm", "cm-1"): (10000000, "divide"),
            ("cm-1", "A"): (100000000, "divide"),
            ("A", "cm-1"): (100000000, "divide"),
            ("micron", "nm"): (1000, "multiply"),
            ("nm", "micron"): (1 / 1000, "multiply"),
            ("A", "micron"): (1 / 10000, "multiply"),
            ("micron", "A"): (10000, "multiply"),
            ("nm", "A"): (10, "multiply"),
            ("A", "nm"): (1 / 10, "multiply")
        }
        if unit_from == unit_to:
            return value_to_convert
        if value_to_convert == 0:
            return 0
        if unit_from not in UNITS or unit_to not in UNITS:
            print(f"Unit can be only cm-1, micron, nm or A ('{unit_from}' and '{unit_to}'were set)!")
            return np.nan
        factor, operation = CONVERSION_FACTORS.get((unit_from, unit_to))
        if factor:
            return do_conversion(value_to_convert, factor, operation)
        print("Conversion not supported!")
        return np.nan
    except Exception as e:
        print(f"Error in units_conversion: {e}")
        return np.nan

def change_unit(data_list, unit_from, unit_to):
    try:
        return np.array([units_conversion(d, unit_from, unit_to) for d in data_list])
    except Exception as e:
        print(f"Error in change_unit: {e}")
        return np.zeros(0)
