# -*- coding: utf-8 -*-
__title__   = "Grid workset"
__doc__     = """Version = 1.0
Date    = 15.06.2024
________________________________________________________________
Description:

This script selects all grids in the current Revit project and moves them to a specified workset.



________________________________________________________________
How-to:
1. Specify the target workset name in the `TARGET_WORKSET_NAME` variable.
2. Run the script.
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
# Import Revit API
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, Transaction, WorksetTable
from pyrevit import forms

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


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

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Define the target workset name
TARGET_WORKSET_NAME = "Shared Levels and Grids"  # Change this to your desired workset name

# Get all worksets in the project
workset_table = doc.GetWorksetTable()
all_worksets = workset_table.GetWorksets()

# Find the target workset
target_workset = None
for workset in all_worksets:
    if workset.Name == TARGET_WORKSET_NAME:
        target_workset = workset
        break

if not target_workset:
    forms.alert(f"Workset '{TARGET_WORKSET_NAME}' not found. Please create it and try again.")
    print(f"Workset '{TARGET_WORKSET_NAME}' not found.")
    exit()

# Get the ID of the target workset
target_workset_id = target_workset.Id

# Select all grids in the project
grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).ToElements()

if not grids:
    forms.alert("No grids found in the current project.")
    print("No grids found in the current project.")
    exit()

# Move grids to the target workset
with Transaction(doc, "Move Grids to Workset") as t:
    t.Start()
    for grid in grids:
        try:
            # Set the grid's workset parameter
            grid.LookupParameter("Workset").Set(target_workset_id.IntegerValue)
            print(f"Grid '{grid.Name}' moved to workset '{TARGET_WORKSET_NAME}'.")
        except Exception as e:
            print(f"Failed to move grid '{grid.Name}': {e}")
    t.Commit()

forms.alert(f"Successfully moved {len(grids)} grids to the workset '{TARGET_WORKSET_NAME}'.")
