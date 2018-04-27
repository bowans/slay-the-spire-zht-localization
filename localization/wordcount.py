'''
This script counts words in json files.

Example usage:
python3 wordcount.py eng/achievements.json  # count words in single file
python3 wordcount.py eng                    # count words in single dir
python3 wordcount.py                        # count all words for all language dirs
'''
import json
import sys
import os
import glob
from functools import reduce

def extract_values(d):
    words = []
    def _extract_values(d):
        if isinstance(d, list):
            for v in d:
                _extract_values(v)
        elif isinstance(d, dict):
            for v in list(d.values()):
                _extract_values(v)
        elif isinstance(d, str) or isinstance(d, unicode):
            words.append(d)
        else:
            words.append(str(d))
    _extract_values(d)
    return words

def read_file(filename):
    with open(filename) as f:
        data = f.read()
    return json.loads(data)

def word_count(data):
    values = extract_values(data)
    words = ' '.join(values).split(' ')
    return len(words)

def process(files):
    print(files)
    wcount = reduce(lambda x,y:x+y, map(lambda x: word_count(read_file(x)), files))
    print("total words: " + str(wcount))

def extract_per_language(lang):
    files = glob.glob("{}/*.json".format(lang))
    process(files)

def main():
    files = sys.argv[1:]
    if len(files) == 0:
        lang_packs = list(filter(lambda x: os.path.isdir(x) and len(x) == 3 and x != 'www', os.listdir()))
        list(map(extract_per_language, lang_packs))
    elif os.path.isdir(files[0]):
        list(map(extract_per_language, files))
    else:
        process(files)

if __name__ == "__main__":
    main()
