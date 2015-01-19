import GoogleSearchExtractor
import CorpusManager
import ArticleExtractor
import ConfigParser
import sys
import getopt

SEARCH_PAGE_LIMIT = 1


class NoConfigFileException(Exception):
    pass


class MissingArgumentsException(Exception):
    pass


def main(argv):
    find_links_enabled = False
    find_articles_enabled = False
    make_viewpoint_directories = False
    viewpoint_id = ""
    pub_config_path = "settings/publication-data.ini"
    api_config_path = "settings/api-keys.ini"

    try:
        if len(argv) < 2:
            raise MissingArgumentsException

        viewpoint_id = sys.argv[1]
        opts, args = getopt.getopt(argv[2:], "lad", ['config=', 'api='])
        for opt, arg in opts:
            if "-l" == opt:
                find_links_enabled = True
            elif "-a" == opt:
                find_articles_enabled = True
            elif "-d" == opt:
                make_viewpoint_directories = True
            elif "--config" in opt:
                pub_config_path = arg
            elif "--api" in opt:
                api_config_path = arg

        config_parser = ConfigParser.SafeConfigParser()
        config_data = config_parser.read(pub_config_path)

        if len(config_data) > 0:
            current_pub_ids = config_parser.get(viewpoint_id, "publicationIDs").split(',')
        else:
            raise NoConfigFileException
        if find_links_enabled:
            for publicationID in current_pub_ids:
                query = config_parser.get(publicationID, "query")
                domain = config_parser.get(publicationID, "domain")
                url = GoogleSearchExtractor.generate_search_query(query, domain)
                links = GoogleSearchExtractor.scrape_google_links(publicationID, url, SEARCH_PAGE_LIMIT)
                CorpusManager.save_links_to_file(links, publicationID)
            print "============\nFinished Retrieving Links\n============"
        if find_articles_enabled:
            config_data = ConfigParser.RawConfigParser()
            config_data.read(api_config_path)
            token = config_data.get('DiffBot', 'Token')
            for publicationID in current_pub_ids:
                links = CorpusManager.load_links_file(publicationID)
                ArticleExtractor.get_multiple_article_json(links, publicationID, token, initial_link_index=1)
            print "============\nFinished Retrieving Articles\n============"
        if make_viewpoint_directories:
            CorpusManager.make_viewpoint_articles(viewpoint_id, current_pub_ids)
    except ConfigParser.NoSectionError:
        show_error("\"" + viewpoint_id + "\" is an invalid Viewpoint ID. \nPlease check configuration file in " + pub_config_path)
    except NoConfigFileException:
        show_error("Configuration File Not Found")
    except getopt.GetoptError:
        show_error("Invalid Argument(s)")
    except MissingArgumentsException:
        show_error("Missing Argument(s)")
    except Exception as e:
        show_error("Uncatched Exception: " + e.message)


def show_error(error_type):
    print "\nERROR:", error_type
    show_instructions()


def show_instructions():
    print ("\n\nInstructions for the Article Scraper:\n"
           "\tArticle Scraper <Viewpoint> [options]...\n"
           "\n\tOptions:\n"
           "\t\t-l\tGet Article links from Google\n\n"
           "\t\t-a\tGet Articles using Diffbot.\n"
           "\t\t\tRequires links from data/(pub id)/(pubid)-links.txt\n\n"
           "\t\t-d\tParses JSON Data of each article to a .txt file of the\n"
           "\t\t\tarticle's main text.Then, it is saved to the Viewpoint\n"
           "\t\t\tfolder and are organized by viewpoint. Requires json\n"
           "\t\t\tarticle data from data/(publication id)/article-json\n\n"
           "\t--config <path>\tSets the path of the .ini file for the publication data\n"
           "\t\t\t(Default: settings/publication-data.ini)\n\n"
           "\t--api <path> \tSets the filepath of the .ini file for the api keys\n"
           "\t\t\t(Default: setting/api-keys.ini)\n")


if __name__ == "__main__":
    main(sys.argv)