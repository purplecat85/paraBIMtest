import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.DB import FilteredElementCollector, Wall, Line, XYZ, Transaction

# Get the current document
doc = DocumentManager.Instance.CurrentDBDocument

# Define the tolerance for off-axis detection
tolerance = 0.1  # degrees

# Function to check if a line is off-axis
def is_off_axis(line):
    angle = line.Direction.AngleTo(XYZ.BasisX) * (180.0 / 3.141592653589793)  # Convert to degrees
    return abs(angle) > tolerance and abs(angle - 90) > tolerance

# Start a transaction to modify the document
t = Transaction(doc, "Fix Off-Axis Walls")
t.Start()

# Collect all walls in the document
walls = FilteredElementCollector(doc).OfClass(Wall).ToElements()

# Loop through each wall and check its orientation
for wall in walls:
    location_curve = wall.Location.Curve
    if isinstance(location_curve, Line):
        if is_off_axis(location_curve):
            # Calculate the new direction to align the wall
            new_direction = XYZ.BasisX if abs(location_curve.Direction.AngleTo(XYZ.BasisX)) < abs(location_curve.Direction.AngleTo(XYZ.BasisY)) else XYZ.BasisY
            # Move the wall to align it
            wall.Location.Move(new_direction * 0.01)  # Move slightly to correct

# Commit the transaction
t.Commit()