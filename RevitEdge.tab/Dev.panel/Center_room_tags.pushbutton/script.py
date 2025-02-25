# -*- coding: utf-8 -*-
__title__   = "Room tag - Center"

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

# VARIABLES
#==================================================
doc   = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
app   = __revit__.Application

# ELEMENTS
all_room_tags = FilteredElementCollector(doc, doc.ActiveView.Id)\
    .OfCategory(BuiltInCategory.OST_RoomTags).WhereElementIsNotElementType().ToElements()

# CONTROLS
step = 2  # INTERNAL UNITS IN FEET


def center_room_tag(tag, new_pt):
    """Function to center the Room Tag Location."""
    tag.Location.Point = new_pt


def move_room_and_tag(tag, new_pt):
    """Function to move the Room Tag to a new point."""
    center_room_tag(tag, new_pt)


# MAIN
#==================================================
with Transaction(doc, __title__) as t:
    t.Start()

    for tag in all_room_tags:
        # ROOM DATA
        room = tag.Room
        if room:  # Check if room is not None
            room_boundaries = room.GetBoundarySegments(SpatialElementBoundaryOptions())
            if room_boundaries:
                # Calculate the center of the room based on boundaries
                total_x = 0
                total_y = 0
                count = 0

                for boundary in room_boundaries:
                    for segment in boundary:
                        curve = segment.GetCurve()
                        pt_start = curve.GetEndPoint(0)
                        pt_end = curve.GetEndPoint(1)

                        total_x += (pt_start.X + pt_end.X) / 2
                        total_y += (pt_start.Y + pt_end.Y) / 2
                        count += 1

                if count > 0:
                    room_center_x = total_x / count
                    room_center_y = total_y / count
                    room_center_z = 0  # Assuming you want to place it at Z = 0

                    room_center = XYZ(room_center_x, room_center_y, room_center_z)

                    # Move the tag to the calculated center
                    move_room_and_tag(tag, room_center)

    t.Commit()