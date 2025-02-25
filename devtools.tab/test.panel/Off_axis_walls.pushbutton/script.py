# -*- coding: utf-8 -*-
__title__   = "Off_axis_walls"
__doc__     = """Version = Try 1.0
Date    = 02.12.2024
________________________________________________________________
Author: """

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================

#.NET Imports
import clr
import math
clr.AddReference('System')
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application

# ╦  ╦╔═╗╦═╗╦╔═╗╔╗ ╦  ╔═╗╔═╗
# ╚╗╔╝╠═╣╠╦╝║╠═╣╠╩╗║  ║╣ ╚═╗
#  ╚╝ ╩ ╩╩╚═╩╩ ╩╚═╝╩═╝╚═╝╚═╝
#==================================================
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document


# ╔╦╗╔═╗╦╔╗╔
# ║║║╠═╣║║║║
# ╩ ╩╩ ╩╩╝╚╝
#==================================================
# Define maximum allowable offset for alignment
max_distance = 0.0001


# Function to align an off-axis element
def align_off_axis_element(element, curve):
    direction = (curve.GetEndPoint(1) - curve.GetEndPoint(0)).Normalize()
    horizontal_distance = direction.DotProduct(XYZ.BasisY)
    vertical_distance = direction.DotProduct(XYZ.BasisX)
    angle = 0

    # Check alignment with horizontal (Y-axis)
    if abs(horizontal_distance) < max_distance:
        vector = direction if direction.X >= 0 else direction.Negate()
        angle = math.asin(-vector.Y)

    # Check alignment with vertical (X-axis)
    if abs(vertical_distance) < max_distance:
        vector = direction if direction.Y >= 0 else direction.Negate()
        angle = math.asin(vector.X)

    # Rotate the element if an angle adjustment is needed
    if angle != 0:
        # Define the rotation axis
        rotation_axis = Line.CreateBound(curve.GetEndPoint(0), curve.GetEndPoint(0) + XYZ.BasisZ)
        try:
         ElementTransformUtils.RotateElement(doc, element.Id, rotation_axis, angle)
         return True
        except Exception as e:
         print("Failed to rotate element {}: {}".format(element.Id, e))
         return False
    return False


# Start a transaction to modify the document
t = Transaction(doc, "Off_axis_walls")
t.Start()

# Counters for the number of aligned elements
aligned_walls_count = 0

# Collect walls to align
walls_to_align = FilteredElementCollector(doc).OfClass(Wall).ToElements()

# Align off-axis walls
for wall in walls_to_align:
    # Get the wall location line (curve)
    location = wall.Location
    if isinstance(location, LocationCurve):
        curve = location.Curve
        if align_off_axis_element(wall, curve):
            aligned_walls_count += 1

# Commit the transaction
t.Commit()

# Print the result using .format() method for compatibility
print("{} walls were aligned.".format(aligned_walls_count))