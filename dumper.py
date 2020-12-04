import argparse
import requests
import json
import logging

queries = {}
def load_queries():
    global queries
    with open("queries.json", 'r') as f:
        queries = json.load(f)

def dump_all():
    for lang in queries.keys():
        dump(lang)

def dump(lang):
    """ dumps """
    logging.info("Saving properties for language '{}'".format(lang))
    S = requests.Session()

    dump_id = queries[lang]["json"]

    URL = "https://quarry.wmflabs.org/run/{}/output/0/json".format(dump_id)

    R = S.get(url=URL)
    S.close()
    data = R.json()

    results = {}
    for row in data["rows"]:
        property_id = row[0]
        property_label = row[1]
        results[property_id] = property_label

    save_results(results, lang)

def save_results(results, lang):
    with open("properties/{}.json".format(lang), 'w') as f:
        json.dump(results, f)

if __name__ == "__main__":
    load_queries()

    parser = argparse.ArgumentParser(description='Dumps wikipedia properties')
    available_languages = ", ".join(["ALL"] + list(queries.keys()))
    parser.add_argument('LANG', metavar='LANG', type=str,
                        help='available languages: {}'.format(available_languages))
    args = parser.parse_args()
    lang = args.LANG

    if lang == "ALL":
        dump_all()
    else:
        dump(lang)