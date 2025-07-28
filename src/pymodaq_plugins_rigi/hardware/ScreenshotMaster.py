# -*- coding: utf-8 -*-
"""
Created on Mon Jul 28 2025

@author: dqml-lab
"""

import numpy as np
import cv2
import pyautogui


class ScreenshotMaster:

    ############## My methods

    def __init__(self) -> None:
        
        # Define region: (left, top, width, height)
        # region = (50, 55, 950, 700)
        self.region = (50, 55, 1260, 960)
        self.background = 10.082550805224868

    def __del__(self):
        print("Killing ScreenShotMaster")
        

    def start_a_grab_snap(self):
        screenshot = pyautogui.screenshot(region=self.region)
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        return gray

