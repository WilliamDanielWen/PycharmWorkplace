from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

class CsvConverter(TextConverter):
    def __init__(self, *args, **kwargs):
        TextConverter.__init__(self, *args, **kwargs)
        pass

#convert a pdf file into a string using pdf miner
def pdf_to_str(filename):

    rsrc = PDFResourceManager()
    outfp = StringIO()
    device = CsvConverter(rsrc, outfp, codec="utf-8", laparams=LAParams())

    fp = open(filename, 'rb')
    interpreter = PDFPageInterpreter(rsrc, device)
    for i, page in enumerate(PDFPage.get_pages(fp)):
        if page is not None:
            interpreter.process_page(page)
    device.close()
    fp.close()

    return outfp.getvalue()



def pdf_to_csv(pdf_file_path, folder):
    print "convert ",pdf_file_path, " ..."

    #get the string
    converved_str = pdf_to_str(pdf_file_path)

    #remove ".pdf"
    file_name = pdf_file_path.split(".")[0]

    #remove "*/"
    file_name=file_name.split("/")[-1]


    output_file_name = file_name + ".csv"
    f = open(folder+"/"+output_file_name, "w")
    f.write(converved_str)
    f.close()




import glob
if __name__ == '__main__':

    #use regular expression to get the path of all pdf files
    pdf_path_sets=glob.glob("downloaded_pdf_files/*.pdf")


    for pdf_file_path in pdf_path_sets:
        pdf_to_csv(pdf_file_path, "converted_csv_files")




