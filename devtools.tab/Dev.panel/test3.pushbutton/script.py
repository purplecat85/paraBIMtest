# -*- coding: utf-8 -*-
__title__   = "Test"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

This is the placeholder for a .pushbutton
You can use it to start your pyRevit Add-In

________________________________________________________________
How-To:

1. [Hold ALT + CLICK] on the button to open its source folder.
You will be able to override this placeholder.

2. Automate Your Boring Work ;)

________________________________________________________________
TODO:
[FEATURE] - Describe Your ToDo Tasks Here
________________________________________________________________
Last Updates:
- [15.06.2024] v1.0 Change Description
- [10.06.2024] v0.5 Change Description
- [05.06.2024] v0.1 Change Description 
________________________________________________________________
Author: Erik Frits"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
# from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction

#.NET Imports
import clr

#from lib.Samples.ViewsSheets import trans

clr.AddReference('System')
from System.Collections.Generic import List

#from pyrevit import script
from pyrevit import forms, revit, script

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================

# Collect all window elements in the project
windows = FilteredElementCollector(doc, view.Id).OfCategory(BuiltInCategory.OST_Windows).WhereElementIsNotElementType().ToElementIds()
view = '1-100 VILLA 151 - GARDEN LEVEL'
# Define highlight color
ogs = OverrideGraphicSettings()
ogs.SetProjectionLineColor(Color(255, 0, 0))  # Red color

# Apply override
with Transaction(doc, "Highlight Windows") as t:
    t.Start()
    for window_id in windows:
        view.SetElementOverrides(window_id, ogs)
    t.Commit()
#==================================================
