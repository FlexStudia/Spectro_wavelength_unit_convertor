# Spectro Wavelength Unit Convertor

A desktop application for converting wavelength values between different units in scientific data files. The underlying calculations are based on a validated scientific model implemented in Python.

## Who is this for?

- **End users**: [download the ready-to-use executable](https://github.com/FlexStudia/Spectro_wavelength_unit_convertor/releases) (no Python required)
- **Researchers / developers**: use the scientific core as a Python module
If you only want to use the program to convert wavelength units and do not work with Python or source code, you only need the executable from the [Releases page](https://github.com/FlexStudia/Spectro_wavelength_unit_convertor/releases). No programming knowledge is required.

# Features

- Supported units: cm⁻¹, micron, nm, and angstrom (Å).
- Works with plain text and CSV files containing scientific data, where the wavelength values are stored in the first column.
- Input data may include a header with column names and additional metadata.
- Allows selecting the order of wavelengths after conversion (ascending or descending).

# Executable

- The executable can be downloaded from the [Releases page](https://github.com/FlexStudia/Spectro_wavelength_unit_convertor/releases)
- **OS support**:
  - Currently, only a Windows EXE version is available.
  - A macOS version is planned
  - Linux support is possible but has not yet been requested
- The EXE is distributed as an archive containing the executable file and an icon folder. Extract the archive, and the application is ready to use.

# Scientific core

The scientific core, implemented in `core.py`, is designed as a self-contained, UI-agnostic Python module and can be reused independently (together with the
modules in the `tools/` directory).

## How to use

Example usage of the scientific core:

```
from core import UnitsConvertor

# set up the converter
convert_action = UnitsConvertor(data_array, unit_from, unit_to, ascending_order)
# run conversion
convert_action.convert_units()
# get converted data
converted_data = convert_action.get_converted_data()
```

Here, `data_array` is a NumPy 2D array containing the data to be converted. `unit_from` and `unit_to` are strings specifying the units (cm-1, micron,
nm, or A). `ascending_order` is a boolean flag controlling the sorting order of the output data.

A more detailed usage example is provided in the `demo_f` function at the end of `core.py`. 

## Core tests & validation

The scientific core has been extensively tested for all supported combinations of units and sorting orders. Conversion results were validated against manually calculated reference values.
The corresponding tests are located in the `tests/` directory (`test_core.py`).

# Repository structure

```
icons/           # icons used by the UI notification system
maps/            # logic maps (mind maps)
template/        # UI templates 
tests/           # core and interface tests, test utilities, and test data
tools/           # auxiliary modules (array handling, data parsing, unit conversion)
core.py          # scientific core
main.py          # UI layer and entry point for the executable
requirements.txt # project dependencies (pip install -r requirements.txt)
LICENCE          # GNU GPL-3 license text
README.md        # this readme file
```

# Licensing

This project is licensed under the GNU General Public License v3.0 (GPL-3).

### For scientific use

You are free to use the executable and the source code for research and educational purposes without restriction. You may run the software, analyze results, and use it in your scientific work.

Citation of this software in scientific publications is appreciated but not legally required by the license.

### Redistribution and modifications

If you modify the code or redistribute the software (in source or binary form), the resulting work must be distributed under the same GPL-3 license, and the corresponding source code must be made publicly available.

This applies to the executable, the scientific core, and any derived works based on this project.

# Documentation

Documentation is currently limited to inline comments and usage examples provided in the source code.

# Contributing

If you encounter any bugs or issues, please report them by email at flex.studia.help@gmail.com.
