# Who is this for?

- **End users**: [download the ready-to-use executable](https://github.com/FlexStudia/Spectro_wavelength_unit_convertor/releases) (no Python required)
- **Researchers / developers**: use the scientific core as a Python module
- **Contributors**: see testing and build instructions

# Spectro Wavelength Unit Convertor

A desktop application built on a validated Python scientific core. A simple utility for converting wavelengths from one unit of measurement to another. 

# Features

- Supported units: cm-1, micron, nm, and A.
- The application works with files containing scientific data where the wavelength is in the first column. Otherwise, the data can have any number of columns.
- The data may be preceded by a header сontaining column names and other information describing the data.
- The application also allows selecting the order of wavelengths after conversion - ascending or descending.

# Executable

- [Can be downloaded in releases](https://github.com/FlexStudia/Spectro_wavelength_unit_convertor/releases)
- ОС: Currently, only the Windows EXE version is available. A Mac OS app is coming soon. Support for Linux is possible, but has not yet been requested.
- The exe file is located in the archive together with the icon folder. The contents of the archive should be extracted, and then everything is ready for use.

# Scientific core

The core in core.py is designed as a self-contained, UI-agnostic Python module and can be reused independently (accompanied by tools folder).

## How to use

Here is an example of using the scientific core:

```python
from core import UnitsConvertor

# set up the class
convert_action = UnitsConvertor(data_array, unit_from, unit_to, ascending_order)
# run conversion
convert_action.convert_units()
# get converted data
converted_data = convert_action.get_converted_data()
```

Here, data_array is a numpy 2-d array with data for conversion, unit_from and unit_to are strings from the list of supported units cm-1, micron, nm, or A, and ascending_order can be True or False depending on the desired order - ascending or descending.

A more detailed example of usage can be found in the demo_f function at the end of core.py. 

## Core tests & validation

The core code has undergone extensive testing for all possible combinations of units and sorting orders. The results of the code's performance were compared with a manually calculated conversion. These tests can be found in the tests folder in test_core.py.

# Repository structure

icons/                    # icons for the notification system that responds to user actions

maps/                    # logic maps (in the form of mind maps)

template/              # UI templates 

tests/                     # core and interface tests, utilities for this process, and used data files

tools/                     # auxiliary modules (for working with arrays, parsing scientific data files, and unit conversion)

LICENCE                 # a copy of GPL-3 under which this software is released

README.md          # this readme

core.py                   # core code for this project

main.py                  # UI-interface part and the base for the executable

requirements.txt    # with all dependencies (installation in venv: pip install -r requirements.txt)

# Licensing

This project is licensed under the GNU General Public License v3.0 (GPL-3).

### For scientific use

You are free to use the executable and the source code for research and
educational purposes without restriction. You may run the software, analyze
results, and use it in your scientific work.

Citation of this software in scientific publications is appreciated but not
legally required by the license.

### Redistribution and modifications

If you modify the code or redistribute the software (in source or binary form),
the resulting work must be distributed under the same GPL-3 license, and the
corresponding source code must be made publicly available.

This applies to the executable, the scientific core, and any derived works
based on this project.

# Citation

Documentation is currently limited to inline comments and examples.

# Contributing

Bug reports and small fixes are welcome. For larger changes, please open an issue first.
