# -*- coding: utf-8 -*-
__title__   = "test 1"
__doc__     = """Version = 1.0
Date    = 08.01.2025
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
from Autodesk.Revit.DB import WorksetTable

#.NET Imports
import clr

clr.AddReference('System')
from System.Collections.Generic import List


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

#==================================================
"""Finds and lists rooms with identical numbers."""
from collections import Counter

from pyrevit import revit, DB
from pyrevit import script

output = script.get_output()

if revit.active_view:
    rooms = DB.FilteredElementCollector(revit.doc, revit.active_view.Id)\
            .OfCategory(DB.BuiltInCategory.OST_Rooms)\
            .WhereElementIsNotElementType()\
            .ToElementIds()

    room_numbers = [revit.doc.GetElement(room_id).Number for room_id in rooms]
    duplicates = \
        [item for item, count in Counter(room_numbers).items() if count > 1]

    if duplicates:
        for room_number in duplicates:
            print('IDENTICAL ROOM NUMBER:  {}'.format(room_number))
            for room_id in rooms:
                rm = revit.doc.GetElement(room_id)
                if rm.Number == room_number:
                    room_name = \
                        rm.Parameter[DB.BuiltInParameter.ROOM_NAME].AsString()
                    print('\t{} (@ {}) {}'.format(room_name.ljust(30),
                                                  rm.Level.Name,
                                                  output.linkify(rm.Id)))
            print('\n')
    else:
        print('No identical room numbers were found.')
