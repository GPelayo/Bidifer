import diffbot
import simplejson
import CorpusManager


def get_article_json(link, token):
    bias_bot = diffbot.DiffBot(token)
    try:
        article_json = bias_bot.article(link)
        print 'Article Character Count: {}'.format(len(article_json.get("text", "")))
        print 'Retrieved Article from:\n{0}'.format(link)
        return article_json
    except KeyError:
        print 'Threw Exception {0}: {1} \n From article: {2}'.format(article_json['errorCode'], article_json['error'], link)
        return "{}"
    except simplejson.scanner.JSONDecodeError:
        print "JSONDecodeError: invalid article data"
        return "{}"


def get_multiple_article_json(links, publication_id, token, article_line_limit=10, initial_link_index=1):
    article_set = []
    total_articles = len(links)
    article_count = initial_link_index
    invalid_articles_offset = 0
    recorded_errors = ""

    try:
        with open("error-dump", 'r') as errorDump:
            recorded_errors = errorDump.read()
    except IOError:
        pass
    for i in range(initial_link_index, total_articles+1):
        print "Extracted Article {}/{} (Link: {})".format(article_count-invalid_articles_offset,
                                                          total_articles-invalid_articles_offset, i)
        try:
            article = get_article_json(links[i-1], token)
            article_text = article.get("text", "")
        except AttributeError as e:
            recorded_errors += "\nAttribute Error: {} at article {}".format(repr(e), i)
            invalid_articles_offset += 1
        if len(article_text) > article_line_limit:
            article_set.append(article)
            CorpusManager.save_article_json(article, publication_id, index=i-invalid_articles_offset)
            article_count += 1
        else:
            recorded_errors += "Lacking Text at Article {}".format(i)
            print "Article Too Small:\nText: \"\"".format(article_text)
            invalid_articles_offset += 1
    with open("error-dump", 'w') as errorDump:
        errorDump.write(recorded_errors)
        print "Extracting Articles for {}".format(publication_id)
    print "\n{} Articles Omitted\n".format(invalid_articles_offset)
    return article_set