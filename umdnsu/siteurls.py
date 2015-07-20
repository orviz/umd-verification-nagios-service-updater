from umdnsu.config import CFG
from umdnsu import log


def get_siteurls():
    with open(CFG.site_urls_file, "rb") as f:
        return dict([line.split()
                     for line in f.readlines()
                     if line.split()])


SITEURLS = get_siteurls()
