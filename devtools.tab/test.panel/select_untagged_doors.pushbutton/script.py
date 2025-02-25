# -*- coding: utf-8 -*-
__title__   = "Select untagged doors"


# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List


# VARIABLES
#==================================================
app    = __revit__.Application
uidoc  = __revit__.ActiveUIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

#📦Variables
active_view = doc.ActiveView
doc = __revit__.ActiveUIDocument.Document

#👉 Collect Doors and Tags in View
all_doors = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_Doors).WhereElementIsNotElementType()
all_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType()

#🔎 Check Tagged Doors
tagged_door_ids = [tag.GetTaggedLocalElements()[0].Id for tag in all_tags]
untagged_doors  = [door.Id for door in all_doors if door.Id not in tagged_door_ids]

#👀 Preview Results
print('Doors in View   : {}'.format(len(all_doors)))
print('DoorTags in View: {}'.format(len(all_tags)))
print('Tagged Doors    : {}'.format(len(tagged_door_ids)))
print('Untagged Doors  : {}'.format(len(untagged_doors)))

#🪄 Select Untagged Doors in View
from System.Collections.Generic import List
uidoc.Selection.SetElementIds(List[ElementId](untagged_doors))
#==================================================
#🚫 DELETE BELOW
from Snippets._customprint import kit_button_clicked    # Import Reusable Function from 'lib/Snippets/_customprint.py'
kit_button_clicked(btn_name=__title__)                  # Display Default Print Message
