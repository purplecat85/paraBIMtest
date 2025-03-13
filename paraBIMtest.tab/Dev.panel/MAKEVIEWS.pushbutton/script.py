# -*- coding: utf-8 -*-
__title__   = "MAKE VIEWS"
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
from Autodesk.Revit.DB import * #Import everything from Autodesk.Revit.DB

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

import rpw
from rpw import db, ui  # Import necessary components from rpw

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
DEFAULT_CROP = '0.75'  # About 9"

# Validate + Filter Selection
selection = rpw.ui.Selection()
selected_rooms = [e for e in selection.get_elements(wrapped=False) if isinstance(e, Room)]

if not selected_rooms:
    ui.forms.Alert('MakeViews', 'You need to select at lest one Room.')

# Get View Types and Prompt User
plan_types = db.Collector(of_class='ViewFamilyType', is_type=True).wrapped_elements

# Filter all view types that are FloorPlan or CeilingPlan
plan_types_options = {t.name: t for t in plan_types
                      if t.view_family.name in ('FloorPlan', 'CeilingPlan')}

plan_type = ui.forms.SelectFromList('MakeViews', plan_types_options, description='Select View Type')
view_type_id = plan_type.Id

crop_offset = ui.forms.TextInput('MakeViews', default=DEFAULT_CROP, description='View Crop Offset [feet]')

crop_offset = float(crop_offset)


def offset_bbox(bbox, offset):
    """
    Offset Bounding Box by given offset
    http://archi-lab.net/create-view-by-room-with-dynamo/
    """
    bboxMinX = bbox.Min.X - offset
    bboxMinY = bbox.Min.Y - offset
    bboxMinZ = bbox.Min.Z - offset
    bboxMaxX = bbox.Max.X + offset
    bboxMaxY = bbox.Max.Y + offset
    bboxMaxZ = bbox.Max.Z + offset
    newBbox = DB.BoundingBoxXYZ()
    newBbox.Min = DB.XYZ(bboxMinX, bboxMinY, bboxMinZ)
    newBbox.Max = DB.XYZ(bboxMaxX, bboxMaxY, bboxMaxZ)
    return newBbox


@rpw.db.Transaction.ensure('Create View')
def create_plan(new_view, view_type_id, cropbox_visible=False, remove_underlay=True):
    """Create a Drafting View"""

    view_type_id
    name = new_view.name
    bbox = new_view.bbox
    level_id = new_view.level_id

    viewplan = DB.ViewPlan.Create(doc, view_type_id, level_id)
    viewplan.CropBoxActive = True
    viewplan.CropBoxVisible = cropbox_visible
    if remove_underlay and revit.version.year == '2015':
        underlay_param = viewplan.get_Parameter(DB.BuiltInParameter.VIEW_UNDERLAY_ID)
        underlay_param.Set(DB.ElementId.InvalidElementId)
    viewplan.CropBox = bbox

    counter = 1
    while True:
        # Auto Increment Room Number
        try:
            viewplan.Name = name
        except Exception:
            try:
                viewplan.Name = '{} - Copy {}'.format(name, counter)
            except Exception as errmsg:
                counter += 1
                if counter > 100:
                    raise Exception('Exceeded Maximum Loop')
            else:
                break
        else:
            break
    return viewplan

NewView = namedtuple('NewView', ['name', 'bbox', 'level_id'])
new_views = []

for room in selected_rooms:
        room = db.Element(room)
        room_level_id = room.Level.Id
        room_name = room.parameters['Name'].value
        room_number = room.parameters['Number'].value

        new_room_name = '{} {}'.format(room_name, room_number)
        room_bbox = room.get_BoundingBox(doc.ActiveView)
        new_bbox = offset_bbox(room_bbox, crop_offset)

        view_name = '{} - {}'.format(room.Level.Name, new_room_name)
        new_view = NewView(name=view_name, bbox=new_bbox, level_id=room_level_id)
        new_views.append(new_view)

for new_view in new_views:
    view = create_plan(new_view= new_view, view_type_id=view_type_id)