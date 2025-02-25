# -*- coding: utf-8 -*-
__title__   = "line_styles"
__doc__     = """Version = 1.0
Date    = 10.02.2025
________________________________________________________________
Description:
list all line styles in the project
sort the list alphabetically
filter unused lines styles
print the list
________________________________________________________________
Author: Nimisha Gupta"""

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from pyrevit import forms, revit, DB
from pyrevit import script

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# VARIABLES
#==================================================
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# Get the current Revit document
doc = __revit__.ActiveUIDocument.Document


# MAIN
#==================================================



