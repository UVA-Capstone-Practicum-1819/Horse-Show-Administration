from labels.sheet import Sheet
from labels.specifications import Specification
from reportlab.graphics import shapes
from .models import *


# Create an A4 portrait (210mm x 297mm) sheets with 2 columns and 8 rows of
# labels. Each label is 90mm x 25mm with a 2mm rounded corner. The margins are
# automatically calculated.
specs = Specification(215.9, 279.4, 3, 10, 66.675, 25.4, corner_radius=0)

# Create a function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # Just convert the object to a string and print this at the bottom left of
    # the label.
    text = str(obj).split('\n')
    label.add(shapes.String(20, 50, text[0], fontName="Helvetica", fontSize=15))
    label.add(shapes.String(20, 35, text[1], fontName="Helvetica", fontSize=15))
    label.add(shapes.String(20, 20, text[2], fontName="Helvetica", fontSize=15))


def generate_show_labels(show_date):
	show = Show.objects.get(date=show_date)
	combos = HorseRiderCombo.objects.filter(show=show)

	# Create the sheet.
	sheet = Sheet(specs, draw_label, border=True)
	for combo in combos: 
		classes = combo.classes.all()
		string_classes = []
		for c in classes: 
			string_classes.append(str(c.num))
		info = str(combo.num) + " - " + combo.horse.name + " \n" + combo.rider.name + " \n" + ', '.join(string_classes)
		# Add label
		sheet.add_label(info)
		sheet.save("show/static/labels/"+str(show_date)+'.pdf')

