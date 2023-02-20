from app import Ui_MainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from random import randint
import sys
from half_life import HalfLifeCalculator
from gui_components import StatsDisplay

class Sim():
    def __init__(self, mw, calculator: HalfLifeCalculator, defaultInterval=100, modeCurrent=0, timeScale=0, nZero=0, halfLife=0):
        self.mw = mw
        self.calculator = calculator

        self.defaultInterval = defaultInterval
        self.modeCurrent = modeCurrent
        self.simulationActive = False
        self.timeElapsed = 0

        self.ticker = QTimer()
        self.tickerElapsed = QTimer()
        self.ticker.timeout.connect(self.tick)
        self.tickerElapsed.timeout.connect(self.elapse_time)
        self.ticker.setInterval(self.defaultInterval)
        self.tickerElapsed.setInterval(self.defaultInterval)

        self.modeCurrent = modeCurrent
        self.timeScale = timeScale
        self.nZero = nZero
        self.halfLife = halfLife

        self.y = 0
        self.x = 0
        self.graph_y = [0]
        self.graph_x = [0]

    def elapse_time(self):
        self.timeElapsed += 0.1

    def start(self):
        self.simulationActive = True
        self.y = self.nZero
        self.graph_x = [0]
        self.graph_y = [self.nZero]

        self.tick()
        self.tickerElapsed.start()
        self.ticker.start()

    def stop(self):
        self.simulationActive = False
        self.tickerElapsed.stop()
        self.ticker.stop()

    def tick(self):
        if self.simulationActive == True:
            ## VIS ##
            painter = QtGui.QPainter(self.mw.ui.labelVis.pixmap())
            painter.eraseRect(0, 0, self.mw.visWidth, self.mw.visHeight)
            pen = QtGui.QPen()
            pen.setWidth(2)
            pen.setColor(QtGui.QColor('red'))
            painter.setPen(pen)
            for n in range(int(self.y)):
                painter.drawPoint(
                    randint(0, self.mw.visWidth),  # x
                    randint(0, self.mw.visHeight)   # y
                )
            painter.end()
            self.mw.ui.labelVis.update()

            ## GRAPH ##
            self.mw.graphDataDash.setData(self.graph_x, self.graph_y)
            self.mw.graphData.setData(self.graph_x, self.graph_y)

            ## STATS ##
            self.mw.stats.set_n(round(self.y, 2))
            self.mw.stats.set_simulated_time_elapsed(round(self.x, 2))
            self.mw.stats.set_real_time_elapsed(round(self.timeElapsed, 1))

            ## UPDATE DATA ##
            self.x += self.timeScale
            self.y = self.calculator.n_remaining(
                self.nZero, self.halfLife, self.x)
            self.graph_x.append(self.x)
            self.graph_y.append(self.y)

    def set_speed(self, interval):
        interval = int(interval)
        self.ticker.setInterval(interval)

class MainWindow(QtWidgets.QMainWindow):

    stats: StatsDisplay

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.stats = StatsDisplay(
            self.ui.statsYAxisLabelStat,
            self.ui.statsXAxisLabelStatUnit,
            self.ui.statsRealTimeStat,
            self.ui.statsRealTimeStatUnit,
            self.ui.statsXAxisLabelStat,
            self.ui.statsSimulatedTimeStat,
            self.ui.statsXAxisLabelStatUnit,
            self.ui.statsSimulatedTimeStatUnit
        )

        self.presets = {
            "<Select>": {"nZeroUnit": "", "halfLife": 0.0, "timeScale": "Years"},
            "Carbon-14": {"nZeroUnit": "Nuclei", "halfLife": 5730.0, "timeScale": "Years"},
            "Plutonium-239": {"nZeroUnit": "Nuclei", "halfLife": 24110.0, "timeScale": "Years"},
        }

        for preset_name in self.presets:
            self.ui.inputPresetsComboBox.addItem(preset_name)

        self.nZeroUnit = self.ui.inputNZeroLineEdit.text()

        self.stats.set_n(0)
        self.stats.set_simulated_time_elapsed(0)
        self.stats.set_real_time_elapsed(0)

        self.visWidth = self.ui.labelVis.width()
        self.visHeight = self.ui.labelVis.height()
        self.ui.labelVis.setPixmap(
            QtGui.QPixmap(self.visWidth, self.visHeight))
        self.clear_canvas()

        pen = pg.mkPen(color='#000000')
        self.ui.graphWidgetHalfLifeDashboard.setBackground('w')
        self.ui.graphWidgetHalfLife.setBackground('w')
        self.graphDataDash = self.ui.graphWidgetHalfLifeDashboard.plot([0], [
                                                                       0], pen=pen)
        self.graphData = self.ui.graphWidgetHalfLife.plot([0], [0], pen=pen)

        self.ui.inputPresetsComboBox.currentIndexChanged[str].connect(
            self.apply_preset)
        self.ui.inputPresetsComboBox.setCurrentIndex(0)

        self.ui.inputNZeroLineEdit.textChanged.connect(
            self.change_nZero_unit_label)

        self.ui.inputTimeScaleComboBox.currentIndexChanged[str].connect(
            self.change_time_unit_label)
        self.ui.inputTimeScaleComboBox.setCurrentIndex(4)

        self.ui.controlsStartStopButton.clicked.connect(self.start_sim)
        self.ui.controlsResetButton.clicked.connect(self.reset_all)

        self.ui.controlsSimSpeedButton_1.clicked.connect(
            lambda: self.set_sim_speed(self.sim.defaultInterval*4))
        self.ui.controlsSimSpeedButton_2.clicked.connect(
            lambda: self.set_sim_speed(self.sim.defaultInterval*2))
        self.ui.controlsSimSpeedButton_3.clicked.connect(
            lambda: self.set_sim_speed(self.sim.defaultInterval))
        self.ui.controlsSimSpeedButton_4.clicked.connect(
            lambda: self.set_sim_speed(self.sim.defaultInterval/2))
        self.ui.controlsSimSpeedButton_5.clicked.connect(
            lambda: self.set_sim_speed(self.sim.defaultInterval/5))

    def apply_preset(self, preset):
        selected_preset = self.presets[preset]
        self.ui.inputNZeroLineEdit.setText(selected_preset["nZeroUnit"])
        self.ui.inputHalfLifeDoubleSpinBox.setValue(
            selected_preset["halfLife"])
        self.ui.inputTimeScaleComboBox.setCurrentText(
            selected_preset["timeScale"])

    def change_nZero_unit_label(self, nZeroUnit):
        self.stats.set_n_unit(nZeroUnit)
        self.nZeroUnit = nZeroUnit

    def change_time_unit_label(self, timeUnit):
        self.ui.inputSimulatedTimeLabel.setText(f"Simulated {timeUnit}")
        self.stats.set_simulated_time_unit(timeUnit)
        self.timeUnit = timeUnit

    def start_sim(self):
        nZero = self.ui.inputNZeroDoubleSpinBox.value()
        halfLife = self.ui.inputHalfLifeDoubleSpinBox.value()
        timeScale = float(self.ui.inputSimulatedTimeSpinBox.value()/10)

        self.ui.inputNZeroLineEdit.textChanged.disconnect(
            self.change_nZero_unit_label)
        self.ui.controlsStartStopButton.clicked.disconnect(self.start_sim)
        self.ui.controlsStartStopButton.clicked.connect(self.stop_sim)
        self.ui.controlsStartStopButton.setText("Stop")
        self.ui.controlsStartStopButton.show()

        self.ui.graphWidgetHalfLifeDashboard.setTitle("Half Life Chart")
        self.ui.graphWidgetHalfLife.setTitle("Half Life Chart")
        self.ui.graphWidgetHalfLifeDashboard.setLabel('left', self.nZeroUnit)
        self.ui.graphWidgetHalfLife.setLabel('left', self.nZeroUnit)
        self.ui.graphWidgetHalfLifeDashboard.setLabel('bottom', self.timeUnit)
        self.ui.graphWidgetHalfLife.setLabel('bottom', self.timeUnit)

        self.sim = Sim(self, HalfLifeCalculator(), nZero=nZero, halfLife=halfLife,
                       timeScale=timeScale)
        self.sim.start()

    def stop_sim(self):
        self.ui.controlsStartStopButton.clicked.disconnect(self.stop_sim)
        self.ui.controlsStartStopButton.hide()
        self.sim.stop()

    def reset_all(self):
        if self.sim.simulationActive == True:
            self.sim.stop()
        self.ui.controlsStartStopButton.show()
        self.clear_canvas()
        self.graphDataDash.setData([0], [0])
        self.graphData.setData([0], [0])
        self.stats.set_n(0)
        self.stats.set_real_time_elapsed(0)
        self.stats.set_simulated_time_elapsed(0)
        self.ui.controlsStartStopButton.clicked.connect(self.start_sim)
        self.ui.controlsStartStopButton.setText("Start")
        self.ui.inputNZeroLineEdit.textChanged.connect(
            self.change_nZero_unit_label)
        del self.sim

    def set_sim_speed(self, interval):
        self.sim.set_speed(interval=interval)

    def clear_canvas(self):
        painter = QtGui.QPainter(self.ui.labelVis.pixmap())
        painter.eraseRect(0, 0, self.visWidth, self.visHeight)
        painter.end()
        self.ui.labelVis.update()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())