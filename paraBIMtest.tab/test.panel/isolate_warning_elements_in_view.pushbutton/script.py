# -*- coding: utf-8 -*-
__title__   = "ISOLATE WARNING"
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

from tkinter.tix import DirSelectBox

# ╦╔╦╗╔═╗╔═╗╦═╗╔╦╗╔═╗
# ║║║║╠═╝║ ║╠╦╝ ║ ╚═╗
# ╩╩ ╩╩  ╚═╝╩╚═ ╩ ╚═╝
#==================================================
from Autodesk.Revit.DB import *

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
# Function to isolate warning elements in the active view
def isolate_warning_elements(doc):
    # Get the active view
    active_view = doc.ActiveView

    if active_view is None:
        TaskDialog.Show("Error", "No active view found.")
        return

    # Collect all elements in the active view
    collector = FilteredElementCollector(doc, active_view.Id)
    all_elements = collector.ToElements()

    # List to hold elements with warnings
    warning_elements = []

    # Check each element for warnings
    for element in all_elements:
        warnings = element.GetWarnings()
        if warnings and len(warnings) > 0:
            warning_elements.append(element)

    # If there are warning elements, isolate them
    if warning_elements:
        # Create a list of element IDs to isolate
        element_ids = [element.Id for element in warning_elements]

        # Start a transaction to isolate elements
        with Transaction(doc, "Isolate Warning Elements") as t:
            t.Start()
            active_view.IsolateElementsTemporary(element_ids)
            t.Commit()

        # Inform the user
        TaskDialog.Show("Isolation Complete", "Isolated {} elements with warnings.".format(len(warning_elements)))
    else:
        TaskDialog.Show("No Warnings", "There are no elements with warnings in the active view.")


# Entry point for the script
if __name__ == "__main__":
    # Get the current document
    doc = __revit__.ActiveUIDocument.Document
    isolate_warning_elements(doc)

#==================================================
#🚫 DELETE BELOW
from Snippets._customprint import kit_button_clicked    # Import Reusable Function from 'lib/Snippets/_customprint.py'
kit_button_clicked(btn_name=__title__)                  # Display Default Print Message
