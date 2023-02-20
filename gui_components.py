from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer


class StatsDisplay:

    _n_label: QtWidgets.QLabel
    _n_unit_label: QtWidgets.QLabel 
    _real_time_elapsed_label: QtWidgets.QLabel
    _real_time_unit_label: QtWidgets.QLabel
    _simulated_time_elapsed_label: QtWidgets.QLabel
    _simulated_time_elapsed_label2: QtWidgets.QLabel
    _simulated_time_unit_label: QtWidgets.QLabel
    _simulated_time_unit_label2: QtWidgets.QLabel

    def __init__(
        self, 
        n_label: QtWidgets.QLabel,
        n_unit_label: QtWidgets.QLabel, 
        real_time_elapsed_label: QtWidgets.QLabel,
        real_time_unit_label: QtWidgets.QLabel,
        simulated_time_elapsed_label: QtWidgets.QLabel,
        simulated_time_elapsed_label2: QtWidgets.QLabel,
        simulated_time_unit_label: QtWidgets.QLabel,
        simulated_time_unit_label2: QtWidgets.QLabel) -> None:
        self._n_label = n_label
        self._n_unit_label = n_unit_label
        self._real_time_elapsed_label = real_time_elapsed_label
        self._real_time_unit_label = real_time_unit_label
        self._simulated_time_elapsed_label = simulated_time_elapsed_label
        self._simulated_time_elapsed_label2 = simulated_time_elapsed_label2
        self._simulated_time_unit_label = simulated_time_unit_label
        self._simulated_time_unit_label2 = simulated_time_unit_label2

    def set_n(self, value: float):
        self._n_label.setText(str(value))

    def set_n_unit(self, value: str):
        self._n_unit_label.setText(value)

    def set_simulated_time_elapsed(self, value: float):
        value_as_str = str(value)
        self._simulated_time_elapsed_label.setText(value_as_str)
        self._simulated_time_elapsed_label2.setText(value_as_str)

    def set_simulated_time_unit(self, value: str):
        self._simulated_time_unit_label.setText(value)
        self._simulated_time_unit_label2.setText(value)

    def set_real_time_elapsed(self, value: float):
        self._real_time_elapsed_label.setText(str(value))

    def set_real_time_unit(self, value: str):
        self._real_time_elapsed_label.setText(value)