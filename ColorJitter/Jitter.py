
'''
    This module is reserved for underlying funcitonality of the jittering that doesn't
    directly interface with Krita.
'''

from krita import (ManagedColor)

import colorsys as cs
import random as r
from enum import Enum


NEW_COLOR_THRESHHOLD = 0.05 # 5% change needed, too much error for exact recording




class Formulae(Enum):
    '''
        Formulae contains all methods of generating new colors.
        Each function takes three things: base, jitter, looped.
        base is the original color, jitter is half of the range, 
        and looped says whether or not the color should go back to zero
        if it overflows.
    '''
    RANDOM = 0,
    NORMAL = 1,
    LINEARPOSITIVE = 3,
    LINEARNEGATIVE = 4

    def randomize(base, jitter, looped = 0): #Base and Jitter both floats
        '''
            Generates a color randomly

            base: [hue, saturation, value]
            jitter: float
            looped: True/False, default Falses

            All colors within range are equally likely.
            Overflow bounces back into the range.

        '''
        if looped:
            return ((base + (float(r.randint(-int(jitter * 100), 
                                             int(jitter * 100))) / 100)) % 1) + 0.01
        
        else:
            val =  (base + (float(r.randint(-int(jitter * 100), 
                                            int(jitter * 100))) / 100))
            
            while val > 1:
                val = 1 - ((val % 1) + 0.01)
            while val < 0:
                val = -val % 1
            return val



    def normal(base, jitter, looped = 0): #Base and Jitter both floats
        '''
            Generates a normally distributed color
            
            base: [hue, saturation, value]
            jitter: float
            looped: True/False, default Falses

            Sample size of 101 averaged and ajusted to be roughly normally distributed
            (much more likely if near base)
            Overflow bounces back into the range.

        '''
        df = 100
        change = 0
        change += float(r.randint(1, 200))
        for i in range(0,df):
            change += float(r.randint(1, 200))
        change /= df + 1 # gets average (should be normal w mean of 100)
        change -= 100 # adjust for negatives to make mean 0
        change /= 20 # adjust standard dev

        change *= float(jitter) #since each jitter is only half

        
        if looped:
            return ((base + change) % 1) + 0.01
        else:
            val =  (base + change)
            while val > 1:
                val =  1 - ((val % 1) + 0.01)
            while val < 0:
                val = -val % 1
            return val
        
        

formulaeNames = ["Random", "Normal"]                # list of distribution options for the dropdown
formulae = [Formulae.randomize, Formulae.normal]    # list of functions in order of names




class Jitter():
    '''
        Jitter stores and manages the base color and jitter ranges. 
        set
    '''

    def __init__(self):
        self.base = [1.0, 1.0, 1.0] # should always be replaced, always a list of HSV
        self.last_jitter = None # should also always be replaced. Normally a QColor
        
        self.val_jitter = 0.5 # the default range for values
        self.hue_jitter = 0.5 # the default range for hues
        self.sat_jitter = 0.5 # the default range for saturation

        self.jitter_formulas = [
            formulae[0],
            formulae[0],
            formulae[0],
        ] # defaults for the formulas will always be the first element of formulae


    def setDistributions(self, newIndexes):
        '''
            newIndexes contains a list of indices that correlate to positions in the formlae list respectively
        '''
        self.jitter_formulas = [formulae[newIndexes[0]], #H
                                formulae[newIndexes[1]], #S
                                formulae[newIndexes[2]]] #V

    def setRanges(self, newRanges):
        '''
            newRanges contains a list of floats that correlate to the jitter ranges of H, S, and V
        '''
        self.hue_jitter = newRanges[0]
        self.sat_jitter = newRanges[1]
        self.val_jitter = newRanges[2]


    def resetColor(self):
        '''
            newRanges contains a list of floats that correlate to the jitter ranges of H, S, and V
        '''
        
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
    

    def newColor(self, current_color):
        '''
            returns a new color based on the current settings. 
            current_color is needed to detect if the user changed colors manually.

            currrent_color: QColor
        '''

        self.updateBase(current_color)

        # now really generating the new color

        depth = Krita.instance().activeDocument().colorDepth()

        self.last_jitter = [self.jitter_formulas[0](self.base[0], self.hue_jitter / 2, looped=True),
                            self.jitter_formulas[1](self.base[1], self.sat_jitter / 2),
                            self.jitter_formulas[2](self.base[2], self.val_jitter / 2)] # halved to account for above/below
                
        as_rgb = cs.hsv_to_rgb(self.last_jitter[0], self.last_jitter[1], self.last_jitter[2])

        managed_color = ManagedColor("RGBA", depth, "")
        comp = managed_color.components()
        red = as_rgb[0]
        green = as_rgb[1]
        blue = as_rgb[2]
        comp = [blue, green, red, 1]
        managed_color.setComponents(comp)

        self.last_jitter = managed_color.components()

            

        return managed_color
    
    def updateBase(self, current_color):
        '''
            checks if the base needs to be updated (if current_color doesn't match self.last_jitter)
            if it does need to be updated, it updates

            currrent_color: QColor
        '''

        if self.last_jitter == None and not current_color == None or \
            (abs(current_color.redF() - self.last_jitter[2]) > (NEW_COLOR_THRESHHOLD) or
            abs(current_color.greenF() - self.last_jitter[1]) > (NEW_COLOR_THRESHHOLD) or
            abs(current_color.blueF() - self.last_jitter[0]) > (NEW_COLOR_THRESHHOLD)): #detects when a new color is selected...
            
            print("Detected Color Switch")
            self.setBase(current_color)




    def setBase(self, color):
        '''
            updates the base to the given color. 
            Also records the given color over the last jitter so that it 
            doesn't infinitely say that it's a new color.

            color: QColor
        '''
        self.last_jitter = self.base
        color = color
        self.base[0] = color.hsvHueF()
        self.base[1] = color.saturationF()
        self.base[2] = color.valueF()

