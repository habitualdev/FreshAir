import datetime
from flask import Flask, jsonify, render_template, request
import copy
import re

app = Flask(__name__)


class twitter_data:
    def __init__(self):
        self.table = []
        self.username = ""
        self.ban = []
        self.words = []
        self.html = ""
        self.reset = 0


init = twitter_data()
init.username = "habitual_dev"
init.table = []
init.html = ""

with open("ban.list") as fban:
    text = fban.read().split(",")
    for asshole in text:
        init.ban.append(asshole)

with open("badword.list") as fbad:
    text = fbad.read().split(",")
    for badword in text:
        init.words.append(badword)

def scrape(streamer):
    init.username = streamer
    import twint
    n = 0
    while True:
        if init.reset == 1:
            init.table = []
            init.reset = 0
        i = 0
        x = datetime.datetime.now()
        c = twint.Config()
        c.Since = str(x.year) + "-" + str(x.month) + "-" + str(x.day)
        c.Hide_output = True
        c.Search = str("@") + init.username
        c.Limit = 1000
        c.Pandas = True
        twint.run.Search(c)
        dataframe = twint.storage.panda.Tweets_df
        data_dict = dataframe.to_dict()
        data_user = data_dict["username"]
        data_data = data_dict["tweet"]
        data_timestamp = data_dict["date"]



        for line in data_data:
            name_matched = False
            word_match = False
            data_entry = str(data_timestamp[line]) + " : " + str(data_user[line]) + " : " + data_data[line]
            for table_line in init.table:
                if data_entry in table_line["tweet"]:
                    name_matched = True
            if not name_matched:
                if data_user[line] not in init.ban:
                    for badword in init.words:
                        if re.search(badword, data_entry):
                            word_match = True
                    if not word_match:
                        init.table.append({"timestamp": data_timestamp[line], "tweet": data_entry})


@app.route('/_display')
def return_html():
    init.html = "<body>\n<div style='background: rgb(124,172,217);'> " "____Timestamp____:____User____:____Tweet____  " + "</div> <hr>\n\r"

    working_table = copy.deepcopy(init.table)
    working_table.sort(key=lambda x: x["timestamp"])
    working_table.reverse()
    try:

        for entry in working_table:
            init.html = init.html + "<div style='background: rgb(124,172,217);'> " + entry["tweet"] + "</div> <hr>\n\r"
    except:
        init.html = init.html + "<div style='background-color: white;'> " + "</div> <hr>\n\r"
    init.html = init.html + "</body>"
    return init.html


@app.route('/_start')
def start():
    streamer = request.args.get('streamer', 0, type=str)
    scrape(streamer)
    return "Success"


@app.route('/_add_ban')
def add_name():
    name = request.args.get('name', 0, type=str)
    init.ban.append(name)
    init.reset = 1
    return jsonify(result="Success")


@app.route('/_add_word')
def add_word():
    name = request.args.get('word', 0, type=str)
    init.words.append(name)
    init.reset = 1
    return jsonify(result="Success")


@app.route('/_restart')
def restart():
    init.ban = ["realdonaldtrump"]
    init.words = ["fuck","bitch"]
    init.html = ""
    init.table = []
    return jsonify(result="Success")


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
