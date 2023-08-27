cantos_per_book = {
    "en":
    {
        1: 77,
        2: 119,
        3: 76,
        4: 67,
        5: 66,
        6: 130
    },
    "sa":
    {
        1: 76,
        2: 111,
        3: 71,
        4: 66,
        5: 66,
        6: 116
    }
}

book_titles = {
    "en":
    {
        1: "Childhood",
        2: "Ayodhya",
        3: "The Forest",
        4: "Vanaras",
        5: "Hanuman's Journey",
        6: "Lanka"
    },
    "sa":
    {
        1: "बालकाण्ड",
        2: "अयोध्याकाण्ड",
        3: "अरण्यकाण्ड",
        4: "किष्किन्धाकाण्ड",
        5: "सुन्दरकाण्ड",
        6: "लंकाकाण्ड"
    }
}

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
};

/* Convert a number to a Devanagari/Hindi-number */
function n2HIn(n)
{
    var s = n.toString();
    var result = "";
    for(var i = 0; i < s.length; i++)
    {
        result += HI_numbers[s[i]];
    }
    return result;
}

function GenerateSideBarHTML(sidebar_title)
{
    var sidebar_html = `
    <img src="/resources/images/sidebar.png" class="sidebar-button" type="button" data-bs-toggle="offcanvas"
    data-bs-target="#rmy_offcanvas" aria-controls="rmy_offcanvas">

    <div class="offcanvas offcanvas-start" tabindex="-1" id="rmy_offcanvas" aria-labelledby="rmy_offcanvas_label">

    <div class="offcanvas-header">
        <h2 class="offcanvas-title" id="rmy_offcanvas_label">${sidebar_title}</h2>
        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" aria-label="Close"></button>
    </div>

    <div class="offcanvas-body shadow-lg">
        <div class="accordion mx-auto" id="rmy-index">
        </div>
    </div>
    `
    return sidebar_html;
}

function nToString(n, language)
{
    if(language == "sa")
    {
        return n2HIn(n);
    }
    else
    {
        return n.toString();
    }
}

function GenerateBookCantoList(language)
{
    var current_canto = $('.rmy-content').data('rmy-canto');
    var current_book = $('.rmy-content').data('rmy-book');
    var canto_list = cantos_per_book[language];

    var URL_language_prefix = (language == "sa") ? "sanskrit/" : "";
    var book_titles_language = book_titles[language];
    var canto_text = (language == "sa") ? "सर्ग" : "Canto";

    for(book in canto_list)
    {
        var book_active = (current_book == book) ? "true" : "false";
        var collapse_list_id = `collapse-list-${book}`;
        
        book_index_html = `<div class="accordion-item my-3 shadow">
        <h4 class="accordion-header">
        <button class="accordion-button ${current_book == book ? "" : "collapsed"}" type="button" data-bs-toggle="collapse" data-bs-target="#${collapse_list_id}" aria-expanded="${book_active}" aria-controls="${collapse_list_id}">
        ${nToString(book, language)}. ${book_titles_language[book]}
        </button>
        </h4>`;
        book_index_html += `<div class="accordion-collapse collapse ${current_book == book ? "show" : ""}" id="${collapse_list_id}">`
        book_index_html += `<div class="accordion-body"><ul class="list-group">`;
        var max_cantos = canto_list[book];
        for(var canto = 1; canto <= max_cantos; canto++)
        {
            var canto_active = (current_book == book && current_canto == canto) ? "active" : "";
            book_index_html += `<a href="/${URL_language_prefix}${book}/${canto}.html" class="list-group-item ${canto_active}">${canto_text} ${nToString(canto, language)}</li>`;
        }
        book_index_html += `</ul>`;
        book_index_html += `</div></div></div>`;
        $('#rmy-index').append(book_index_html);
    }
}

function AddZoomButtons()
{
    zoom_buttons = `<div class="zoom-button">
    <button class="btn btn-danger" onClick="IncreaseFontSize('rmy-content', 1.1)">
    <span class="fa fa-lg fa-search-plus px-2"></span>
    </button>

    <button class="btn btn-danger" onClick="IncreaseFontSize('rmy-content', 0.9)">
    <span class="fa fa-lg fa-search-minus px-2"></span>
    </button>
    </div>`;

    $('body').append(zoom_buttons);
}

/* Function for increasing font size. */
function IncreaseFontSize(id, increaseFactor)
{
    txt = document.getElementsByClassName(id)[0];
    style = window.getComputedStyle(txt, null).getPropertyValue('font-size');
    currentSize = parseFloat(style);
    txt.style.fontSize = (currentSize*increaseFactor) + 'px';
}

$(document).ready(() => {
    var language = $('.rmy-content').data('rmy-lang');
    $('body').append(GenerateSideBarHTML(language == 'en' ? "Ramayana" : "रामायण"));
    GenerateBookCantoList(language);
    AddZoomButtons();
});