def pdf_to_csv(filename, separator, threshold):
    from cStringIO import StringIO
    from pdfminer.converter import LTChar, TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage

    class CsvConverter(TextConverter):
        def __init__(self, *args, **kwargs):
            TextConverter.__init__(self, *args, **kwargs)
            self.separator = separator
            self.threshold = threshold

    # ... the following part of the code is a remix of the
    # convert() function in the pdfminer/tools/pdf2text module
    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = CsvConverter(rsrc, outfp, codec="utf-8", laparams=LAParams())
    # becuase my test documents are utf-8 (note: utf-8 is the default codec)

    fp = open(filename, 'rb')

    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(PDFPage.get_pages(fp)):
        if page is not None:
            interpreter.process_page(page)
    device.close()
    fp.close()

    return outfp.getvalue()


if __name__ == '__main__':
    # the separator to use with the CSV
    separator = ';'
    # the distance multiplier after which a character is considered part of a new word/column/block. Usually 1.5 works quite well
    threshold = 1.5
    data= pdf_to_csv('Peer1_2002_1thQuarter.pdf', separator, threshold)
    lines=data.split("\n")
    f=open("test.csv","w")
    for char in data:

        f.write(char)
    breakpoint=1
    #print data