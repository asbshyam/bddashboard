
# Headers

from flask import Flask
import begin

app = Flask(__name__)


@app.route('/')
def hello():
    begin.logic()
    string = ""
    infile = open("temp.txt", "r").read()
    for line in infile.splitlines():
        string += str(line.split(",")[1]) + str("<br>")
        print string
    return string

if __name__ == '__main__':
    app.run()
