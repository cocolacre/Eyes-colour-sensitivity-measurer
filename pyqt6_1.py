import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize


class ColoredRectangleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.color = QColor(255, 0, 0)  # Initial color is red
        self.colorR = QColor(255, 255, 0)  # 
        self.colorL = QColor(255, 0, 255)  # 
        self.buttonsPane = QWidget()
        self.bigPane = QWidget()
        self.rectsWidget = QWidget()
        self.rectLeft = QWidget()
        self.rectRight = QWidget()
        
        self.rectsSize = QSize(300, 300)
        self.rectLeft.setFixedSize(self.rectsSize)
        self.rectRight.setFixedSize(self.rectsSize)
        # Create a layout
        layoutBig = QVBoxLayout()
        layoutRects = QHBoxLayout()
        layoutButtons = QHBoxLayout()


        # Create a button
        self.button = QPushButton('Change Color', self)
        self.button.clicked.connect(self.change_color)
        self.button2 = QPushButton('Change Color Randomly', self)
        self.button2.clicked.connect(self.change_color_random)

        # Add the button to the layout
        layoutButtons.addWidget(self.button)
        layoutButtons.addWidget(self.button2)
        self.buttonsPane.setLayout(layoutButtons)

        layoutRects.addWidget(self.rectLeft)
        layoutRects.addWidget(self.rectRight)
        #layoutRects.addWidget(self.rectLeft)
    
        self.rectsWidget.setLayout(layoutRects)
        layoutBig.addWidget(self.rectsWidget) # VBox
        layoutBig.addWidget(self.buttonsPane) # VBox
        self.setLayout(layoutBig)


    def generate_random_color(self):
        return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def generate_two_slightly_different_random_colors(self):
        color1 =  QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color1R =  random.randint(0, 255)
        color1G =  random.randint(0, 255)
        color1B =  random.randint(0, 255)
        
        delta_MAX = 64
        delta = random.randint(0,delta_MAX)
        deltaR = random.randint(0,delta)
        delta = random.randint(0,delta_MAX)
        deltaG = random.randint(0,delta)
        delta = random.randint(0,delta_MAX)
        deltaB = random.randint(0,delta)

        if color1R + deltaR > 255:
            color2R = color1R - deltaR
        else:
            color2R = color1R + deltaR

        if color1G + deltaG > 255:
            color2G = color1G - deltaG
        else:
            color2G = color1G + deltaG

        if color1B + deltaB > 255:
            color2B = color1B - deltaB
        else:
            color2B = color1B + deltaB
        
        chance = random.randint(0,1)
        if chance == 0:
            return QColor(color1R, color1G, color1B), QColor(color2R, color2G, color2B)
        else:
            return QColor(color2R, color2G, color2B), QColor(color1R, color1G, color1B)


    def change_color(self):
        # Change the color of the rectangle to a random color
        self.color = QColor(255, 0, 0)  # You can modify this line to generate a random color

        # Trigger a repaint
        self.update()

    def change_color_random(self):
        # Change the color of the rectangle to a random color
        rni = random.randint
        self.color = QColor(rni(0,255), rni(0,255), rni(0,255))  # You can modify this line to generate a random color
        self.colorR = QColor(rni(0,255), rni(0,255), rni(0,255))  # You can modify this line to generate a random color
        #self.colorR = QColor(0, 255, 0)  # You can modify this line to generate a random color
        self.colorL = QColor(rni(0,255), rni(0,255), rni(0,255))  # You can modify this line to generate a random color
        #self.colorL = QColor(0, 0, 255)  # You can modify this line to generate a random color

        # Trigger a repaint
        colorL, colorR = self.generate_two_slightly_different_random_colors()
        #self.rectLeft.setStyleSheet(f"background-color: {self.generate_random_color().name()};")
        self.rectLeft.setStyleSheet(f"background-color: {colorL.name()};")
        #self.rectRight.setStyleSheet(f"background-color: {self.generate_random_color().name()};")
        self.rectRight.setStyleSheet(f"background-color: {colorR.name()};")
        print(f"{repr(colorL)=}   {repr(colorR)=}")
        print(f"{colorL.lightness()=}    {colorR.lightness()=}")
        print(f"{colorL.hue()=}    {colorR.hue()=}")
        print(f"{colorL.saturation()=}    {colorR.saturation()=}")
        self.update()
    
    def paintEvent(self, event):
        # Paint the colored rectangle
        painter = QPainter(self)
        #painter.fillRect(self.rect(), self.color)
        #painter.fillRect(self.rectRight.rect(), self.colorL)
        #painter.fillRect(self.Left.rect(), self.colorL)
        #painter.fillRect(0,0,100,100, self.colorR)
        #painter.fillRect(100,100,100,100, self.colorL)
        #painter.fillRect(self.rectLeft.rect(), self.colorL)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ColoredRectangleWidget()
    window.setGeometry(50, 50, 800, 1200)
    window.setWindowTitle('Colored Rectangle App')
    window.show()

    sys.exit(app.exec())
