# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:53:54 2017

@author: Minghui GUAN
"""

import base64

with open("E:\VPN_Easy Connect\snap_t0045_p0036.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

print encoded_string