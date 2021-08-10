import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify, make_response

app = Flask(__name__, static_folder="static", template_folder="templates")
pages = set()


def get_all_links(url_received):
    pattern = re.compile("^(/)")
    html = requests.get(url_received).text
    soup = BeautifulSoup(html, 'html.parser')

    for link in soup.find_all("a", href=pattern):

        if len(pages) >= 100:
            return pages

        if "href" in link.attrs:
            if link.attrs["href"] not in pages:
                new_page = link.attrs["href"]
                absolute_link = url_received + new_page
                print(absolute_link)
                pages.add(absolute_link)
                get_all_links(absolute_link)

    return pages


@app.route('/', methods=["POST", "GET"])
def index():
    pages.clear()
    if request.method == 'POST':
        url_received = request.form.get("url")
        print(url_received)

        links = get_all_links(url_received)
        print(len(links))
        return render_template("links.html", data=links)

    return render_template("index.html", title="verification")


@app.route('/links')
def get():
    url_received = request.args.get('url')
    if not url_received:
        return make_response({"message": "please provide a url"}, 400)

    links = get_all_links(url_received=url_received)

    return jsonify({"response": list(links)})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
