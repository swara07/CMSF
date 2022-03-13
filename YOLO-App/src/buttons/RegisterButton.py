from PyQt5 import QtCore, QtGui, QtWidgets


class RegisterButton(QtWidgets.QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.color1 = QtGui.QColor(12, 135, 75)
        self.color2 = QtGui.QColor(8, 71, 40)
        
        self.qss = """
            QPushButton{
                color: white;
                border-style: none;
                border-width: 3px;
                border-radius: 8px;
                border-color: #0F49B5;
                border-bottom: 3px solid #0a3620;
                font: bold 14px;
                min-width: 10em;
                padding: 6px; }
        """
        
        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

        self.setStyleSheet(self.qss)


    def _animate(self, value):
        
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        self.qss += grad
        self.setStyleSheet(self.qss)

    def enterEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().enterEvent(event)