def get_siteurls():
    with open("site-urls.conf", "rb") as f:
        return dict([line.split()
                     for line in f.readlines()
                     if line.split()])

SITEURLS = get_siteurls()
SITEURLS_FNAME = "site-urls.conf"
