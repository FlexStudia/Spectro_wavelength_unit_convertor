# coding: utf-8

# PACKAGES
import filecmp
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import numpy as np

from main import *
from tools.data_pars import DataPars

# test QApp
test_app = QApplication(sys.argv)


# TESTS
# warning system
def test_warning_system():
    # input
    spectrum_file_path = "tests/files/simple.txt"
    # app run
    win = UnitsConvertorMW()
    # on win load
    assert "question" in win.ui.spectrum_status.text()
    assert "error" in win.ui.convert_status.text()
    assert "question" in win.ui.export_status.text()
    # on spectrum load
    win.select_file_action(spectrum_file_path)
    assert "ok" in win.ui.spectrum_status.text()
    assert "question" in win.ui.convert_status.text()
    assert "question" in win.ui.export_status.text()
    # convert
    win.convert()
    assert "ok" in win.ui.spectrum_status.text()
    assert "ok" in win.ui.convert_status.text()
    assert "ok" in win.ui.export_status.text()
    # on change
    win.ui.unit_to.setCurrentIndex(0)
    win.ui.unit_to.setCurrentIndex(1)
    assert "ok" in win.ui.spectrum_status.text()
    assert "question" in win.ui.convert_status.text()
    assert "question" in win.ui.export_status.text()
    win.close()

# full tests
def test_simple_same_unit_ascending():
    # input
    spectrum_file_path = "tests/files/simple.txt"
    unit_from = 0 # cm-1 ["cm-1", "micron", "nm", "A"]
    unit_to = 0 # cm-1
    ascending_order = True
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/simple_same_unit_ascending.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_simple_nm_micron_descending():
    # input
    spectrum_file_path = "tests/files/simple.txt"
    unit_from = 2  # nm ["cm-1", "micron", "nm", "A"]
    unit_to = 1  # micron
    ascending_order = False
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/simple_nm_micron_descending.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_ammoniac_nm_cm_descending():
    # input
    spectrum_file_path = "tests/files/sal_ammoniac_B01_1_temp_cal.txt"
    unit_from = 2  # nm ["cm-1", "micron", "nm", "A"]
    unit_to = 0  # cm-1
    ascending_order = False
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/conv_ammoniac.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_calcite_cm_micron_ascending():
    # input
    spectrum_file_path = "tests/files/Calcite-hydrotherm_BS00-02_bloc1_VfNfc48_i0e30a0_cal.txt"
    unit_from = 0  # cm-1 ["cm-1", "micron", "nm", "A"]
    unit_to = 1  # micron
    ascending_order = True
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/conv_Calcite.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_jarosite_A_nm_descending():
    # input
    spectrum_file_path = "tests/files/NH4-Jarosite_geo_cal.txt"
    unit_from = 3  # A ["cm-1", "micron", "nm", "A"]
    unit_to = 2  # nm
    ascending_order = False
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/conv_Jarosite.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_larderellite_micron_A_ascending():
    # input
    spectrum_file_path = "tests/files/larderellite_32-80_A09-3_90K_c.txt"
    unit_from = 1  # micron ["cm-1", "micron", "nm", "A"]
    unit_to = 3  # A
    ascending_order = True
    # app run
    win = UnitsConvertorMW()
    # setup inputs
    win.select_file_action(spectrum_file_path)
    win.ui.unit_from.setCurrentIndex(unit_from)
    win.ui.unit_to.setCurrentIndex(unit_to)
    win.ui.ascending_order.setChecked(ascending_order)
    win.ui.descending_order.setChecked(not ascending_order)
    # calc
    win.convert()
    # export
    export_file_path = "tests/main_files/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/main_files/conv_larderellite.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def end_file():
    pass
