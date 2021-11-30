#! /usr/bin/python

#
# Description:
# ================================================================
# Time-stamp: "2021-11-30 12:30:13 trottar"
# ================================================================
#
# Author:  Richard L. Trotta III <trotta@cua.edu>
#
# Copyright (c) trottar
#
import pandas as pd
import pdf2image
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
from PyQt5.QtWidgets import QProgressBar,QApplication
import os, sys

import tools

pd.set_option('display.max_colwidth', None)

def import_pdf(pdf,pbar,button):

    PATH = "../database/pdfs/"
    
    pdfDict = {}
    df = pd.DataFrame()

    if None != pdf:
    
        #initialize the counter that you will use later in your pdf extraction function
        i = 1

        # need to delete some unrequired files from our pdf files
        def delete_ppms():
            for file in os.listdir(PATH):
                if '.ppm' in file or '.DS_Store' in file:
                    try:
                        os.remove(PATH + file)
                    except FileNotFoundError:
                        pass

        # Extract text from PDF files. Here is the pdf_extract function.
        # First, it prints the name of each file from which the text is extracted.
        # Depending on the size of the document, extracting text may take some time.      
        def pdf_extract(file, i):
            delete_ppms()
            images = pdf2image.convert_from_path(PATH + file, output_folder=PATH)
            j = 0
            for file in sorted(os.listdir(PATH)):
                if '.ppm' in file and 'image' not in file:
                    #pbar.setMaximum(len(pdf_files))
                    #pbar.setValue(j)
                    #QApplication.processEvents() 
                    tools.progressBar(j, len(sorted(os.listdir(PATH)))-1)
                    os.rename(PATH + file, PATH + 'image' + str(i) + '-' + str(j) + '.ppm')
                    j += 1
            j = 0
            files = [f for f in os.listdir(PATH) if '.ppm' in f]

            text = ''
            for file in sorted(files, key=lambda x: int(x[x.index('-') + 1: x.index('.')])):
                text += pytesseract.image_to_string(Image.open(PATH + file))

            return text

        # use our function to extract from all the PDF files
        for i in range(len(pdf)):
            pdf_file = pdf[i]
            button.setText("Updating {} pdf data...".format(pdf_file))
            print("Importing data for pdf {}...".format(pdf_file))
            pdfDict.update({"title" : pdf_file.split('.pdf')[0]})
            pdfDict.update({"url" : pdf_file})
            pdfDict.update({"type" : "pdf"})
            with open('../database/log/database_titles.txt') as f:
                if pdf_file in f.read():
                    continue
            text = pdf_extract(pdf_file, i)
            pdfDict.update({"transcript" : ' '.join([line.strip().lower() for line in text.splitlines()])})
            pdfDict = {k : pdfDict[k] for k in sorted(pdfDict.keys())}
            df = df.append(pdfDict,ignore_index=True)
    print("-"*70)
    return df
