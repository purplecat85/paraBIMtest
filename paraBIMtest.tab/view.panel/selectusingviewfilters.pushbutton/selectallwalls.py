# -*- coding: utf-8 -*-
__title__   = "Button 3"
__doc__     = """Version = 1.0"""

from Autodesk.Revit.DB import *
import clr
clr.AddReference('System')
from System.Collections.Generic import List

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.ApplicationServices import Application

app    = __revit__.Application  # type:Application
uidoc  = __revit__.ActiveUIDocument  # type:UIDocument
doc    = __revit__.ActiveUIDocument.Document  # type:Document

# Get the active view
active_view = doc.ActiveView

# Filter walls in the active view
wall_filter = ElementCategoryFilter(BuiltInCategory.OST_Walls)
walls_in_view = FilteredElementCollector(doc, active_view.Id).WherePasses(wall_filter).ToElements()

# Get View Filters applied to the current view
view_filters = active_view.GetFilters()  # Returns a list of filter ElementIds

# Get only the Parameter Filters (since some may be Graphic Overrides)
param_filters = [doc.GetElement(f) for f in view_filters if isinstance(doc.GetElement(f), ParameterFilterElement)]

# Set to store hidden element IDs
hidden_wall_ids = set()

# Check which elements are hidden by these filters
for param_filter in param_filters:
    if not active_view.GetFilterVisibility(param_filter.Id):  # Check if filter is hiding elements
        filter_rules = param_filter.GetElementFilter()  # Get the actual filter rules
        if filter_rules:  # Ensure there are rules before proceeding
            for wall in walls_in_view:
                if filter_rules.PassesFilter(wall):  # If the wall matches the filter, it is hidden
                    hidden_wall_ids.add(wall.Id)

# Select only visible walls (not hidden by filters)
visible_walls = [wall for wall in walls_in_view if wall.Id not in hidden_wall_ids]

# Select walls in the view
if visible_walls:
    wall_ids = List[ElementId]([wall.Id for wall in visible_walls])  # Convert list to ICollection[ElementId]
    uidoc.Selection.SetElementIds(wall_ids)
    print("Selected {} visible walls.".format(len(visible_walls)))  
else:
    print("No visible walls found in the active view.")
