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

# Import Revit API
from Autodesk.Revit.DB import (
    FilteredElementCollector,
    BuiltInCategory,
    Transaction,
    WorksetTable,
    WorksetId,
    BuiltInParameter
)
from pyrevit import forms

# .NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Collect all grids in the document
grids = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).ToElements()

# Specify the target workset name
TARGET_WORKSET_NAME = "Shared Levels and Grids"  # Change this to your desired workset name

# Access the WorksetTable to retrieve all worksets
workset_table = doc.GetWorksetTable()

# Get all user worksets (user-created worksets)
all_worksets = list(workset_table.GetWorksets(WorksetKind.UserWorkset))

# Check if the target workset exists
target_workset = None
for workset in all_worksets:
    if workset.Name == TARGET_WORKSET_NAME:
        target_workset = workset
        break

if target_workset:
    print("Workset '{}' found with ID: {}".format(TARGET_WORKSET_NAME, target_workset.Id))
else:
    print("Workset '{}' not found. Please create it first.".format(TARGET_WORKSET_NAME))