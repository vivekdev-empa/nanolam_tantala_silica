# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 14:43:30 2025

@author: devi
"""

import py4DSTEM
import hyperspy.api as hs

# Load with HyperSpy
data = hs.load("G:/Analytik/Personal/Vivek/PC_Titan_EMPA/PED/20250317_PED_PJ3049_NI01/PJ3049_1645.blo")

# Save in py4DSTEM's preferred format
py4DSTEM.save("1645_file.h5", data.data)