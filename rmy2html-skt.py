import os
import jinja2

RMY_BUILD_DIR = './build/'
HI_numbers = {
    "1": "१",
    "2": "२",
    "3": "३",
    "4": "४",
    "5": "५",
    "6": "६",
    "7": "७",
    "8": "८",
    "9": "९",
    "0": "०",
    ".": "." 
}

def n2HIn(n):
    return ''.join([HI_numbers[c] for c in str(n)])

rmy_data = {
    1: {},
    2: {},
    3: {},
    4: {},
    5: {},
    6: {},
    7: {}
}

rmy_cantos_per_book_sanskrit = {}

def rmy_generate_canto_path_sanskrit(book_no, canto_no, prefix=RMY_BUILD_DIR):
    return os.path.join(prefix, f'sanskrit/{book_no}/{canto_no}.html')

def rmy_parse_verse_id(verse_id):
    book_no = int(verse_id[0:1])
    canto_no = int(verse_id[1:4])
    verse_no = int(verse_id[4:7])
    pad = verse_id[7]

    return (book_no, canto_no, verse_no, pad)

def rmy_parse_sanskrit_line(line):
    # Get the verse_id (start of every line, separated by space)
    line_split = line.split(' ', 1)
    verse_id = line_split[0]
    verse_txt = line_split[1]
    book, canto, verse, pad = rmy_parse_verse_id(verse_id)
    if(canto not in rmy_data[book]):
        rmy_data[book][canto] = {}
    
    if(verse not in rmy_data[book][canto]):
        rmy_data[book][canto][verse] = {}
    
    rmy_data[book][canto][verse]["number"] = f'{n2HIn(book)}.{n2HIn(canto)}.{n2HIn(verse)}'

    if(pad == 'a'):
        rmy_data[book][canto][verse]["pad_a"] = verse_txt
    else:
        rmy_data[book][canto][verse]["pad_c"] = verse_txt
    
def rmy_read_sanskrit(txt):
    with open(txt, 'r', encoding='utf-8') as f:
        rmy_text = f.readlines()
        for line in rmy_text:
            if(line.startswith("% ")):
                continue
            rmy_parse_sanskrit_line(line)

def rmy_render_sanskrit_canto(book_no, canto_no, verse_array):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    jinja2_env = jinja2.Environment(loader=templateLoader)
    page_template = jinja2_env.get_template('rmy-skt.template.html')

    file_path = rmy_generate_canto_path_sanskrit(book_no, canto_no)
    file_dir = os.path.dirname(file_path)
    os.makedirs(file_dir, exist_ok=True)

    next_page_url = "/"
    previous_page_url = "/"
    max_canto = rmy_cantos_per_book_sanskrit[book_no]

    if(canto_no < max_canto):
        next_page_url = rmy_generate_canto_path_sanskrit(book_no, canto_no+1, prefix='')
    elif(canto_no == max_canto and book_no < 6):
        next_page_url = rmy_generate_canto_path_sanskrit(book_no+1, 1, prefix='')
    
    if(canto_no > 1):
        previous_page_url = rmy_generate_canto_path_sanskrit(book_no, canto_no - 1, prefix='')
    elif(canto_no == 1 and book_no > 1):
        previous_page_url = rmy_generate_canto_path_sanskrit(book_no - 1, rmy_cantos_per_book_sanskrit[book_no - 1], prefix='')

    page_info = {
        "book": n2HIn(book_no),
        "canto": n2HIn(canto_no),
        "book_no_en": book_no,
        "canto_no_en": canto_no,
        "verse_array": verse_array,
        "previous_page_url": previous_page_url,
        "next_page_url": next_page_url
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(page_template.render(page_info))

def rmy_write_sanskrit_book(book_no):
    cantos = rmy_data[book_no]
    for canto in cantos.keys():
        verse_array = []
        for verse in rmy_data[book_no][canto].keys():
            verse_content = ""
            if("pad_a" in rmy_data[book_no][canto][verse]):
                verse_content += rmy_data[book_no][canto][verse]["pad_a"] + "<br>"
            if("pad_c" in rmy_data[book_no][canto][verse]):
                verse_content += rmy_data[book_no][canto][verse]["pad_c"] + "<br>"
            
            verse_array.append({ "number": rmy_data[book_no][canto][verse]["number"],  "content": verse_content })
        
        rmy_render_sanskrit_canto(book_no, canto, verse_array)

def rmy_build_canto_index():
    for i in range(1, 7):
        rmy_cantos_per_book_sanskrit[i] = len(rmy_data[i].keys())


# First read all that data into a dict
rmy_read_sanskrit('rmy-skt.txt')
# Then build the index
rmy_build_canto_index()
for i in range(1, 7):
    print(f"Generating HTML for Sanskrit Ramayana, {rmy_cantos_per_book_sanskrit[i]} cantos...")
    rmy_write_sanskrit_book(i)
