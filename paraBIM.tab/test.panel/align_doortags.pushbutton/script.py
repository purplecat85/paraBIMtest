# -*- coding: utf-8 -*-
__title__   = "Door tags"

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from pyrevit import forms
from pyrevit import revit, DB

#.NET Imports
import clr
clr.AddReference('System')

from System.Collections.Generic import List

# VARIABLES
#==================================================
from pyrevit import forms, script
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, XYZ, Transaction

app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# MAIN
#==================================================
# Function to move door tags to the center of the door panels
def move_door_tags_to_center():
    # Start a transaction to modify the Revit document
    t = Transaction(doc, "Move Door Tags to Center")
    t.Start()

    # Filter to collect all door elements
    door_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType()

    # Iterate through each door
    for door in door_collector:
        # Get the door's bounding box
        bounding_box = door.get_BoundingBox(None)
        if bounding_box:
            # Calculate the center of the door panel
            center_x = (bounding_box.Min.X + bounding_box.Max.X) / 2
            center_y = (bounding_box.Min.Y + bounding_box.Max.Y) / 2

            # Create a new point at the center of the door panel
            center_point = XYZ(center_x, center_y, door.Location.Point.Z)

            # Find the door tag associated with the door
            door_tags = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType()
            for tag in door_tags:
                # Check if the tag is associated with the current door
                if tag.TaggedElementId.IntegerValue == door.Id.IntegerValue:
                    # Move the door tag to the center point
                    tag.Location.Move(center_point - tag.Location.Point)
                    break

    # Commit the transaction
    t.Commit()

# Run the function
move_door_tags_to_center()