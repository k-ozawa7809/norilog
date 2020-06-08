import json
from datetime import datetime
from flask import Flask, render_template, redirect, request, Markup, escape
# import pdb

app = Flask(__name__)
DATA_FILE = 'norilog.json'


@app.route('/save', methods=['POST'])
def save():
    """recode"""
    start = request.form.get('start')
    finish = request.form.get('finish')
    memo = request.form.get('memo')
    created_at = datetime.now()
    save_data(start, finish, memo, created_at)

    return redirect('/')


def save_data(start, finish, memo, created_at):
    """Save recorded data
    :param start: The train station
    :type start: str
    :param finish: Station
    :type finish: str
    :parame memo: Note of getting on and off
    :type memo: str
    :param created: Date of getting on and off
    :type created_at: datetime.datetimeu
    :return None
    """

    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []

    database.insert(0, {
        "start": start,
        "finish": finish,
        "memo": memo,
        "created_at": created_at.strftime("%Y-%m-%d %H:%M")
    })

    json.dump(database, open(DATA_FILE, mode='w', encoding="utf-8"),
              indent=4, ensure_ascii=False)
    # pdb.set_trace()


def load_data():
    """Return recode data"""
    try:
        database = json.load(open(DATA_FILE, mode="r", encoding="utf-8"))
    except FileNotFoundError:
        database = []
    return database


@app.route('/')
def index():
    rides = load_data()
    return render_template('index.html', values=rides)


@app.template_filter('nl2br')
def nl2br_filter(s):
    """Replace newline character with br"""
    return escape(s).replace('\n', Markup('<br>'))


def main():
    app.run('127.0.0.1', 8000)


if __name__ == "__main__":
    app.run('0.0.0.0', 8000, debug=True)
