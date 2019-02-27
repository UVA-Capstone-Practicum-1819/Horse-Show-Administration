from sheet import Sheet
from specifications import Specification
from reportlab.graphics import shapes

# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = Specification(210, 297, 2, 8, 90, 25, corner_radius=2)

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    label.add(shapes.String(2, 2, str(obj), fontName="Helvetica", fontSize=11))

# Create the sheet.
sheet = Sheet(specs, draw_label, border=True)

# Add a couple of labels.
sheet.add_label("420: Sal\n Horsey \n 40, 20, 15")
sheet.add_label("World")

# We can also add each item from an iterable.
sheet.add_labels(range(3, 22))

# Note that any oversize label is automatically trimmed to prevent it messing up
# other labels.
sheet.add_label("Oversized label here")

# Save the file and we are done.
sheet.save('basic.pdf')
print("{0:d} label(s) output on {1:d} page(s).".format(sheet.label_count, sheet.page_count))