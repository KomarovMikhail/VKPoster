from lib import *
import time


if __name__ == '__main__':
    while True:
        try:
            make_step()
            time.sleep(2000)
        except Exception as e:
            print('Caught exception:')
            print(e.args)
