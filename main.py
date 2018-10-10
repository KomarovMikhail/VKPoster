from lib import *
import time
from flask import Flask


app = Flask(__name__)


@app.route('/')
def main():
    while True:
        try:
            make_step()
            time.sleep(2000)
        except Exception as e:
            print('Caught exception:')
            print(e.args)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
