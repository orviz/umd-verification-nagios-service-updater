import logging
from logging import StreamHandler

default_formatter = logging.Formatter(\
   "%(asctime)s:%(levelname)s:%(message)s")

default_handler = StreamHandler()
default_handler.setFormatter(default_formatter)

root = logging.getLogger()
root.addHandler(default_handler)
root.setLevel(logging.DEBUG)
