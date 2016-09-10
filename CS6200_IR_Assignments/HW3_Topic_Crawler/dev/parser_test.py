from lxml import etree
import urllib2
import time

if __name__ == '__main__':

    t1 = time.time() * 1000

    url = 'http://www.theamericanrevolution.org/DocumentDetail.aspx?document=33'

    opener = urllib2.build_opener()

    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    response = opener.open(url)
    header = response.info()

    print header

    if 'content-type' in header:
        if 'text' in header['content-type']:
            print 'NOT text-based page: {}'.format(url)

    # if 'content-language' in header:
    #     print header['content-language']
    #     if 'en' not in header['content-language']:
    #         print ('NOT english-based page: {}'.format(url))

    html = str(response.read())
    response.close()
    opener.close()

    parser = etree.HTMLParser(encoding='utf-8', target = Parser(url), remove_blank_text=True, remove_comments=True)

    etree.HTML(html, parser)

    t2 = time.time() * 1000

    text = ' '.join(parser.target.text_lines)
    print text

    title = parser.target.title
    print title

    links = parser.target.links

    for link in links:
        print link



    print 'elapsed time: {} ms'.format(t2 - t1)