# import urllib.request, json
# import sys
#! /usr/bin/python
import os
import pdfrw
from pdfrw import PdfReader, PdfWriter

INVOICE_TEMPLATE_PATH = 'VHSA_Results_2015.pdf'
INVOICE_OUTPUT_PATH = 'VHSA_Final_Results.pdf'
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):
    template_pdf = pdfrw.PdfReader(input_pdf_path) #reads the file from the input_pdf_path that was passed in
    annotations = template_pdf.pages[1][ANNOT_KEY] #populating data onto the second page of the pdf 
    for annotation in annotations:
        if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
            if annotation[ANNOT_FIELD_KEY]:
                key = annotation[ANNOT_FIELD_KEY][1:-1]
                if key in data_dict.keys():
                    annotation.update(
                        pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                    )
    pdfrw.PdfWriter().write(output_pdf_path, template_pdf) #populates the fields of the pdf with the corresponding data from data_dict and writes it to the output_pdf_path that was passed in
    data_dict = {
   'show': '11/7/2018',
   'judge': 'Bertha',
    } #hardcoded info to populate the pdf's "show" and 'judge' fields
if __name__ == '__main__':
    write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict)
