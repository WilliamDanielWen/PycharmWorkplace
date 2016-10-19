import PyPDF2
pdfReader = PyPDF2.PdfFileReader(open('encrypted.pdf', 'rb'))
pdfReader.isEncrypted
True
pdfReader.getPage(0)
Traceback (most recent call last):
File "<pyshell#173>", line 1, in <module>
pdfReader.getPage()
--snip--
File "C:\Python34\lib\site-packages\PyPDF2\pdf.py", line 1173, in getObject
raise utils.PdfReadError("file has not been decrypted")
PyPDF2.utils.PdfReadError: file has not been decrypted
pdfReader.decrypt('rosebud')
1
pageObj = pdfReader.getPage(0)