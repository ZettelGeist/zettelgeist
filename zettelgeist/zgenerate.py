import yaml
import random
import pprint
import os
import os.path
import sys
import random_words

from zettelgeist import zdb

NUMBER_OF_DOCS = int(sys.argv[1])

MIN_WORDS = 5
MAX_WORDS = 10

MIN_WORDS_TEXT = 100
MAX_WORDS_TEXT = 500

MIN_LINES = 3
MAX_LINES = 10

OUTPUT_DIR = "./data"


def generate_doc():
    doc = {}
    for field in zdb.ZETTEL_FIELDS:
        if field in ['tags']:
            doc[field] = generate_list()
        elif field in ['mentions']:
            doc[field] = generate_list_of_nicknames()
        elif field in ['filename']:
            doc[field] = generate_filename()
        elif field in ['summary', 'text']:
            doc[field] = generate_text(MIN_WORDS_TEXT, MAX_WORDS_TEXT)
        elif field in ['dates']:
            doc[field] = generate_date()
        else:
            doc[field] = generate_text(MIN_WORDS, MAX_WORDS)

    return doc


rw = random_words.RandomWords()


def generate_word(i):
    return rw.random_word()


def generate_text(min_words, max_words):
    number_of_words = random.randint(min_words, max_words)
    return " ".join([generate_word(i) for i in range(0, number_of_words)])


def generate_list():
    number_of_lines = random.randint(MIN_LINES, MAX_LINES)
    return [generate_word(i) for i in range(0, number_of_lines)]


def generate_list_of_nicknames():
    rn = random_words.RandomNicknames()
    number_of_lines = random.randint(MIN_LINES, MAX_LINES)
    return [rn.random_nick(gender=['m', 'f'][i % 2]) for i in range(0, number_of_lines)]


ERA = ['BC', 'BCE', 'CE', 'AD']


def generate_date():
    year = random.randint(0, 2016)
    disp = random.randint(0, 100)

    if disp % 3 == 0:
        return "%s %s" % (year, ERA[year % 4])
    else:
        era = ERA[year % 4]
        if era in ['BC', 'BCE']:
            return "%s-%s %s" % (year + disp, year, ERA[year % 4])
        else:
            return "%s-%s %s" % (year, year + disp, ERA[year % 4])
    return year


def generate_filename():
    return "-".join(generate_list()) + '.yaml'


doc = generate_doc()

#pp = pprint.PrettyPrinter()
# pp.pprint(doc)

if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

print("Generating %d docs. Please wait." % NUMBER_OF_DOCS)
for i in range(0, max(NUMBER_OF_DOCS, 100)):
    if (i + 1) % 100 == 0:
        print("...%d" % (i + 1))
    doc = generate_doc()
    yaml_path = os.path.join(OUTPUT_DIR, doc['filename'])
    del(doc['filename'])
    with open(yaml_path, "w") as outfile:
        outfile.write(yaml.dump(doc))
