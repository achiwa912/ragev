
# Table of Contents

1.  [vocaBull (server)](#org007f6ae)
2.  [Overview](#orgd480a0a)
    1.  [How Vocabull works](#org9364c2d)
    2.  [The Shifting Learning Window method](#orgcc7054f)
3.  [Quick Start](#org9e7f328)
    1.  [Register and login](#org4e7e312)
    2.  [Choose a sample book](#org930dd7a)
    3.  [Practice flashcards](#org8769a29)
    4.  [Practice type spells](#org4cdd3fd)
    5.  [Create a book and add words](#org96ef701)
    6.  [Optionally, you can load words from file](#orgdcd16bd)
    7.  [Or, borrow a wordbook from the library (new)](#org6a6832d)
    8.  [Backup and restore](#org51e55d9)
        1.  [How to backup](#orgdcf2533)
        2.  [How to restore](#org0b192b3)
4.  [Setup server](#orgc817e85)
5.  [License](#orgf73bf6d)
6.  [Contact](#org21d7375)
7.  [Acknowledgments](#org12539f7)


<a id="org007f6ae"></a>

# vocaBull (server)

![img](./images/vbs.jpg)


<a id="orgd480a0a"></a>

# Overview

[Vocabull (server)](https://github.com/achiwa912/vbs) is a better flashcard web application for your vocabulary building.  It has three modes:

1.  Flashcard - word &rarr; definition
2.  Flashcard - definition &rarr; word
3.  Type words from the definitions

I believe it is better than simple flashcards because:

-   You'll see hard-to-memorize words more frequently
    -   The shifting learning window method (see below)
-   You can practice spelling (the type-word mode)
-   vocaBull pronounces words and examples for you
-   As a web application, you can practice anywhere at anytime with your mobile phone, tablet or PC
-   Presents words in random order

![img](./images/vocabull_sample.jpg)


<a id="org9364c2d"></a>

## How Vocabull works

-   Vocabull randomly presents to you words that have the lowest "memorized" score
-   Vocabull keeps track of 10 recent unfamiliar words that you are working on
-   You'll see these 10 words repeatedly until you "memorize" them for now
-   You'll see memorized words again after the entire words are memorized for the round
-   You can skip known words for five entire rounds; or, you can remove the words


<a id="orgcc7054f"></a>

## The Shifting Learning Window method

Repetition is the key for memorizing new words (thus, flash cards), but I don't think exising flash cards or flash-card apps provide you with enough repetitions for efficient memorization.

For example, say, a set of flash cards or a word book has 200 words.  If you go over the 200 words one-by-one, you'd be most likely to forget almost everything when you encountr the same word for the 2nd, 3rd or 4th time.

vocaBull addresses this issue by introducing a combination of high-frequency repetitions of small number of words, and low-frequency repetitions of medium number of words - the Shifting Learning Window method.

![img](./images/vbs_SLW.jpg)

The high-frequenry repetitions are realized with the "learning window".  Learning window can have 10 words, and initially has the 1st 10 words in a word book.  (More precicely, words are randomly picked)

As you repeat 10 words in the learning window, you memorize a word or two.  Then, the learning window replaces the memorized word with a new word.  This way, the learning window has 10 words that you are actively working on.  It shifts through a word book and eventually reaches the end of the book.  Then, the next cycle starts.  This process contines until you memorize everything in the book.

As you can see, a word book represents the unit of low-frequency repepitions.


<a id="org9e7f328"></a>

# Quick Start


<a id="org4e7e312"></a>

## Register and login

-   You can try <https://achiwa912.pythonanywhere.com>
-   Click the menu icon at the top right corner > `Login` > `Click here to register`
-   Register your account
-   Check your email and confirm
    -   Note: you might need to wait several minutes for a confirmation email to arrive; pythonanywhere is really slow on this&#x2026;
-   Login


<a id="org930dd7a"></a>

## Choose a sample book

-   At first, a sample book (ie, sample\_<your<sub>user</sub><sub>name</sub>>) is registered and it has 5 words in it

![img](./images/vbs_samplebook.jpg)

-   Click the sample book


<a id="org8769a29"></a>

## Practice flashcards

-   Click `(play) practice` menu > choose `word to def` or `def to word`
    -   You will be navigated to the practice page

![img](./images/vbs_samplewords.jpg)

-   Click the word card to flip and show the answer
    -   Blue card shows the word, and greenish-blue card shows the definition
    -   You can flip cards as many as you like

![img](./images/vbs_w2d.jpg)

-   Click `(single-note) word` to check the pronunciation of the word
-   Click `(duplet) example` to check the pronunciation of the example sentence
-   If you don't know, click `(thumbs-down) once more` so that the word will reappear in the near future
-   If you managed to memorize it, click `(thumbs-up) okay!` to increase the score by 1
    -   You won't see the word for this round as vocaBull presents to you 10-lowest-score words
-   If you know the word, click `(skip) knew it!` to increase the score by 5!
    -   So, you won't see the word for 5 rounds
-   Click `Back to book` to go back to the selected book


<a id="org4cdd3fd"></a>

## Practice type spells

-   Click `(play) practice` menu > choose `type word`
-   vocaBull shows the definition of a word and asks you to type the word

![img](./images/vbs_type.jpg)

-   Type your answer and click `Submit` (or push `return` key)
-   It shows correct/incorrect and asks you to type the word 4 times, anyway
    -   Tip: use `tab` or `return` key to move from an input box to another
    -   If incorrect, you'll see the word again after a while
    -   Click `(single-note) word` to check the pronunciation of the word
    -   Click `(duplet) example` to check the pronunciation of the example sentence

![img](./images/vbs_repeat.jpg)

-   It moves to the next word


<a id="org96ef701"></a>

## Create a book and add words

Also, you can create your own book and register words.

-   Click My Books > `Add` button
-   Type a book name, language to pronounce and click `Submit`
    -   The language code will be used to pronounce words
    -   It can be en-US (English (USA)), fr-FR (French (France)), etc. and default to en-US
    -   Language code list here: <http://www.lingoes.net/en/translator/langcode.htm>
    -   Note: your browser might not support some languages
-   Click the newly created book card > click `Add word`
-   Type word and definition, and then click `Submit` &rarr; Now, `Practice` is activated
    -   Add a few words


<a id="orgdcd16bd"></a>

## Optionally, you can load words from file

-   Prepare a word definition file
    -   one word definition per line
    -   a line consists of `word`, `definition` and an optional `sample sentence` separated by a tab (\t)
    -   a line format (`\t` is a tab):

    <word>\t<definition>[\t<sample>]

-   Example:

    strident	shrill, harsh, rough	in more strident tones
    lassitude	weariness, fatigue	 feeling of lassitude
    deleterious	bad, harmful	a deleterious effect on health

-   Navigate to a book page
-   Click `Load from file` > click `Browse...` > choose a file > click `Submit`


<a id="org6a6832d"></a>

## Or, borrow a wordbook from the library (new)

You can borrow wordbooks that other users created and practice them as if these are your own books.

-   Click menu icon on the top-right corner > choose `library` > you are navigated to the library page

![img](./images/library.jpg)

-   You'll see books that other pepole published
-   Click a book for browsing

![img](./images/browse.jpg)

-   If you click `(Cart) Checkout`, the book will appear on your home page but in a different color from your own books.

![img](./images/borrowed.jpg)


<a id="org51e55d9"></a>

## Backup and restore

As Vocabull is still being developed, there's some risk that your data is all deleted and lost.  For example, a bug could corrupt the database.  To address such a scenario, I have implemented `Export all` and `Import and restore` features, which enable you to backup/restore your books and practice progress to a local file.

`Export all` exports all your books, all words in them and scores to a JSON file.

`Import and restore` reads the backup JSON file and restores books, words and scores.  If there's an existing book of the same name, it will add words to the existing book.  If the same word is in the book, it will overwrite the definition and sample sentence from the backup.  For scores, larger values remain.

For example, if you `Export all` and then `Import and restore` right after, nothing will change in your books, words or scores.


<a id="orgdcf2533"></a>

### How to backup

-   On the top page, scroll down until you see Backup and restore section.
-   Click `Export all` to save your books and progress to a local file named `vocabull.json`


<a id="org0b192b3"></a>

### How to restore

-   On the top page, scroll down until you see Backup and restore section.
-   click `Import and restore` button
-   Click `Browse...` and choose `vocabull.json`, and then click `Submit`


<a id="orgc817e85"></a>

# Setup server

If you ever want to setup a vocaBull server yourself, here's the steps.

-   Setup Python 3.11 or later
-   git clone repository

    git clone https://github.com/achiwa912/vbs.git

or

    git clone git@github.com:achiwa912/vbs.git

-   create virtual environment (recommended)

    cd vbs
    python -m venv ve
    ./ve/bin/activate

-   Install prerequisites

    pip install -r requirements.txt

-   Set environment variables if you use Flask's development web server

    export FLASK_APP=vbs.py
    export FLASK_DEBUG=1  # optional

-   Prepare secrets.json file in the project folder (eg, ~/py/vbs/secrets.json)
    -   SECRET<sub>KEY</sub>: put a random string
    -   ADMIN<sub>USER</sub>/<sub>PASSWORD</sub>: reserved for future enhancement
    -   MAIL<sub>USERNAME</sub>: your gmail username
    -   MAIL<sub>PASSWORD</sub>: your app password.  you need to manyally obtain one.  See [google help](https://support.google.com/accounts/answer/185833?hl=en)

    {
        "SECRET_KEY": "hard to memorize string",
        "ADMIN_USER": "username",
        "ADMIN_PASS": "password",
        "MAIL_USERNAME": "test@gmail.com",
        "MAIL_PASSWORD": "abcd efgh hijk lmno "
    }

-   vocaBull might fail to run if it can't find secrets.json file.  In that case, you might need to specify a full path to 4th line from the bottom of config.py.  For example,

    with open("/home/yourhome/py/vbs/secrets.json") as f:

-   Initial setup

    flask initial-setup

-   Run app

    flask run

or use a proper web server

    pip install gunicorn
    gunicorn --bind 0.0.0.0:5000 vbs:app

-   Visit `localhost:5000` from web browser


<a id="orgf73bf6d"></a>

# License

Vocabull Server is under [MIT license](https://en.wikipedia.org/wiki/MIT_License).


<a id="org21d7375"></a>

# Contact

Kyosuke Achiwa - achiwa912+gmail.com (please replace + with @)

Project link: <https://github.com/achiwa912/vbs>
Blog article: <https://achiwa912.github.io/vbs_eng.html>


<a id="org12539f7"></a>

# Acknowledgments

-   Vocabull uses user management and other parts from the fabulous `Flask Web Development` (by Miguel Grinberg) [book](https://www.oreilly.com/library/view/flask-web-development/9781491991725/) and [companion github repository](https://github.com/miguelgrinberg/flasky)
-   Vocabull uses a bootstrap 4 theme `litera` from

