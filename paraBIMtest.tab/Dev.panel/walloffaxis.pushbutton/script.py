# -*- coding: utf-8 -*-
__title__   = "wall_off_axis"
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


#...................................................... IMPORTS
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
#from System.Collections.Generic import List

# Import necessary modules
from pyrevit import forms
from pyrevit import revit, DB

#...................................................... VARIABLES
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

#...................................................... MAIN

#create a list  to hold wall types
wall_types = []

# Filter for wall types in the document
collector = DB.FilteredElementCollector(doc)
wall_types_collected = collector.OfClass(DB.WallType).ToElements()

# Loop through the collected wall types and add their names to the list
for wall_type in wall_types_collected:
    wall_types.append(wall_type.Name)

# Print the list of wall types
if wall_types:
    forms.alert('\n'.join(wall_types), title='Wall Types')
else:
    forms.alert('No wall types found.', title='Wall Types')