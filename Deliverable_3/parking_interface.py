from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import main_window_ui
import json as json
import paho.mqtt.client as mqtt


class ParkingLotInterface(QtWidgets.QMainWindow, main_window_ui.Ui_MainWindow):
    """UI Window Class"""

    def __init__(self):
        """initialize the window class"""
        super(ParkingLotInterface,self).__init__()
        self.setupUi(self)
        self.warning_on_off_flg = False
        self.warning_on_button.clicked.connect(self.turn_on_warning)
        self.warning_off_button.clicked.connect(self.turn_on_warning)
        self.mqttBroker = ""

    def turn_on_off_warning(self):
        """ Turn on or off the warning light
        """
        # TODO: need to connect to LED

        # Turn on warning
        if self.warning_on_button.isChecked() and not self.on_off:
            self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 80%); border-radius: 25px")
            self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 30%); border-radius:25px")
            self.warning_off_button.setChecked(False)
            self.warning_on_off_flg = True
        else:
            self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 30%); border-radius: 25px")
        
        # Turn off Warning
        if self.warning_off_button.isChecked() and self.on_off:
            self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 80%); border-radius: 25px")
            self.warning_on_light.setStyleSheet("background-color: rgba(0,200,0, 30%); border-radius:25px")
            self.warning_on_button.setChecked(False)
            self.warning_on_off_flg = False
        else:
            self.warning_off_light.setStyleSheet("background-color: rgba(200,0,0, 30%); border-radius: 25px")

        




if __name__== "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow=ParkingLotInterface()
    mainWindow.show()
    sys.exit(app.exec())
