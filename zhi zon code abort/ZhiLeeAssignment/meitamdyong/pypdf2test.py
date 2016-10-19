from urllib import urlopen
import PyPDF2

pdfFileObj = open('Peer1_2002_1thQuarter.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
form=pdfReader.getFormTextFields()
breakp=1

