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
    # reads the file from the input_pdf_path that was passed in
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for i in range(1, 22):
        # populating data onto the second page of the pdf
        annotations = template_pdf.pages[i][ANNOT_KEY]
        for annotation in annotations:
            # print(annotation)
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]

                    if key in data_dict.keys():
                        # print(key + ": " + data_dict[key])
                        annotation.update(
                            pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                        )
        # populates the fields of the pdf with the corresponding data from data_dict and writes it to the output_pdf_path that was passed in
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)


def read_pdf(input_pdf_path, page, key_index):
    # reads the file from the input_pdf_path that was passed in
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    # populating data onto the second page of the pdf
    annotations = template_pdf.pages[page-1][ANNOT_KEY]
    # for annotation in annotations:
    # print(annotation)
    if annotations[key_index][SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
        if annotations[key_index][ANNOT_FIELD_KEY]:
            key = annotations[key_index][ANNOT_FIELD_KEY][1:-1]
            return key


def read_written_pdf(input_pdf_path, data_dict, page, key_index):
    # reads the file from the input_pdf_path that was passed in
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    # populating data onto the second page of the pdf
    annotations = template_pdf.pages[page-1][ANNOT_KEY]
    # for annotation in annotations:
    # print(annotation)
    if annotations[key_index][SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
        if annotations[key_index][ANNOT_FIELD_KEY]:
            key = annotations[key_index][ANNOT_FIELD_KEY][1:-1]
            return pdfrw.PdfDict(V='{}'.format(data_dict[key]))["/V"]


if __name__ == '__main__':
    write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict)
    read_pdf(INVOICE_TEMPLATE_PATH, page, key_index)
    read_written_pdf(INVOICE_TEMPLATE_PATH, page, key_index)
