# coding: utf-8

# PACKAGES
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox
from PyQt6.QtCore import Qt, QSettings
import sys
import os
from pathlib import Path
import numpy as np

from core import UnitsConvertor
from tools.array_tools import is_array_empty

# MODULES
from tools.data_pars import DataPars

# TEMPLATES
from template.mw import Ui_MainWindow as Ui_MainWindow

# GLOBALS
version = "0.1"
copyright = "<a href='https:www.gnu.org/licenses/gpl-3.0.html'>The GNU General Public License v3.0</a>"
author_mail = "<a href='mailto: flex.studia.dev@gmail.com'>flex.studia.dev@gmail.com</a>"
bug_support_mail = "<a href='mailto: flex.studia.help@gmail.com'>flex.studia.help@gmail.com</a>"
github_url = "https://github.com/FlexStudia/Spectro_wavelength_unit_convertor"
__app_name__ = "Wavelength unit covertor"
__org_name__ = "Flex Studia Dev"
__org_site__ = github_url
settings = QSettings(__org_name__, __app_name__)
about_text = (f"<b>{__app_name__}</b> v.{version}"
              f"<p>Copyright: {copyright}</p>"
              f"<p><a href='{github_url}'>GitHub repository</a> (program code and more information)</p>"
              f"<p>Created by Gorbacheva Maria ({author_mail})</p>"
              "<p>Scientific base by Bernard Schmitt, IPAG (<a href='mailto: bernard.schmitt@univ-grenoble-alpes.fr'>bernard.schmitt@univ-grenoble-alpes.fr</a>)</p>"
              f"<p>For any questions and bug reports, please, mail at {bug_support_mail}</p>"
              "<p>In case of a bug, please report it and specify your operating system, "
              "provide a detailed description of the problem with screenshots "
              "and the files used and produced, if possible. Your contribution matters to make this program better!</p>")


class UnitsConvertorMW(QtWidgets.QMainWindow):
    def __init__(self):
        super(UnitsConvertorMW, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # setter & globals
        self.class_setter()
        self.set_globals()
        # window tilte
        self.setWindowTitle(f"{__app_name__} v.{version}")
        # menu
        self.set_menu()
        # UI
        self.set_ui()

    # init -> class setter & globals
    def class_setter(self):
        # spectrum
        self.spectrum_data = np.zeros(0)
        self.spectrum_path = ""
        self.spectrum_file_header = ""
        self.spectrum_file_separator = ""
        self.spectrum_file_accuracy = []
        # coversion result
        self.spectrum_data_converted = np.zeros(0)

    def set_globals(self):
        # bigger btn style
        self.bigger_btn_style = "QPushButton{padding: 7px; font-size: 14px;}"
        # unit list
        self.units_list = ["cm-1", "micron", "nm", "A"]
        # warning system tool tip dict
        self.tool_tip_dict = {
            # spectrum
            "spectrum empty": (self.ui.spectrum_status, self.ui.spectrum_text_output, "question",
                               "Load a spectrum file to convert"),
            "spectrum loaded": (self.ui.spectrum_status, self.ui.spectrum_text_output, "ok",
                                "The spectrum file has been successfully loaded"),
            "spectrum error": (self.ui.spectrum_status, self.ui.spectrum_text_output, "error",
                               "Unable to load the spectrum file"),
            # convert
            "not ready to convert": (self.ui.convert_status, self.ui.convert_output_text, "error",
                                     "No file to convert."),
            "not convert yet": (self.ui.convert_status, self.ui.convert_output_text, "question",
                                "Everything is ready for conversion!"),
            "convert expired": (self.ui.convert_status, self.ui.convert_output_text, "question",
                                "The parameters have changed.\nPlease run conversion again."),
            "convert error": (self.ui.convert_status, self.ui.convert_output_text, "error",
                              "Something has gone wrong.\nUnable to convert."),
            "convert finished": (self.ui.convert_status, self.ui.convert_output_text, "ok",
                                 "The conversion has been successfully completed!"),
            # export
            "nothing to export": (self.ui.export_status, self.ui.export_output_text, "question",
                                  "Nothing to export yet."),
            "export expired": (self.ui.export_status, self.ui.export_output_text, "question",
                               "The parameters have changed.\nThe previous result is still available for export."),
            "export ready": (self.ui.export_status, self.ui.export_output_text, "ok",
                             "The export is ready!"),
            "export finished": (self.ui.export_status, self.ui.export_output_text, "ok",
                                "The export has been completed successfully!"),
            "export error": (self.ui.export_status, self.ui.export_output_text, "error",
                             "Something has gone wrong.\nUnable to export"),
        }

    # messages
    def show_dialog(self, message, title, icon, buttons=QMessageBox.StandardButton.Ok):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.setIcon(icon)
        dlg.setStandardButtons(buttons)
        return dlg.exec()

    def show_info_dialog(self, message, title="Information"):
        self.show_dialog(message, title, QMessageBox.Icon.Information)

    def show_error_dialog(self, message, title="Error!"):
        self.show_dialog(message, title, QMessageBox.Icon.Critical)

    # init -> set_menu
    def set_menu(self):
        try:
            extractAction = QAction("&About", self)
            extractAction.setStatusTip('About The App')
            extractAction.triggered.connect(self.show_about)
            self.statusBar()
            mainMenu = self.menuBar()
            fileMenu = mainMenu.addMenu('&Help')
            fileMenu.addAction(extractAction)
        except Exception as e:
            message = f"Error in set_menu: {e}"
            self.show_error_dialog(self, message)

    # init -> set_menu -> show_about
    def show_about(self):
        self.show_info_dialog(about_text, "About")

    # init -> set_ui
    def set_ui(self):
        try:
            self.set_spectrum()
            self.set_units()
            self.set_order()
            self.set_conversion()
            self.set_export()
        except Exception as e:
            message = f"Error in set_ui: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_spectrum
    def set_spectrum(self):
        try:
            # btn spectrum_select
            self.ui.spectrum_select.setStyleSheet(f"{self.bigger_btn_style}")
            self.ui.spectrum_select.clicked.connect(self.file_dialog)
            # warning system update
            self.warning_system("spectrum empty")
        except Exception as e:
            message = f"Error in set_spectrum: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_spectrum -> file_dialog
    def file_dialog(self):
        try:
            # search in settings for the last saved location
            if settings.value("spectrum_dir") and os.path.isdir(settings.value("spectrum_dir")):
                dir_name = settings.value("spectrum_dir")
            else:
                dir_name = ""
            # file path dialog
            file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", dir_name,
                                                       "Text documents (*.txt *.csv *tsv);;All files (*.*)")
            # if valid file path
            if os.path.isfile(file_path):
                settings.setValue("spectrum_dir", os.path.dirname(file_path))  # update settings
                self.select_file_action(file_path)  # run further processing
        except Exception as e:
            message = f"Error in select_file_dialog: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_spectrum -> file_dialog -> select_file_action
    def select_file_action(self, file_path):
        def get_file_data(file_path):
            try:
                data_read = DataPars(file_path)
                data_read.file_pars_f()
                return data_read.file_body, data_read.file_header, data_read.file_separator, data_read.file_accuracy
            except:
                return np.zeros(0), "", "", np.zeros(0)

        try:
            if os.path.isfile(file_path):
                # file read: get all data & parameters
                file_content, file_header, file_separator, file_accuracy = get_file_data(file_path)
                # set label with file name
                self.ui.spectrum_label.setText(os.path.basename(file_path))
                # file data processing
                if not is_array_empty(file_content):  # there is data
                    # set globals
                    self.spectrum_data = file_content
                    self.spectrum_path = file_path
                    self.spectrum_file_header = file_header
                    self.spectrum_file_separator = file_separator
                    self.spectrum_file_accuracy = file_accuracy
                    # expire export if exist
                    self.on_any_parameter_change()
                    # warning system update
                    self.warning_system("spectrum loaded")
                    self.warning_system("not convert yet")
                else:  # there is no data
                    self.warning_system("spectrum error")
                    self.warning_system("not ready to convert")
        except Exception as e:
            message = f"Error in select_file_action: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_units
    def set_units(self):
        try:
            def unit_setup(action_type):
                try:
                    unit_action_dict = {"unit_from": [self.ui.unit_from, 2],
                                        "unit_to": [self.ui.unit_to, 1]}
                    unit_container = unit_action_dict[action_type][0]
                    # fill unit container
                    unit_container.insertItems(0, self.units_list)
                    # set default valur /saved value
                    if settings.value(action_type) or settings.value(action_type) == 0:
                        unit_container.setCurrentIndex(settings.value(action_type))
                    else:
                        unit_index = unit_action_dict[action_type][1]
                        unit_container.setCurrentIndex(unit_index)
                        settings.setValue(action_type, unit_index)
                    # connect function on change
                    unit_container.currentIndexChanged.connect(lambda: self.unit_changed(action_type))
                except Exception as e:
                    message = f"Error in unit_setup: {e}"
                    self.show_error_dialog(self, message)

            # unit from
            unit_setup("unit_from")
            # unit to
            unit_setup("unit_to")
        except Exception as e:
            message = f"Error in set_units: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_units -> unit_changed
    def unit_changed(self, action_type):
        unit_action_dict = {"unit_from": self.ui.unit_from,
                            "unit_to": self.ui.unit_to}
        unit_container = unit_action_dict[action_type]
        settings.setValue(action_type, unit_container.currentIndex())
        self.on_any_parameter_change()

    # init -> set_ui -> set_order
    def set_order(self):
        try:
            # read order from settings if there is
            if settings.value("ascending_order"):
                if settings.value("ascending_order") == "True":
                    self.ui.ascending_order.setChecked(True)
                    self.ui.descending_order.setChecked(False)
                else:
                    self.ui.ascending_order.setChecked(False)
                    self.ui.descending_order.setChecked(True)
            else:
                self.ui.ascending_order.setChecked(True)
                self.ui.descending_order.setChecked(False)
                settings.setValue("ascending_order", "True")
            # set order toggle
            self.ui.ascending_order.toggled.connect(self.order_changed)
            self.ui.descending_order.toggled.connect(self.order_changed)
        except Exception as e:
            message = f"Error in set_order: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_order -> set_order -> order_changed
    def order_changed(self):
        try:
            if self.ui.ascending_order.isChecked():
                settings.setValue("ascending_order", "True")
            else:
                settings.setValue("ascending_order", "False")
            self.on_any_parameter_change()
        except Exception as e:
            message = f"Error in order_changed: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_conversion
    def set_conversion(self):
        try:
            self.ui.convert_btn.setStyleSheet(f"{self.bigger_btn_style}")
            self.ui.convert_btn.clicked.connect(self.convert)
            self.warning_system("not ready to convert")
        except Exception as e:
            message = f"Error in set_conversion: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_conversion -> convert
    def convert(self):
        try:
            if "ok" in self.ui.convert_status.text() or "question" in self.ui.convert_status.text():
                convert_action = UnitsConvertor(self.spectrum_data,
                                                self.ui.unit_from.currentText(), self.ui.unit_to.currentText(),
                                                True if self.ui.ascending_order.isChecked() else False)
                convert_action.convert_units()
                self.spectrum_data_converted = convert_action.get_converted_data()
                self.warning_system("convert finished")
                self.warning_system("export ready")
        except Exception as e:
            message = f"Error in convert: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export
    def set_export(self):
        try:
            self.ui.export_btn.setStyleSheet(f"{self.bigger_btn_style}")
            self.ui.export_btn.clicked.connect(self.export_dialog)
            self.warning_system("nothing to export")
        except Exception as e:
            message = f"Error in set_export: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export -> export_dialog
    def export_dialog(self):
        try:
            if "ok" in self.ui.export_status.text():
                # file name creation: original name stem + _wincor + original file extension
                save_file_name = Path(self.spectrum_path).stem + f"_{self.ui.unit_to.currentText()}" + Path(self.spectrum_path).suffix
                # export path saved in settings if available
                if settings.value("export_dir") and os.path.isdir(settings.value("export_dir")):
                    save_file_name = os.path.join(settings.value("export_dir"), save_file_name)
                # get export path
                export_path, _ = QFileDialog.getSaveFileName(self, "Save File", save_file_name, "Text Files (*.txt)")
                # if export path
                if export_path:
                    settings.setValue("export_dir", os.path.dirname(export_path))  # update settings
                    self.export_action(export_path)  # run export action
        except Exception as e:
            self.warning_system("export error")
            message = f"Error in export_dialog: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export -> export_dialog -> export_action
    def export_action(self, export_path):
        try:
            def create_export_str():
                try:
                    data_to_str = ""
                    # header
                    for line in self.spectrum_file_header:
                        data_to_str += line
                    # data
                    for line in self.spectrum_data_converted:
                        for column_number, column in enumerate(line):
                            data_to_str += f"{column:.{self.spectrum_file_accuracy[column_number]}f}"
                            if column_number != len(line) - 1:
                                data_to_str += self.spectrum_file_separator
                        data_to_str += "\n"
                    return data_to_str
                except Exception as e:
                    self.warning_system("export error")
                    message = f"Error in create_export_str: {e}"
                    self.show_error_dialog(self, message)

            if "ok" in self.ui.export_status.text():
                with open(export_path, 'w+') as file_output:
                    file_output.write(create_export_str())
                self.warning_system("export finished")
        except Exception as e:
            self.warning_system("export error")
            message = f"Error in export_action: {e}"
            self.show_error_dialog(self, message)

    # on_any_parameter_change <-> conversion & export expiration
    def on_any_parameter_change(self):
        try:
            if "ok" in self.ui.convert_status.text():
                self.warning_system("convert expired")
            if "ok" in self.ui.export_status.text():
                self.warning_system("export expired")
        except Exception as e:
            message = f"Error in on_any_parameter_change: {e}"
            self.show_error_dialog(self, message)

    # warning system: interface output on user interaction
    def warning_system(self, action_type):
        try:
            icon_container = self.tool_tip_dict[action_type][0]  # get icon container
            text_output_container = self.tool_tip_dict[action_type][1]  # get text output container
            icon_type = self.tool_tip_dict[action_type][2]  # get icon type
            tool_tip_text = self.tool_tip_dict[action_type][3]  # gt output text
            icon_container.setText(f"<html><img src='icons/{icon_type}.svg'></html>")  # set icon container
            text_output_container.setText(tool_tip_text)  # set output text
        except Exception as e:
            message = f"Error in warning_system: {e}"
            self.show_error_dialog(self, message)


# APP RUN
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = UnitsConvertorMW()
    win.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
    win.show()
    sys.exit(app.exec())
