import os
import logging

filepath = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename=filepath + '\log.log',level=logging.INFO)

if __name__ == "__main__":

    from app import main
