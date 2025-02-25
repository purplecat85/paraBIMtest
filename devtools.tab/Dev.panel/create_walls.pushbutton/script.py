# -*- coding: utf-8 -*-
__title__   = "createwalls"
__doc__     = """Version = 1.0
Date    = 11.02.2025
________________________________________________________________
Description:

create walls with input coordinates
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
Author: Nimisha Gupta"""

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# VARIABLES
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

#MAIN
# Function to create a wall
def create_wall(start_point, end_point):
    # Retrieve the default wall type
    wall_type = FilteredElementCollector(doc).OfClass(WallType).FirstElement()
    
    # Create a line from the start and end points
    line = Line.CreateBound(start_point, end_point)
    
    # Create the wall
    Wall.Create(doc, line, wall_type.Id, False)