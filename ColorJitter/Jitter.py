from krita import (ManagedColor)

import colorsys as cs
import random as r
from enum import Enum


NEW_COLOR_THRESHHOLD = 0.1



class Formulae(Enum):
    RANDOM = 0,
    NORMAL = 1,
    LINEARPOSITIVE = 3,
    LINEARNEGATIVE = 4

    def randomize(base, jitter, looped = 0): #Base and Jitter both floats
        if looped:
            return ((base + (float(r.randint(-int(jitter * 100), 
                                             int(jitter * 100))) / 100)) % 1) + 0.01
        
        else:
            val =  (base + (float(r.randint(-int(jitter * 100), 
                                            int(jitter * 100))) / 100))
            
            if val > 1:
                return 1 - ((val % 1) + 0.01)
            if val < 0:
                return -val % 1
            return val



    def normal(base, jitter, looped = 0): #Base and Jitter both floats
        df = 100
        change = 0
        change += float(r.randint(1, 200))
        for i in range(0,df):
            change += float(r.randint(1, 200))
        change /= df + 1 # gets average (should be normal w mean of 100)
        change -= 100 # adjust for negatives to make mean 0
        change /= 20 # adjust standard dev

        print(change)

        change *= float(jitter) #since each jitter is only half

        
        if looped:
            return ((base + change) % 1) + 0.01
        else:
            val =  (base + change)
            if val > 1:
                return 1 - ((val % 1) + 0.01)
            if val < 0:
                return -val % 1
            return val
        
        


formulae = [Formulae.randomize, Formulae.normal]
formulaeNames = ["Random", "Normal"]



class Jitter():

    def __init__(self):
        self.base = [1.0, 1.0, 1.0]
        self.last_jitter = None
        
        self.val_jitter = 0.125
        self.hue_jitter = 0.125
        self.sat_jitter = 0.125

        self.jitter_formulas = [
            formulae[0],
            formulae[0],
            formulae[0],
        ]


    def setDistributions(self, newIndexes):
        #newIndexes contains a list of indices that correlate to positions in the formlae list respectively
        self.jitter_formulas = [formulae[newIndexes[0]], #H
                                formulae[newIndexes[1]], #S
                                formulae[newIndexes[2]]] #V

    def setRanges(self, newRanges):
        self.hue_jitter = newRanges[0]
        self.sat_jitter = newRanges[1]
        self.val_jitter = newRanges[2]


    def resetColor(self):
        
        depth = Krita.instance().activeDocument().colorDepth()

        as_rgb = cs.hsv_to_rgb(self.base[0], self.base[1], self.base[2])

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        comp = [blue, green, red, 1]
        managed_color.setComponents(comp)

        return managed_color
    
    def isUninterupted(self, newColor):
        match = True

        for x in range(0, 3):
            match = match and self.last_jitter[x] == newColor[x]

        return match
    

    def newColor(self, current_color): #Takes in a QColor

        if self.last_jitter == None and not current_color == None or \
            (abs(current_color.hsvHueF() - self.last_jitter[0]) > (NEW_COLOR_THRESHHOLD) or
            abs(current_color.saturationF() - self.last_jitter[1]) > (NEW_COLOR_THRESHHOLD) or
            abs(current_color.valueF() - self.last_jitter[2]) > (NEW_COLOR_THRESHHOLD)): #detects when a new color is selected...
            
            print(current_color.hsvHueF())
            print(current_color.saturationF())
            print(current_color.valueF())
            print(self.last_jitter)
            print("Detected Color Switch")
            self.setBase(current_color)

        depth = Krita.instance().activeDocument().colorDepth()

        self.last_jitter = [self.jitter_formulas[0](self.base[0], self.hue_jitter / 2),
                            self.jitter_formulas[1](self.base[1], self.sat_jitter / 2),
                            self.jitter_formulas[2](self.base[2], self.val_jitter / 2)]
                
        as_rgb = cs.hsv_to_rgb(self.last_jitter[0], self.last_jitter[1], self.last_jitter[2])

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        comp = [blue, green, red, 1]
        managed_color.setComponents(comp)

            

        return managed_color



    def setBase(self, color): #Takes in a QColor
        self.base[0] = color.hsvHueF()
        self.base[1] = color.saturationF()
        self.base[2] = color.valueF()
        self.last_jitter = self.base

