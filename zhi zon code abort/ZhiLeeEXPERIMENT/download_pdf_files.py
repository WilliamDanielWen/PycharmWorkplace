import urllib

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open


def readpdf(pdfFile):
    rsrcmgr=PDFResourceManager()
    retstr= StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)


    process_pdf(rsrcmgr, retstr, laparams=laparams)
    device.close()


    content = retstr.getvalue()
    retstr.cloese()

    content = retstr.getvalue()
    retstr.close()
    return content

pdfFile = urlopen("")
outputString = readpdf(pdfFile)
print(outputString)
pdfFile.close()

