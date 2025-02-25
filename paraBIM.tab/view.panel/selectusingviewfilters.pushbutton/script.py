# -*- coding: utf-8 -*-
__title__   = "workset_walls"
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
________________________________________________________________
Author: Nimisha"""

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List
from pyrevit import forms, script


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
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, ElementId
from Autodesk.Revit.UI import UIDocument
from System.Collections.Generic import List

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Get the active view
active_view = doc.ActiveView

# Create a filter for elements visible in the active view
visible_filter = VisibleInViewFilter(doc, active_view.Id)

# Collect all wall instances
#all_walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()

# Collect wall instances visible in the active view
walls_in_view = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().WherePasses(visible_filter).ToElements()

all_walls = walls_in_view

# Ask user for the correct workset name
workset_name = forms.ask_for_string(
    title="Workset Check",
    prompt="Enter the correct workset name:",
    default=""
)
# Filter walls that are not on the correct workset
correct_workset = workset_name

wrong_walls_ids = [wall.Id for wall in all_walls if wall.LookupParameter("Workset").AsValueString() != correct_workset]

# Convert to List[ElementId]
List_el_ids = List[ElementId](wrong_walls_ids)

# Select elements in Revit UI
uidoc.Selection.SetElementIds(List_el_ids)
