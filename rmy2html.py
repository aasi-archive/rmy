import os
import re
import jinja2

RMY_BUILD_DIR = './build/'

cantos_per_book = {
    1: 77,
    2: 119,
    3: 76,
    4: 67,
    5: 66,
    6: 130
}

def roman2n(roman_str):
    try:
        i = int(roman_str)
        return i
    except:
        roman_values_map = { "I": 1, 
                            "V": 5,
                            "X": 10,
                            "L": 50,
                            "C": 100,
                            "D": 500,
                            "M": 1000}
        result = 0
        i = len(roman_str) - 1
        current_val = roman_values_map["I"]
        while(i >= 0):
            c = roman_str[i]
            if(c not in roman_values_map):
                raise Exception("Invalid Roman Digit: " + c)
            val = roman_values_map[c]
            if(val < current_val):
                result -= val
            else:
                result += val
            current_val = val
            i -= 1
        return result

def rmy_generate_canto_path(book_no, canto_no, prefix=RMY_BUILD_DIR):
    return os.path.join(prefix, f'{book_no}/{canto_no}.html')

def rmy_render_book(book_no, canto_array, footnotes):
    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    jinja2_env = jinja2.Environment(loader=templateLoader)
    page_template = jinja2_env.get_template('rmy.template.html')

    for canto in canto_array:
        file_path = rmy_generate_canto_path(book_no, canto["number"])
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)

        next_page_url = "/"
        previous_page_url = "/"
        max_canto = cantos_per_book[book_no]

        if(canto["number"] < max_canto):
            next_page_url = rmy_generate_canto_path(book_no, canto["number"]+1, prefix='')
        elif(canto["number"] == max_canto and book_no < 6):
            next_page_url = rmy_generate_canto_path(book_no+1, 1, prefix='')
        
        if(canto["number"] > 1):
            previous_page_url = rmy_generate_canto_path(book_no, canto["number"] - 1, prefix='')
        elif(canto["number"] == 1 and book_no > 1):
            previous_page_url = rmy_generate_canto_path(book_no - 1, cantos_per_book[book_no - 1], prefix='')

        # Add the footnotes to both title and content
        content = canto["content"]
        title = canto["title"]

        # Replace '[GPT]' as <sup>GPT</sup>
        title = title.replace('[GPT]', '<span class="footnote-tooltip text-danger"><sup class="fs-6">GPT</sup><span class="footnote-tooltip-text">Not part of the original Griffith text. Generated from prose using GPT3.5.</span></span>')
        title = re.sub(r'\((\d+)\)', lambda match: f'<span class="footnote-tooltip text-danger"><sup><i class="fa fa-info-circle"></i></sup><span class="footnote-tooltip-text">{footnotes[int(match.group(1))-1]}</span></span>', title)
        content = content.replace('\n', '<br>')
        content = re.sub(r'\((\d+)\)', lambda match: f'<span class="footnote-tooltip text-danger"><sup><i class="fa fa-info-circle"></i></sup><span class="footnote-tooltip-text">{footnotes[int(match.group(1))-1]}</span></span>', content)

        page_info = {
            "canto": canto["number"],
            "book": book_no,
            # Replace newlines with HTML <br>
            "canto_content": content,
            "canto_title": title,
            "previous_page_url": previous_page_url,
            "next_page_url": next_page_url
        }

        with open(file_path, mode="w", encoding="utf-8") as page:
            page.write(page_template.render(page_info))
            page.close() 

if(__name__ == "__main__"):
    with open('rmy.txt', 'r', encoding='utf-8') as f:
        rmy_text = f.read()
        f.close()

    book_separator = re.compile(r'^BOOK ([IVXLCDM]+)\.', flags=re.MULTILINE|re.DOTALL|re.UNICODE)
    canto_separator = re.compile(r'^Canto ([IVXLCDM]+)\. ', flags=re.MULTILINE|re.DOTALL|re.UNICODE)
    footnote_separator = re.compile(r'^FOOTNOTES', flags=re.MULTILINE|re.DOTALL|re.UNICODE)
    footnote_content_separator = re.compile('^\d+ ', flags=re.MULTILINE|re.DOTALL|re.UNICODE)

    # First split the footnotes and the content 
    books_and_footnotes = re.split(footnote_separator, rmy_text)
    books = books_and_footnotes[0]
    footnotes = books_and_footnotes[1]

    # Now split the footnotes
    footnote_array = re.split(footnote_content_separator, footnotes)[1:]
    underscore_to_italics = re.compile(r'(?:^|\s)[^@#\s_]*(_([^_]+)_)', flags=re.MULTILINE|re.DOTALL|re.UNICODE)
    for i in range(0, len(footnote_array)):
        footnote_array[i] = re.sub(underscore_to_italics, lambda match: f'<em>&nbsp;{match.group(1).replace("_", "")}</em>', footnote_array[i])
    
    # Split the books
    book_split = re.split(book_separator, books)[1:]
    book_array = {}
    for i in range(0, len(book_split)):
        if(i % 2 == 1):
            book_array[i+1] = book_split[i]

    # Now split each book into cantos
    book_no = 1
    for book in book_array.keys():
        last_canto = 0
        canto_array = []
        canto_split = re.split(canto_separator, book_array[book])[1:]
        for i in range(0, len(canto_split)):
            if(i % 2 == 1):
                canto_title_content = canto_split[i].split('\n', 1)
                canto_title = canto_title_content[0]
                canto_content = canto_title_content[1].strip()
                canto_number = roman2n(canto_split[i-1])
                canto_dict = { 
                    "title": canto_title,
                    "content": canto_content,
                    "number": canto_number
                }

                if(canto_number - 1 != last_canto):
                    print(f"{book_no}.{canto_number} is missing.")
                
                last_canto = canto_number
                canto_array.append(canto_dict)
        print(f"Generating Book {book_no} (English)...")
        rmy_render_book(book_no, canto_array, footnote_array)
        book_no += 1

    