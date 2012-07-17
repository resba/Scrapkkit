#!/usr/bin/python
# Scrapkkit IRC Bot [https://www.github.com/resba/Scrapkkit]
# Built off of Sprokkit v0.1 [https://www.github.com/resba/Sprokkit]
# Script by Resba
# Version: 0.0.1-ALPHA
# 
# License: Do not remove this original copyright for fair use. 
# Give credit where credit is due!
# 
#
# NOTE: All commented lines of CODE are debug messages for when something goes wrong.
from mongokit import Document

class Quote(Document):
    use_schemaless = True
    structure = {
        'uid': int,
        'quote': str,
    }
    use_dot_notation = True