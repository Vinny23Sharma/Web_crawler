import re
from string import punctuation
from collections import Counter

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__, static_folder="static", template_folder="templates")
pages = dict()


def get_num_of_words(link: str):
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'html.parser')

    # We get the words within paragraphs
    text_p = (''.join(s.findAll(text=True)) for s in soup.findAll('p'))
    c_p = Counter((x.rstrip(punctuation).lower() for y in text_p for x in y.split()))

    # We get the words within divs
    text_div = (''.join(s.findAll(text=True)) for s in soup.findAll('div'))
    c_div = Counter((x.rstrip(punctuation).lower() for y in text_div for x in y.split()))

    total = c_div + c_p
    return len(total)


def get_all_links(url_received, num_of_links: int):
    pattern = re.compile("^(/)")
    html = requests.get(url_received).text
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all("a", href=pattern):

        if len(pages) >= num_of_links:
            return pages

        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                new_page = link.attrs["href"]
                absolute_link = url_received + new_page
                num_of_words = get_num_of_words(absolute_link)
                pages[absolute_link] = num_of_words
                get_all_links(absolute_link, num_of_links)

    return pages


@app.route('/', methods=["POST", "GET"])
def index():
    pages.clear()
    if request.method == 'POST':
        url_received = request.form.get("url")
        num_of_links = int(request.form.get('num_of_links'))

        links = get_all_links(url_received=url_received, num_of_links=num_of_links)
        return render_template("links.html", data=links)

    return render_template("index.html", title="verification")


@app.route('/links')
def get():
    url_received = request.args.get('url')
    num_of_links = int(request.args.get('num_of_links'))

    if not url_received:
        return make_response({"message": "please provide a url"}, 400)

    links = get_all_links(url_received=url_received, num_of_links=num_of_links)

    return jsonify({"response": list(links)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
