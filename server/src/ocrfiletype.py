import os
import fileinput
from document import real_directory
from document import path_join
import json


def test(collection, document):
    return {"key": 'hello' + ' ' + collection + ' ' + document}


def logOcrFileTypeDetails(collection, document, ocrOutputResult, identificationOutputResult,
                          identificationBoundaryOutputResult, extractionOutputResult, fileType, lossType, comments):
    path = path_join(real_directory(collection), 'qafunnelocrfiledetails')
    if not os.path.exists(path):
        os.mknod(path)

    searchFlag = False

    for line in fileinput.input(path, inplace=True):
        loaded_r = json.loads(line)
        docname = str(loaded_r['document'])

        if docname == document:
            searchFlag = True
            print "%s" % (
                json.dumps({"document": document, "ocrOutputResult": ocrOutputResult, "identificationOutputResult": identificationOutputResult,
                            "identificationBoundaryOutputResult": identificationBoundaryOutputResult, "extractionOutputResult": extractionOutputResult, "fileType": fileType, "lossType": lossType, "comments": comments}) + '\n'),
        else:
            print "%s" % (line),

    fileinput.close()

    if not searchFlag:
        with open(path, 'a') as file:
            file.write(json.dumps(
                {"document": document, "ocrOutputResult": ocrOutputResult,"identificationOutputResult": identificationOutputResult,
                             "identificationBoundaryOutputResult": identificationBoundaryOutputResult, "extractionOutputResult": extractionOutputResult, "fileType": fileType, "lossType": lossType, "comments": comments}) + '\n')
            file.close

    return {"status": 'true'}


def getOcrFileTypeDetails(collection, document):
    path = path_join(real_directory(collection), 'qafunnelocrfiledetails')

    returnMap = {"status": False}

    for line in fileinput.input(path, inplace=False):
        loaded_r = json.loads(line)
        docname = str(loaded_r['document'])

        if docname == document:
            returnMap = {"status": True, "document": document, "ocrOutputResult": loaded_r['ocrOutputResult'],
                         "identificationOutputResult": loaded_r['identificationOutputResult'],
                         "identificationBoundaryOutputResult": loaded_r['identificationBoundaryOutputResult'],
                         "extractionOutputResult": loaded_r['extractionOutputResult'],
                         "fileType": loaded_r['fileType'], "lossType": loaded_r['lossType'], "comments": loaded_r['comments']}

    #fileinput.close()
    return returnMap

def getPdfEncoded(collection, document):
    path = path_join(real_directory(collection+ "source/"), document)

    a = open(path, "rb").read().encode("base64")

    return {"encodedPdf": a}