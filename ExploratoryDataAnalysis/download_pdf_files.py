import re
import urllib2
import urllib
def save_pdf_file(pdf_url, filename, folder):
    urllib.urlretrieve(pdf_url,folder+"/"+filename)

    print "Downloading ",pdf_url," ..."
    print "Rename as ",filename
    print ""


def get_new_file_name(pdf_url):

    # get "PeerGroup_1_*.pdf"
    file_name=pdf_url.split("/")[-1]

    #print "changing file name ", file_name, " ..."

    #remove"group" then  get "Peer_1_*.pdf"
    file_name=file_name.replace("PeerGroup","Peer")

    #get "*.pdf", where "*" is date
    old_date=file_name.split("_")[-1]

    #remove the suffix, then old date format is "*"
    old_date=old_date.replace(".pdf","")

    # get the new date format
    new_date=change_date_format(old_date)


    # replace the date in "Peer_1_*.pdf"
    new_file_name=file_name.replace(old_date,new_date)
    return new_file_name



def change_date_format(old_format):
    year=old_format[-4:]
    month=old_format.replace(year,"")

    month=month.lower()

    if month == "january" or month == "february" or month == "march" or month=="mar":
        quarter="Quarter1"

    elif month == "april" or month == "may" or month == "june" or month=="jun":
        quarter="Quarter2"

    elif month == "july" or month == "august" or month == "september" or month =="sept" or month=="sep":
        quarter="Quarter3"

    elif month == "october" or month == "november" or month == "december" or month=="dec":
        quarter="Quarter4"

    else:
        #for debugging
        quarter = "UnknownQuarter-"+month

    new_format=year+"_"+quarter
    return new_format





if __name__ == "__main__":
    seed_url = "https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/BHCPR_Peer.htm"

    seed_response=urllib2.urlopen(seed_url,timeout=20)

    seed_string=seed_response.read()

    #use the regular expression to find all relative urls
    re_pattern=re.compile(r"<a href=\"(.*?).pdf\">")
    relative_url_list=re.findall(re_pattern, seed_string)

    full_url_list=[]

    for relative_url  in relative_url_list:
        if relative_url.split("_")[-2]== "1":
            #only keep the peer1 data
            full_url_list.append("https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/" + relative_url + ".pdf")


    for full_url in full_url_list:
        #get new file name
        new_name=get_new_file_name(full_url)

        #save file
        save_pdf_file(full_url, new_name, "downloaded_pdf_files")


