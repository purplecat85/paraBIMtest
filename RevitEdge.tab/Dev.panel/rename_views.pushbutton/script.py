# -*- coding: utf-8 -*-
__title__   = "rename views"
__doc__     = """Version = 1.0
Date    = 10.12.2024
________________________________________________________________
Description:
Rename views in Revit using Find/Replace Logic.
________________________________________________________________
How-To:
-> Click on the Button
-> Select Views
-> Define Renaming Rules
-> Rename views
________________________________________________________________
Last Updates:
- [10.12.2024] v1.0 Release
________________________________________________________________
Author: Nimisha"""

import pyrevit.forms
# IMPORTS
#==================================================
from Autodesk.Revit.DB import *

#.NET Imports
import clr

from pyrevit.forms import select_views

#from lib.Samples.FilteredElementCollector import view_types
#from lib.Samples.Selection import selected_elements, selected_element_ids, el_id

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

# 1 Select Views

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

# 2A Define Renaming Rules
#prefix  = ''
#find    = 'Copy '
#replace = '0'
#suffix  = ''

#2B define renaming rules (UI form)
# https://revitpythonwrapper.readthedocs.io/en/latest/ui/forms.html #flexforms
from rpw.ui.forms import (FlexForm, Label, TextBox, Separator, Button)
components = [Label('Prefix:'),  TextBox('prefix'),
              Label('Find:'),    TextBox('find'),
              Label('Replace:'), TextBox('replace'),
              Label('Suffix'),   TextBox('suffix'),
              Separator(),       Button('Rename Views')]

form = FlexForm('Title', components)
form.show()

user_inputs = form.values
prefix = user_inputs['prefix']
find = user_inputs['find']
replace = user_inputs['replace']
suffix = user_inputs['suffix']

#Start transactions to make changes in project
t = Transaction(doc, 'NG-Rename Views')

t.Start()

for View in sel_views:

    #3 Create new View Name
    old_name = View.Name
    #new_name = old_name.replace(find, replace)
    new_name = prefix + old_name.replace(find, replace) + suffix

    #4 Rename Views (Ensure unique view name)
    for i in range(5):
     try:
        View.Name = new_name
        print('{} -> {}'.format(old_name, new_name))
        break
     except:
        new_name += '*'

t.Commit()

print('-'*50)
print('Done!')