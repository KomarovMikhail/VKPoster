from lib import *
import time
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler


app = Flask(__name__)


scheduler = BackgroundScheduler()
scheduler.start()


def job():
    try:
        make_step()
    except Exception as e:
        print('Caught exception:')
        print(e.args)


scheduler.add_job(job, 'interval', minutes=1)


@app.route('/')
def main():
    pass


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
