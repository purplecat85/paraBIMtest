# -*- coding: utf-8 -*-
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *
from System.Collections.Generic import List

# Initialize the Revit document
doc = __revit__.ActiveUIDocument.Document
active_view = doc.ActiveView

# Collect Doors and Tags in View
all_doors = FilteredElementCollector(doc, active_view.Id).OfCategory(
    BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
all_tags = FilteredElementCollector(doc, active_view.Id).OfCategory(
    BuiltInCategory.OST_DoorTags).WhereElementIsNotElementType().ToElements()

# Check Tagged Doors
tagged_door_ids = [tag.GetTaggedLocalElements()[0].Id for tag in all_tags]
untagged_doors = [door for door in all_doors if door.Id not in tagged_door_ids]

# Preview Results
print('Doors in View   : {}'.format(len(all_doors)))
print('DoorTags in View: {}'.format(len(all_tags)))
print('Tagged Doors    : {}'.format(len(tagged_door_ids)))
print('Untagged Doors  : {}'.format(len(untagged_doors)))

# Start a transaction to tag untagged doors
transaction = Transaction(doc, "Tag Untagged Doors")
transaction.Start()

for door in untagged_doors:
    # Create a new door tag
    door_tag_type = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_DoorTags).WhereElementIsElementType().FirstElement()

    if door_tag_type is not None:
        # Place the door tag
        tag = IndependentTag.Create(doc, active_view.Id, door.Id, XYZ(0, 0, 0), False, TagOrientation.Horizontal,
                                    door_tag_type.Id)

# Commit the transaction
transaction.Commit()

# Select Untagged Doors in View
uidoc = __revit__.ActiveUIDocument
uidoc.Selection.SetElementIds(List[ElementId]([door.Id for door in untagged_doors]))
#==================================================
#🚫 DELETE BELOW
from Snippets._customprint import kit_button_clicked    # Import Reusable Function from 'lib/Snippets/_customprint.py'
kit_button_clicked(btn_name=__title__)                  # Display Default Print Message
