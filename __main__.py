import GoogleSearchExtractor
import CorpusManager
import ArticleExtractor
import ConfigParser
import sys


SEARCH_PAGE_LIMIT = 1
INCLINATION_ID = sys.argv[1]

FIND_LINKS_ENABLED = False
FIND_ARTICLES_ENABLED = False
MAKE_VIEWPOINT_DIRECTORIES = False


class NoConfigFileException(Exception):
    pass

for arg in sys.argv:
    if arg == '-l':
        FIND_LINKS_ENABLED = True
    elif arg == '-a':
        FIND_ARTICLES_ENABLED = True
    elif arg == '-d':
        MAKE_VIEWPOINT_DIRECTORIES = True

publicationData = ConfigParser.SafeConfigParser()
foundInIs = publicationData.read("settings/publication-data.ini")

try:
    if len(foundInIs) > 0:
        currentPubIDs = publicationData.get(INCLINATION_ID, "publicationIDs").split(',')
    else:
        raise NoConfigFileException
    if FIND_LINKS_ENABLED:
        for publicationID in currentPubIDs:
            query = publicationData.get(publicationID, "query")
            domain = publicationData.get(publicationID, "domain")
            url = GoogleSearchExtractor.generate_search_query(query, domain)
            links = GoogleSearchExtractor.scrape_google_links(publicationID, url, SEARCH_PAGE_LIMIT)
            CorpusManager.save_links_to_file(links, publicationID)
        print "============\nFinished Retrieving Links\n============"
    if FIND_ARTICLES_ENABLED:
        for publicationID in currentPubIDs:
            links = CorpusManager.load_links_file(publicationID)
            articleJSON = ArticleExtractor.get_multiple_article_json(links, publicationID, initial_link_index=1)
        print "============\nFinished Retrieving Articles\n============"
    if MAKE_VIEWPOINT_DIRECTORIES:
        CorpusManager.make_viewpoint_articles(INCLINATION_ID, currentPubIDs)
except ConfigParser.NoSectionError:
    print "Invalid Viewpoint ID"
except NoConfigFileException:
    print "Configuration File Not Found"