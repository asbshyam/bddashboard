
# Headers

from flask import Flask
import begin

app = Flask(__name__)


@app.route('/test')
def test():
    begin.logic()
    string = ""
    infile = open("data/temp.txt", "r").read()
    for line in infile.splitlines():
        string += str(line.split(",")[1]) + str("<br>")
        print string
    return string


@app.route('/')
def root():
    string = "<html><title>Test</title><body><a href=\"test\">Test Page</body></html>"
    return string

if __name__ == '__main__':
    app.run(host='0.0.0.0')
