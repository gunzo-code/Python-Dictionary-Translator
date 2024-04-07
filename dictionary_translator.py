from bs4 import BeautifulSoup
import json
import os
from glob import glob


def translate_webpage(inputfile, overwrite=True):
    # Use BeautifulSoup to read text in html
    soup = BeautifulSoup(open(inputfile, encoding='utf-8'), features='html.parser') 

    # Load dictionnary of phrases
    with open("dictionary_phrases.json", encoding="utf-8") as json_file:
        dictionnary_phrases = json.load(json_file)

    # Looping on all texts found
    for linetext in soup.findAll(string=True):
        # Translate with dictionnary phrases
        #if linetext.strip() != "":
            #print(linetext.strip())
        try:
            translatedText = dictionnary_phrases[linetext.strip()]
            linetext.replaceWith(translatedText)
        except KeyError:
            pass  

    # Load dictionnary of words
    with open("dictionary_words.json", encoding="utf-8") as json_file:
        dictionnary_words = json.load(json_file)

    # Translate with dictionnary words
    htmltext = str(soup)   
    for word_from, work_to in dictionnary_words.items():
        htmltext = htmltext.replace(word_from, work_to)

    # Saving translated html to disk
    if not overwrite:
        head, tail = os.path.splitext(inputfile)
        outputfile = head + "_translated" + tail
    else:
        outputfile = inputfile
    with open(outputfile, "w", encoding="utf-8") as file:
        file.write(htmltext)

def translate_folder_with_webpages(folder, recursive=True, overwrite=True):
    htmlfilemask = "*.html"

    if recursive:
        folder = htmlfolder + "/**/" + htmlfilemask
    else:
        folder = htmlfolder + "/" + htmlfilemask

    for filename in glob(folder, recursive=True):
        if "_translated." not in filename:
            translate_webpage(filename, overwrite)

htmlfolder = "../great_expectations/uncommitted/data_docs/"
translate_folder_with_webpages(htmlfolder, recursive=True, overwrite=False)