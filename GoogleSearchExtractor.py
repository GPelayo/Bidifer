import urllib2
import CorpusManager
from bs4 import BeautifulSoup


def generate_search_query(query, domain="", date=""):
    domain_parameter = ""
    date_parameter = ""
    if len(domain) > 0:
        domain_parameter = "+site:{}".format(domain)
    if len(date) > 0:
        date_parameter = "+daterange:{}".format(date)

    url = "https://www.google.com/search?q={}{}{}".format(query, domain_parameter, date_parameter)
    return url.replace(" ", "+", len(url))


def scrape_google_links(pub_id, search_result_url, page_qty, initial_page=1):
    links = []
    for i in range(initial_page-1, page_qty):
        print "Accessing Google Results Page {}".format(i+1)
        url = u"{}&start={}".format(search_result_url, i*10)
        print "Using link {}".format(url)
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0)'
                                         'Gecko/20100101 Firefox/24.0')
        response = urllib2.urlopen(request)
        html = response.read()
        print "Scrapping Links for Page {}".format(i+1)
        links = scrape_google_search_page(html)
    unique_links = set(links)
    print "{} Unique Links Found from Scrapping for {}\n\n".format(len(unique_links), pub_id)
    print "{} Duplicate Links Removed\n\n".format((len(links) - len(unique_links)))
    return unique_links


#Please change if google updates the google site structure
def scrape_google_search_page(html):
    soup = BeautifulSoup(html)
    links = []
    results = soup.findAll("h3", {"class", "r"})
    for result in results:
        links += [result.find("a")["href"]]
    #pretty_html = soup.prettify().encode("utf-8")
    #CorpusManager.dump_search_page(pub_id, i+1, pretty_html)
    return links