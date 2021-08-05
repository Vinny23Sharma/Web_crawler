from flask import Flask, render_template, request, redirect


app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route('/',  methods=["POST", "GET"])
def index():
    if request.method == 'POST':
        url_received= request.form.get("url")
        print(url_received)
    return render_template("index.html", title = "verification")

if __name__ == '__main__':
    app.run(port=5000)