from flask import Flask, render_template, request, jsonify, abort, make_response
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__, static_folder="static", template_folder="templates")


def get_all_links(url_received):
    pages = set()
    pattern = re.compile("^(/)")
    html = requests.get(url_received).text
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all("a", href=pattern):
        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                new_page = link.attrs["href"]
                print(url_received + new_page)
                pages.add(url_received + new_page)

    return pages


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        url_received = request.form.get("url")
        print(url_received)

        pages = get_all_links(url_received)
        print(pages)

    return render_template("index.html", title="verification")


@app.route('/links')
def get():
    url_received = request.args.get('url')
    if not url_received:
        return make_response({"message": "please provide a url"}, 400)

    pages = get_all_links(url_received=url_received)

    return jsonify({"response": list(pages)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
