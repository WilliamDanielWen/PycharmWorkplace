import urllib2


def download_pdf_url(download_url):
    response = urllib2.urlopen(download_url)
    file = open("PeerGroup_1_March2016.pdf", 'wb')
    file.write(response.read())
    file.close()
    print("Completed")

if __name__ == "__main__":
    seed_url = "https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/BHCPR_Peer.htm"
    seed_response=urllib2.urlopen(seed_url,timeout=20)
    source=seed_response.read()


    url="https://www.ffiec.gov/nicpubweb/content/BHCPRRPT/REPORTS/BHCPR_PEER/March2016/PeerGroup_1_March2016.pdf"
    download_pdf_url(url)