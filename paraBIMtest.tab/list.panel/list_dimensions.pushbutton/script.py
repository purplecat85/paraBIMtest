# -*- coding: utf-8 -*-
__title__   = "Button 3"
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

# IMPORT
#==================================================
from Autodesk.Revit.DB import *

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

# MAIN
#==================================================
# Import necessary modules
from pyrevit import forms
from pyrevit import revit, DB

# Function to get all dimension types in the project
def get_all_dimension_types():
    # Create a set to store unique dimension types
    dimension_types = set()
    
    # Collect all dimension types in the document
    collector = DB.FilteredElementCollector(revit.doc)
    dimension_type_collector = collector.OfClass(DB.DimensionType).ToElements()
    
    # Loop through each dimension type and add its name to the set
    for dimension_type in dimension_type_collector:
        dimension_types.add(dimension_type.Name)
    
    return dimension_types

# Get all dimension types used in the project
dimension_types = get_all_dimension_types()

# Display the results
if dimension_types:
    forms.alert("Dimension Types in the project:\n" + "\n".join(dimension_types))
else:
    forms.alert("No dimension types found in the project.")