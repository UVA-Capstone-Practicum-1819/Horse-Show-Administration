from labels.sheet import Sheet
from labels.specifications import Specification
from reportlab.graphics import shapes
from .models import *


# Create an A4 portrait (215.9mm x 279.4mm, or 8.5 x 11 in) sheets with 3 columns and 10 rows of
# labels. Each label is 66.675mm x 25.4mm. The margins are
# automatically calculated between labels, top and bottom margins are 0.5 inches/12.7mm.
specs = Specification(215.9, 279.4, 3, 10, 66.675, 25.4, bottom_margin=12.7, top_margin=12.7)

# function to draw each label. This will be given the ReportLab drawing
# object to draw on, the dimensions (NB. these will be in points, the unit
# ReportLab uses) of the label, and the object to render.
def draw_label(label, width, height, obj):
    # converts each part to a string and adds separately so that everything is done on separate lines
    text = str(obj).split('\n')
    label.add(shapes.String(20, 50, text[0], fontName="Helvetica", fontSize=10))
    label.add(shapes.String(20, 35, text[1], fontName="Helvetica", fontSize=10))
    label.add(shapes.String(20, 20, text[2], fontName="Helvetica", fontSize=10))


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
		info = str(combo.num) + " - " + combo.horse.name + " \n" + combo.rider.first_name +" "+combo.rider.last_name+ " \n" + ', '.join(string_classes)
		# remove default border drawing of labels
		sheet.border = False
		# add label to sheet
		sheet.add_label(info)
		# save to static/labels folder
		sheet.save("show/static/labels/"+str(show_date)+'.pdf')

