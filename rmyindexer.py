import os
import json
from unidecode import unidecode
from bs4 import BeautifulSoup

RMY_ROOT_DIR = './build/'
RMY_DIRS_TO_INDEX = [ '1', '2', '3', '4', '5', '6']
RMY_DIV_TO_INDEX = ['rmy-content']
RMY_SEARCH_INDEX = {}
SEARCH_INDEX_JSON = 'rmy.json'

def FilePathToIndexer(path):
    # Path is of the form
    # ./build/<book>/<canto>.html
    # We want to turn this into
    # <parva>,<verse>
    # Remove index root dir and html
    path = path.replace(RMY_ROOT_DIR, '')
    path = path.replace('.html', '')
    # Split by '\\'
    parva_verse = path.split('\\')
    return parva_verse[0] + ":" + parva_verse[1]

def GetHTMLFilesInDir(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if(file.endswith(".html")):
            result.append(os.path.join(path, file))
    return result

def AddToSearchIndex(file, content):
    indexloc = FilePathToIndexer(file)
    RMY_SEARCH_INDEX[indexloc] = unidecode(content.replace("\n", " ").replace("\t", " "))

all_files = []
for dir_to_index in RMY_DIRS_TO_INDEX:
    all_files += GetHTMLFilesInDir(os.path.join(RMY_ROOT_DIR, dir_to_index))

for file in all_files:
    with open(file, 'r', encoding='utf-8') as fp:
        soup = BeautifulSoup(fp, 'html.parser')
        content = soup.find(id='to_index')
        print("Index: ", file)
        if(content):
            AddToSearchIndex(file, content.get_text(separator = '\n', strip = True))

with open(SEARCH_INDEX_JSON, "wb") as index_file:
    index_file.write(json.dumps(RMY_SEARCH_INDEX, separators=(',', ':'), ensure_ascii=False).encode('utf-8'))
 