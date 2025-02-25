from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, XYZ, Transaction, Reference, IndependentTag, TagMode, TagOrientation

# Get the current document
doc = __revit__.ActiveUIDocument.Document

# Get the active view
active_view = doc.ActiveView

# Collect all doors in the current view
doorFiltered = FilteredElementCollector(doc, active_view.Id) \
    .OfCategory(BuiltInCategory.OST_Doors) \
    .WhereElementIsNotElementType() \
    .ToElements()

# Initialize a list to store locations to avoid
avoid_locations = []

# Start a transaction for tagging doors
with Transaction(doc, 'Tag Doors') as tx:
    tx.Start()  # Start the transaction

    for door in doorFiltered:
        # Check if the door has a valid location
        if door.Location is None or door.Location.Point is None:
            print("Skipping door %s due to invalid location." % door.Id)
            continue  # Skip this door if it has no location

        door_location = door.Location.Point
        avoid_locations.append(XYZ(door_location.X, door_location.Y, door_location.Z))

        shift_point = XYZ(door_location.X, door_location.Y, door_location.Z)
        door_ref = Reference(door)

        # Create door tags
        tag_instance = IndependentTag.Create(doc, active_view.Id, door_ref, False, TagMode.TM_ADDBY_CATEGORY, TagOrientation.Horizontal, shift_point)
        tag_instance.ChangeTypeId(TagSymbols)

        # Get location of tag
        tag_bounding_box = tag_instance.get_BoundingBox(doc.GetElement(tag_instance.OwnerViewId))
        global_max = tag_bounding_box.Max
        global_min = tag_bounding_box.Min
        bounding_box_center = XYZ((global_max.X + global_min.X) / 2, (global_max.Y + global_min.Y) / 2, global_max.Z)
        tag_size = global_max.DistanceTo(global_min)

        # Find overlap
        required_distance = tag_size
        overlap_found = True
        counter = 1

        while overlap_found:
            spiral_points = list(shift(counter, (bounding_box_center.X, bounding_box_center.Y, bounding_box_center.Z)))
            new_point = spiral_points[-1]
            counter += 1

            test_point = XYZ(new_point[0], new_point[1], new_point[2])
            distances = [test_point.DistanceTo(loc) for loc in avoid_locations]

            move_vector = XYZ(new_point[0] - door_location.X, new_point[1] - door_location.Y, new_point[2] - door_location.Z)

            if any(distance < required_distance for distance in distances):
                continue

            if all(distance > required_distance for distance in distances):
                tag_instance.Location.Move(move_vector)

                new_tag_bounding_box = tag_instance.get_BoundingBox(doc.GetElement(tag_instance.OwnerViewId))
                new_global_max = new_tag_bounding_box.Max
                new_global_min = new_tag_bounding_box.Min
                new_bounding_box_center = XYZ((new_global_max.X + new_global_min.X) / 2, (new_global_max.Y + new_global_min.Y) / 2, new_global_max.Z)

                avoid_locations.append(new_bounding_box_center)
                print("Location found")
                overlap_found = False
                break
            else:
                print('No match')
                break

        # Add leader to the tag
        tag_instance.HasLeader = True
        tag_instance.LeaderElbow = XYZ(shift_point.X + 10, shift_point.Y, shift_point.Z)

# The transaction will automatically commit when exiting the 'with' block