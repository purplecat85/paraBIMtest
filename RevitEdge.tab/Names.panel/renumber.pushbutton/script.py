# -*- coding: utf-8 -*-
__title__   = "renumber"
__doc__     = """Version = 1.0
Date    = 13.01.2025
________________________________________________________________
Description:

renumbers selected text boxes in the sequnce they are created

________________________________________________________________
How-To:

1. select text boxes
2. click button

________________________________________________________________
Last Updates:
- [15.06.2024] v1.0 completed
________________________________________________________________
Author: Nimisha Gupta"""

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr
clr.AddReference('System')
from System.Collections.Generic import List

# Import necessary Revit and PyRevit modules
from Autodesk.Revit.DB import FilteredElementCollector, TextNote
from Autodesk.Revit.UI import TaskDialog
from pyrevit import forms, revit, script

# VARIABLES
#==================================================
from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application
app    = __revit__.Application #type:Application
uidoc  = __revit__.ActiveUIDocument #type:UIDocument
doc    = __revit__.ActiveUIDocument.Document #type:Document

# MAIN
#==================================================
# Get the selected elements in the Revit document
selected_elements = revit.get_selection()

# Filter the selected elements to keep only TextNotes
text_notes = [elem for elem in selected_elements if isinstance(elem, TextNote)]

# Check if there are any selected text notes
if not text_notes:
    forms.alert("No text notes selected. Please select text notes to renumber.", title="No Selection")
else:
    # Renumber the selected text notes
    for index, text_note in enumerate(text_notes, start=1):
        # Start a transaction to modify the Revit document
        with revit.Transaction('Renumber Text Notes'):

#note value
            text_note.Text = str(index)

    # Display a success message
    #forms.alert("Text notes have been renumbered.", title="Success")
print('Done')