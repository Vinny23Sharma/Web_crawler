from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        pages = set()
        url_received = request.form.get("url")
        print(url_received)

        pattern = re.compile("^(/)")
        html = requests.get(url_received).text
        soup = BeautifulSoup(html, 'html.parser')

        for link in soup.find_all("a", href=pattern):
            if "href" in link.attrs:
                if link.attrs["href"] not in pages:
                    new_page = link.attrs["href"]
                    print(url_received+new_page)
                    pages.add(url_received+new_page)

    return render_template("index.html", title="verification")


if __name__ == '__main__':
    app.run(port=5000)
