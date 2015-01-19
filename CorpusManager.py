from ConfigParser import ConfigParser
import json
import codecs
import os


def check_directory(media_source_id):
    file_dir = "data/publication/{0}".format(media_source_id)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)


def dump_search_page(media_source_id, article_num, html):
    check_directory(media_source_id)
    directory = "data/publication/{0}/google-search-links/".format(media_source_id)
    file_location = directory + "{0}-pg{1}.htm".format(media_source_id, article_num)
    if not os.path.exists(directory):
        os.makedirs(directory)
    html_file = open(file_location, "w")
    html_file.write(html)
    html_file.close()


def save_article_json(article_json, media_source_id, index=-1):
    check_directory(media_source_id)
    directory = "data/publication/{0}/article-json/".format(media_source_id)

    if not os.path.exists(directory):
        os.makedirs(directory)

    file_location = "{0}{1}-article-data-{2}.json".format(directory, media_source_id, index)
    json_file = codecs.open(file_location, 'wb', 'utf-8')
    json.dump(article_json, json_file, indent=4)
    json_file.close()


def load_viewpoint_json(pub_id):
    json_batch = []
    i = 0
    while True:
        i += 1
        file_path = "data/publication/{0}/article-json/{0}-article-data-{1}.json".format(pub_id, i)
        try:
            with codecs.open(file_path, 'r', 'utf-8') as articleDatafile:
                json_batch.append(json.load(articleDatafile))
        except IOError:
            print "Stopped at searching {} article data at index {}".format(pub_id, i)
            break

    return json_batch

def save_links_to_file(links, media_source_id):
    check_directory(media_source_id)

    links = [link.strip() for link in links]
    new_links_file = open("data/publication/{0}/{0}-links.txt".format(media_source_id), 'w')
    new_links_file.writelines('\n'.join(links))
    new_links_file.close()


def load_links_file(media_source_id):
    links_file = open("data/publication/{0}/{0}-links.txt".format(media_source_id), 'r')
    links = links_file.readlines()
    links_file.close()
    return links


def make_viewpoint_articles(viewpoint_id, pub_ids):
    directory = "data/viewpoint/articles/{}".format(viewpoint_id)

    if not os.path.exists(directory):
        os.makedirs(directory)
    for pubID in pub_ids:
        json_array = load_viewpoint_json(pubID)
        article_index = 1
        for article in json_array:
            article_index += 1
            article_file = codecs.open("{}/{}-{}.txt".format(directory, pubID, article_index), 'wb', 'utf-8')
            article_file.write(article.get("text"))
            article_file.close()