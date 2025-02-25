# -*- coding: utf-8 -*-
__title__   = "View Filters"
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

# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr



from pyrevit import forms
from pyrevit.forms import select_views


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
# 01 Select views
# Get Views - Selected in ProjectBrowser
sel_el_ids = uidoc.Selection.GetElementIds()
sel_elem = [doc.GetElement(e_Id) for e_Id in sel_el_ids]
sel_views = [el for el in sel_elem if issubclass(type(el), View)]

#If None Selected - Prompt SelectViews from pyrevit.forms.select_view
if not sel_views:
    sel_views = pyrevit.forms.select_views()

# Ensure Views are Selected
if not sel_views:
    pyrevit.forms.alert('No Views Selected. Please Try Again', exitscript=True)



# # 1️⃣ Get Views From/To
# def get_view_by_name(view_name):
#     """Get Views by exact Name."""
#     views = FilteredElementCollector(doc).OfCategory(
#         BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()
#     dict_views = {view.Name: view for view in views}
#
#     if view_name not in dict_views:
#         print('Could not find view by name: {}'.format(view_name))
#     else:
#         return dict_views[view_name]
#
#
# view_from = get_view_by_name('1-100 VILLA #151 - GARDEN LEVEL')  # type: View
# view_to = get_view_by_name('1-100 VILLA #151 - UPPER LEVEL')  # type: View
#
# # 2️⃣ Get and Select View Filters
# filter_ids = view_from.GetOrderedFilters()
# filters = [doc.GetElement(f_id) for f_id in filter_ids]
#
# sel_filters = forms.SelectFromList.show(filters,
#                                         multiselect=True,
#                                         name_attr='Name',
#                                         button_name='Select View Filters')
#
# # ✅ Ensure Selected Filters
# if not sel_filters:
#     forms.alert("No View Filters were Selected.\n"
#                 "Please Try Again.", exitscript=True)
#
# # 3️⃣ Copy View Filters
# with Transaction(doc, 'Copy ViewFilters') as t:
#     t.Start()
#
#     for view_filter in filters:
#         # 🅰️ Copy Filter Overrides
#         overrides = view_from.GetFilterOverrides(view_filter.Id)
#         view_to.SetFilterOverrides(view_filter.Id, overrides)
#
#         # 🅱️ Copy Enable/Visibility Controls
#         visibility = view_from.GetFilterVisibility(view_filter.Id)
#         enable = view_from.GetIsFilterEnabled(view_filter.Id)
#
#         view_to.SetFilterVisibility(view_filter.Id, visibility)
#         view_to.SetIsFilterEnabled(view_filter.Id, enable)
#
#     t.Commit()
#
#
#
#
#
#
#
# #==================================================
