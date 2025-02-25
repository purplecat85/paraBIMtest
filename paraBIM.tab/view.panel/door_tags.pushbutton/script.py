# -*- coding: utf-8 -*-
__title__   = "door tags"
__doc__     = """Version = 1.0
Date    = 20.02.2025
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

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr



# from pyrevit import forms
# from pyrevit import select_views


clr.AddReference('System')
from System.Collections.Generic import List


#VARIABLES
#==================================================
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# MAIN
#==================================================
print("Script is running...")
# Get the active view from the document
active_view = doc.ActiveView  

# Get the active view
view = uidoc.ActiveView  # Ensure this is defined before using it

#  collect door tags in view
all_doors_in_view = FilteredElementCollector(doc, active_view.Id)\
                     .OfCategory(BuiltInCategory.OST_Doors)\
                     .WhereElementIsNotElementType()\
                     .ToElements()
all_tags_in_view = FilteredElementCollector(doc, active_view.Id)\
                  .OfCategory(BuiltInCategory.OST_DoorTags)\
                  .WhereElementIsNotElementType()\
                  .ToElements()

# # check tagged doors
tagged_doors_id = [tag.GetTaggedLocalElements()[0].Id for tag in all_tags_in_view]
untagged_doors = [d.Id for d in all_doors_in_view if d.Id not in tagged_doors_id]

# preview results

print('Doors in view:     {}'.format(len(list(all_doors_in_view))))
print("Door Tags in view: {}".format(len(list(all_tags_in_view))))
print("Tagged Doors:      {}".format(len(list(tagged_doors_id))))
print("Untagged Doors:    {}".format(len(list(untagged_doors))))

#==================================================

# Select untagged doors in view
import clr
clr.AddReference('System')
from System.Collections.Generic import List

uidoc.Selection.SetElementIds(List[ElementId](untagged_doors))


def find_untagged_doors(view):
    """Function to find untagged doors in the provided view"""

all_doors = FilteredElementCollector(doc, view.Id)\
.OfCategory(BuiltInCategory.OST_Doors)\
.WhereElementIsNotElementType()\
.ToElements()

all_tags = FilteredElementCollector(doc, view.Id)\
.OfCategory(BuiltInCategory.OST_DoorTags)\
.WhereElementIsNotElementType()\
.ToElements()

#check tagged doors
tagged_doors_id = [tag.GetTaggedLocalElements()[0].Id for tag in all_tags]
untagged_door_ids = [d.Id for d in all_doors if d.Id not in tagged_doors_id]
# return untagged_door_ids

#select views
from pyrevit import forms, script
selected_views = forms.select_views()


output     = script.get_output()
output.print_md('# Missing Tags Report:')

for view in selected_views:
    output.print_md('# Missing Tags Report:')

for view in selected_views: 
    output.print_md('---')
    linkify_view = output.linkify(view.Id, view.Name)
    door_ids_no_tags = find_untagged_doors(view)

    if door_ids_no_tags:
        output.print_md('### View: {} - Missing Tags'.format(linkify_view))
        for door_id in door_ids_no_tags:
            door = doc.GetElement(door_id)
            linkify_door = output.linkify(door_id, '{}[{}]'.format(door.Name, door.Id))

            print('No Tag Door: {}'.format(linkify_door))
else:
    output.print_md('### No missing tags on view: {}'.format(linkify_view))