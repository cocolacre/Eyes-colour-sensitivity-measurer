import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize


class ColoredRectangleWidget(QWidget):
    def __init__(self):
        super().__init__()



        self.games = []
        self.last_R_lightness = 0
        self.last_L_lightness = 0
        self.last_selected_rect = ""
        self.last_selection_result = False
        # game element: dict : timestamp_shown, timestamp_solved, time_delta, RGB_L, RGB_R, L_L, L_R, result, deltaLightnessLminusR, info STRING (for game configuration data).

        self.color = QColor(255, 0, 0)  # Initial color is red
        self.colorR = QColor(255, 255, 0)  # 
        self.colorL = QColor(255, 0, 255)  # 
        self.buttonsPane = QWidget()
        self.bigPane = QWidget()
        self.rectsWidget = QWidget()
        self.rectLeft = QWidget()
        self.rectRight = QWidget()
        
        self.rectsSize = QSize(375, 375)
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
        self.buttonLeftSelect = QPushButton('Select LEFT')
        self.buttonRightSelect = QPushButton('Select RIGHT')

        self.left_arrow_shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.right_arrow_shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.left_arrow_shortcut.activated.connect(self.left_arrow_pressed)
        self.right_arrow_shortcut.activated.connect(self.right_arrow_pressed)
        
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

    def right_arrow_pressed(self):
        self.last_selected_rect = "R"
        self.check_select_result()

    def left_arrow_pressed(self):
        self.last_selected_rect = "L"
        self.check_select_result()

    def check_select_result(self):
        if self.last_selected_rect == "R":
            if self.last_R_lightness >= self.last_L_lightness:
                self.last_selection_result = True
            if self.last_R_lightness < self.last_L_lightness:
                self.last_selection_result = False
        if self.last_selected_rect == "L":
            if self.last_L_lightness >= self.last_R_lightness:
                self.last_selection_result = True
            if self.last_L_lightness < self.last_R_lightness:
                self.last_selection_result = False
        
        self.games[-1]["selected_rect"] = self.last_selected_rect
        self.games[-1]["time_solved"] = time.time()
        self.games[-1]["spent"] = self.games[-1]["time_solved"] - self.games[-1]["time_shown"]
        self.games[-1]["result"] = { True:"Win", False:"Loss" }[self.last_selection_result]
        self.games[-1]["delta lightness abs"] = abs(self.games[-1]["L lightness"] - self.games[-1]["R lightness"])
        
        #self.games[-1]["solution_time"] = self.games[-1]
        with open("games_log.txt", "a+") as fout:
            msg = str([str(k) + "=" + str(v) for k,v in self.games[-1].items()])[1:-1]
            fout.writelines([msg,])
                            
        self.change_color_random()
        
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
        c_L_R_norm = colorL.red() / 255.0
        c_L_G_norm = colorL.green() / 255.0
        c_L_B_norm = colorL.blue() / 255.0

        c_R_R_norm = colorR.red() / 255.0
        c_R_G_norm = colorR.green() / 255.0
        c_R_B_norm = colorR.blue() / 255.0

        c_min_L = min(c_L_R_norm, c_L_G_norm, c_L_B_norm)
        c_min_R = min(c_R_R_norm, c_R_G_norm, c_R_B_norm)
        c_max_L = max(c_L_R_norm, c_L_G_norm, c_L_B_norm)
        c_max_R = max(c_R_R_norm, c_R_G_norm, c_R_B_norm)
        
        L_R = (c_min_R + c_max_R) / 2.0 #lightness RIGHT
        L_L = (c_min_L + c_max_L) / 2.0 #lightness LEFT
        print(f"{L_L=}    {L_R=}")
        print(f"{255.0*L_L=}    {255.0*L_R=}")
        print(f"{colorL.lightness()=}    {colorR.lightness()=}")
        self.last_R_lightness = L_R
        self.last_L_lightness = L_L
        self.update()
        self.games.append({"time_shown":time.time()})
        self.games[-1]["L RGB"] = (colorL.red(), colorL.green(),colorL.blue())
        self.games[-1]["R RGB"] = (colorR.red(), colorR.green(),colorR.blue())
        self.games[-1]["L lightness"] = 255.0*L_L
        self.games[-1]["R lightness"] = 255.0*L_R

    
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
