book_titles = {
    1: 'Childhood',
    2: 'Ayodhya',
    3: 'The Forest',
    4: 'Vanaras',
    5: 'Hanuman\'s Journey',
    6: 'Lanka'
}

book_descriptions = {
    1: `The childhood of Rama and his brothers, spent as princes at the
    palace of Ayodhya as sons of King Dashrathha.`,
    2: `The banishment of Rama, Sita and Laxmana from Ayodhya, due to Keikeiya's demand
    of her son Bharata to become King. Bharata refuses and revolts against his Mother,
    King Dashrattha dies of sorrow in Rama's absence.`,
    3: `The years in exile spent by Rama, Sita and Laxmana in the Forest. At the end,
    Sita is kidnapped by Ravana on his chariot and taken to Lanka.`,
    4: `The search for Sita leads Rama and Laxmana to the Kingdom of the <i>Vanaras</i>,
    the Great Monkeys. The King of the Vanaras, Sugriva, offers aid in exchange for helping
    restore his throne. This is where Rama meets Hanuman, the Son of Wind, armed with great
    strength, who becomes his greatest devotee.`,
    5: `Hanuman undertakes a journey to Lanka, to find Sita in Lanka. He is able to infilitrate
    Ravana's Great Palace, and talk to Sita, but eventually is caught by the royal guards. The guards
    tie him up, and burn his tail, but Hanuman's unties himself and takes his burning tail throughout
    Lanka, setting everything on fire, causing the <i>Lankadehan</i> (The Burning of Lanka).`,
    6: `With Hanuman's return from Lanka, and Lanka in disarray after the <i>Lankadehan</i> episode,
    the Vanara army along with Rama, Laxmana and Hanuman go to war. Ravana is slain in battle, 
    and Sita is freed.`
}
function GenerateBookCard(book) 
{
    book_card_HTML = `
    <div class="col-lg-3 col-md-4 col-sm-6 d-flex align-items-stretch">
        <div class="card shadow-lg my-3 mx-auto">
            <div class="card-header">
                <h4 class="card-title">Book ${book}</h4>${book_titles[book]}
            </div>
            <div class="card-body">
                <img src="/resources/images/book${book}.jpg" class="book-thumbnail" width="192px"><br>
                <hr>
                <div class="container h-75 small-text">
                    ${book_descriptions[book]}
                </div>
            </div>
            <div class="card-footer">
                <a href="/${book}/1.html" class="btn btn-sm btn-danger" style="float:left;"><span class="fa fa-book"></span>&nbsp;Read</a>
                <a href="/sanskrit/${book}/1.html" class="btn btn-sm btn-danger" style="float:right;">कि&nbsp;Original</a>
            </div>
        </div>
    </div>`
    return book_card_HTML;
}

function GenerateBooksCatalog(selector)
{
    var content = "";
    for(var i = 1; i <= 6; i++)
    {
        content += GenerateBookCard(i);
    }
    $(selector).html(content);
}