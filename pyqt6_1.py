import sys, os
import time
import random
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtCore import QObject
#from PyQt6.QtGui import QSound
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimedia import QSoundEffect

Key_Left = Qt.Key.Key_Left
Key_Right = Qt.Key.Key_Right

class Sound(QObject):
    def __init__(self):
        super(QObject, self).__init__()
        ###resources_dir = "resources"
        ###self.sounds_filenames = os.listdir(resources_dir)
        #self.media_player = QMediaPlayer()
        self.win_effect = QSoundEffect()
        self.win_effect.setSource(QUrl.fromLocalFile("resources\\ring.wav"))
        self.win_effect.setLoopCount(1)
        self.lose_effect = QSoundEffect()
        self.lose_effect.setSource(QUrl.fromLocalFile("resources\\damage.wav"))
        self.lose_effect.setLoopCount(1)
        
        #self.audio_output = QAudioOutput()
        #self.media_player.setAudioOutput(self.audio_output)
        
        
        
        ###self.qsounds = [QSound(resources_dir+"\\"+sound) for sound in self.sounds_filenames]
        
        #self.ring_content = QMediaContent.fromUrl(QUrl.fromLocalFile('resources\\ring.wav'))
        #self.damage_content = QMediaContent.fromUrl(QUrl.fromLocalFile('resources\\damage.wav'))
        #self.media_player.setMedia(media_content)
        ###self.sounds = dict(zip(self.sounds_filenames, self.qsounds))
        
    def win(self):
        ##self.media_player.setMedia(self.ring_content)
        ###self.sounds['ring.wav'].play()
        ##self.media_player.play()
        self.win_effect.play()

    def lose(self):
        #self.media_player.setMedia(self.damage_content)
        ###self.sounds['damage.wav'].play()
        #self.media_player.play()
        self.lose_effect.play()

class ColoredRectangleWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.sound = Sound()

        self.games = []
        self.last_R_lightness = 0
        self.last_L_lightness = 0
        self.last_selected_rect = ""
        self.last_selection_result = False
        # game element: dict : timestamp_shown, timestamp_solved, time_delta, RGB_L, RGB_R, L_L, L_R, result, deltaLightnessLminusR, info STRING (for game configuration data).

        self.color = QColor(255, 0, 0)  # Initial color is red
        self.colorR = QColor(255, 255, 0)  # 
        self.colorL = QColor(255, 0, 255)  # 
        self.buttonsPaneA = QWidget()
        self.buttonsPaneB = QWidget()
        self.buttonsPaneC = QWidget()
        self.buttonsPaneMain = QWidget()
        
        self.bigPane = QWidget()
        self.rectsWidget = QWidget()
        self.rectLeft = QWidget()
        self.rectRight = QWidget()
        
        self.rectsSize = QSize(400, 300)
        self.rectLeft.setFixedSize(self.rectsSize)
        self.rectRight.setFixedSize(self.rectsSize)
        # Create a layout
        layoutBig = QVBoxLayout()
        layoutRects = QHBoxLayout()
        
        layoutButtonsMain = QVBoxLayout()
        layoutButtonsA = QHBoxLayout()
        layoutButtonsB = QHBoxLayout()
        layoutConfigsA = QVBoxLayout()
    
    
        #labels
        # min_delta_red, min_delta_green, min_delta_blue  
        # max_delta_red, max_delta_green, max_delta_blue  
        # min_delta_h, min_delta_l, min_delta_s 
        # max_delta_h, max_delta_l, max_delta_s 
        # min_h, max_h, min_l, max_l, min_s, max_s
        self.RGBSettingsLabels = QHBoxLayout() #LAYOUT RGB labels
        self.RGBSettingsEdits = QHBoxLayout() #LAYOUT RGB edits
        self.LabelMinDeltaRed = QLabel("min delta R")
        self.LabelMinDeltaGreen = QLabel("min delta G")
        self.LabelMinDeltaBlue = QLabel("min delta B")
        self.MinDeltaRedEdit = QLineEdit("0")
        self.MinDeltaGreenEdit = QLineEdit("0")
        self.MinDeltaBlueEdit = QLineEdit("0")
        

        self.LabelMaxDeltaRed = QLabel("max delta R")
        self.LabelMaxDeltaGreen = QLabel("max delta G")
        self.LabelMaxDeltaBlue = QLabel("max delta B")
        self.MaxDeltaRedEdit = QLineEdit("30")
        self.MaxDeltaGreenEdit = QLineEdit("30")
        self.MaxDeltaBlueEdit = QLineEdit("30")

        self.RGBSettingsLabels.addWidget(self.LabelMinDeltaRed)
        self.RGBSettingsLabels.addWidget(self.LabelMaxDeltaRed)
        self.RGBSettingsLabels.addWidget(self.LabelMinDeltaGreen)
        self.RGBSettingsLabels.addWidget(self.LabelMaxDeltaGreen)
        self.RGBSettingsLabels.addWidget(self.LabelMinDeltaBlue)
        self.RGBSettingsLabels.addWidget(self.LabelMaxDeltaBlue)
        
        self.RGBSettingsEdits.addWidget(self.MinDeltaRedEdit)
        self.RGBSettingsEdits.addWidget(self.MaxDeltaRedEdit)
        self.RGBSettingsEdits.addWidget(self.MinDeltaGreenEdit)
        self.RGBSettingsEdits.addWidget(self.MaxDeltaGreenEdit)
        self.RGBSettingsEdits.addWidget(self.MinDeltaBlueEdit)
        self.RGBSettingsEdits.addWidget(self.MaxDeltaBlueEdit)

        layoutConfigsA.addLayout(self.RGBSettingsLabels)
        layoutConfigsA.addLayout(self.RGBSettingsEdits)

        
        self.HSLSettingsDeltasLabels = QHBoxLayout() #LAYOUT HSL deltas labels
        self.HSLSettingsDeltasEdits = QHBoxLayout() #LAYOUT HSL deltas edits
        self.LabelMinDeltaHue = QLabel("min delta H")
        self.LabelMinDeltaSaturation = QLabel("min delta S")
        self.LabelMinDeltaLightness = QLabel("min delta L")
        self.MinDeltaHueEdit = QLineEdit("0")
        self.MinDeltaSaturationEdit = QLineEdit("0")
        self.MinDeltaLightnessEdit = QLineEdit("0")
        
        self.LabelMaxDeltaHue = QLabel("max delta H")
        self.LabelMaxDeltaSaturation = QLabel("max delta S")
        self.LabelMaxDeltaLightness = QLabel("max delta L")
        self.MaxDeltaHueEdit = QLineEdit("30")
        self.MaxDeltaSaturationEdit = QLineEdit("30")
        self.MaxDeltaLightnessEdit = QLineEdit("30")
        
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMinDeltaHue)
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMaxDeltaHue)
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMinDeltaSaturation)
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMaxDeltaSaturation)
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMinDeltaLightness)
        self.HSLSettingsDeltasLabels.addWidget(self.LabelMaxDeltaLightness)
        
        self.HSLSettingsDeltasEdits.addWidget(self.MinDeltaHueEdit)
        self.HSLSettingsDeltasEdits.addWidget(self.MaxDeltaHueEdit)
        self.HSLSettingsDeltasEdits.addWidget(self.MinDeltaSaturationEdit)
        self.HSLSettingsDeltasEdits.addWidget(self.MaxDeltaSaturationEdit)
        self.HSLSettingsDeltasEdits.addWidget(self.MinDeltaLightnessEdit)
        self.HSLSettingsDeltasEdits.addWidget(self.MaxDeltaLightnessEdit)

        layoutConfigsA.addLayout(self.HSLSettingsDeltasLabels)
        layoutConfigsA.addLayout(self.HSLSettingsDeltasEdits)
        
        self.HSLSettingsMinMaxLabels = QHBoxLayout() #LAYOUT min-max HSL labels
        self.HSLSettingsMinMaxEdits = QHBoxLayout() #LAYOUT min-max HSL edits
        self.LabelMinHue = QLabel("min H")
        self.LabelMaxHue = QLabel("max H")
        self.MinHueEdit = QLineEdit("0") #TODO: derive min HUE from RGB!
        self.MaxHueEdit = QLineEdit("321") #TODO: derive max HUE from RGB!
        
        self.LabelMinSaturation = QLabel("min S")
        self.LabelMaxSaturation = QLabel("max S")
        self.MinSaturationEdit = QLineEdit("0") #TODO: derive min SAT from RGB!
        self.MaxSaturationEdit = QLineEdit("228") #TODO: derive max SAT from RGB!
        
        self.LabelMinLightness = QLabel("min L")
        self.LabelMaxLightness = QLabel("max L")
        self.MinLightnessEdit = QLineEdit("0") #TODO: derive min LIGHTNESS from RGB!
        self.MaxLightnessEdit = QLineEdit("255") #TODO: derive max LIGHTNESS from RGB!
        
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMinHue)
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMaxHue)
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMinSaturation)
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMaxSaturation)
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMinLightness)
        self.HSLSettingsMinMaxLabels.addWidget(self.LabelMaxLightness)
        
        self.HSLSettingsMinMaxEdits.addWidget(self.MinHueEdit)
        self.HSLSettingsMinMaxEdits.addWidget(self.MaxHueEdit)
        self.HSLSettingsMinMaxEdits.addWidget(self.MinSaturationEdit)
        self.HSLSettingsMinMaxEdits.addWidget(self.MaxSaturationEdit)
        self.HSLSettingsMinMaxEdits.addWidget(self.MinLightnessEdit)
        self.HSLSettingsMinMaxEdits.addWidget(self.MaxLightnessEdit)
        
        layoutConfigsA.addLayout(self.HSLSettingsMinMaxLabels)
        layoutConfigsA.addLayout(self.HSLSettingsMinMaxEdits)
        
        self.ConfigsAWidget = QWidget()
        self.ConfigsAWidget.setLayout(layoutConfigsA)
        
        
        # Create a button
        self.button = QPushButton('Change Color', self)
        self.button.clicked.connect(self.change_color)
        self.button2 = QPushButton('Change Color Randomly', self)
        self.button2.clicked.connect(self.change_color_random)
        self.buttonLeftSelect = QPushButton('Select LEFT')
        self.buttonRightSelect = QPushButton('Select RIGHT')
        self.buttonApplyColorGeneratingConfig = QPushButton('Apply color config')
        
        self.left_arrow_shortcut = QShortcut(QKeySequence(Key_Left), self)
        self.right_arrow_shortcut = QShortcut(QKeySequence(Key_Right), self)
        self.left_arrow_shortcut.activated.connect(self.left_arrow_pressed)
        self.right_arrow_shortcut.activated.connect(self.right_arrow_pressed)
        
        # Add the button to the layout
        #layoutButtonsA.addWidget(self.button)
        layoutButtonsA.addWidget(self.button2)
        layoutButtonsA.addWidget(self.buttonLeftSelect)
        layoutButtonsA.addWidget(self.buttonRightSelect)
        self.buttonsPaneA.setLayout(layoutButtonsA)

        
        
        #layoutButtonsB.addWidget(self.buttonApplyColorGeneratingConfig)
        layoutRects.addWidget(self.rectLeft)
        layoutRects.addWidget(self.rectRight)
        #layoutRects.addWidget(self.rectLeft)
    
        self.rectsWidget.setLayout(layoutRects)
        layoutBig.addWidget(self.rectsWidget) # VBox
        layoutBig.addWidget(self.buttonsPaneA) # VBox
        layoutBig.addWidget(self.ConfigsAWidget)
        
        layoutBig.addWidget(self.buttonsPaneB) # VBox
        
        self.setLayout(layoutBig)

        self.change_color_random()

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
                self.sound.win()
            if self.last_R_lightness < self.last_L_lightness:
                self.sound.lose()
                self.last_selection_result = False
        if self.last_selected_rect == "L":
            if self.last_L_lightness >= self.last_R_lightness:
                self.last_selection_result = True
                self.sound.win()
            if self.last_L_lightness < self.last_R_lightness:
                self.sound.lose()
                self.last_selection_result = False

        self.games[-1]["selected_rect"] = self.last_selected_rect
        self.games[-1]["time_solved"] = time.time()
        self.games[-1]["spent"] = self.games[-1]["time_solved"] - self.games[-1]["time_shown"]
        self.games[-1]["result"] = { True:"Win", False:"Loss" }[self.last_selection_result]
        self.games[-1]["delta lightness abs"] = abs(self.games[-1]["L lightness"] - self.games[-1]["R lightness"])
        
        #self.games[-1]["solution_time"] = self.games[-1]
        with open("games_log.txt", "a+") as fout:
            msg = str([str(k) + "=" + str(v) for k,v in self.games[-1].items()])[1:-1]
            fout.write(msg + "\n")
                            
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
