from flask import abort, json, Flask, url_for, request, jsonify
import logging
import subprocess
import time

from umdnsu.config import CFG
from umdnsu import log
from umdnsu.siteurls import SITEURLS


logger = logging.getLogger(__name__)
app = Flask(__name__)


def get_prefix_no(name):
    indexes = [k.split(name)[-1] for k in SITEURLS.keys()
                                 if k.startswith(name)]
    indexes = [k.strip('_') for k in indexes if k]
    if indexes:
        logger.debug("Found indexes for '%s': %s" % (name, indexes))
        index_max = int(max(indexes))
        logger.debug("Max index found for '%s': %s" % (name, index_max))
        lindexes = list(set(range(1, index_max)).difference(set(indexes)))
        if lindexes:
            return str(lindexes[0])
        return str(index_max+1)
    return '1'


def wait_for_bdii(max_attempts=5):
    restarted_ok = False
    c = 0
    while True:
        p = subprocess.Popen(["ldapsearch",
                              "-x",
                              "-h",
                              "localhost",
                              "-p",
                              "2170",
                              "-b",
                              "mds-vo-name=resource,o=grid"],
                             stdout=subprocess.PIPE)
        r = p.communicate()
        if not p.returncode:
            logger.debug("BDII restarted successfully.")
            restarted_ok = True
            break
        if c>=max_attempts:
            logger.error("BDII not responding after %s attempts."
                         % max_attempts)
            break
        time.sleep(5)
        c += 1
        time.sleep(5)
    return restarted_ok


@app.route('/')
def api_root():
    return 'Welcome to UMDNSU'


@app.route('/siteurls', methods=["GET", "POST"])
def api_siteurls_get():
    if request.method == "GET":
        if "name" in request.args:
            try:
                logger.info("site-url for '%s': %s"
                            % (request.args["name"],
                               SITEURLS[request.args["name"]]))
            except KeyError:
                logger.debug("Could not find site-url: %s"
                             % request.args["name"])
    elif request.method == "POST":
        if request.headers['Content-Type'] == 'application/json':
            try:
                name = request.json["name"]
            except KeyError, e:
                logger.error("400 Bad Request")
                abort(400)
        else:
            logger.debug("415 Unsupported Media Type ;")
            abort(415)

        url = "ldap://%s:2170/mds-vo-name=resource,o=grid" % request.remote_addr
        prefix_no = get_prefix_no(name)
        if prefix_no:
            prefix = ''.join([name, prefix_no])
        else:
            prefix = name
        logger.debug("Prefix set to: %s" % prefix)

        enabled = False
        if url not in SITEURLS.values():
            with open(CFG.site_urls_file, "a") as f:
                f.write("%s\t%s\n" % (prefix, url))
                enabled = True
        else:
            logger.info("URL already exists in '%s'" % CFG.site_urls_file)

        if enabled:
            subprocess.call(["/etc/init.d/bdii", "restart"])
            logger.info("BDII restarted.")
            if wait_for_bdii():
                subprocess.call("/usr/sbin/ncg.reload.sh")
                logger.info("Executed 'ncg.reload.sh' script.")
            else:
                logger.info(("Check BDII and run 'ncg.reload.sh'"
                             "script manually."))

    data = {
        "enabled": enabled,
        "prefix": prefix,
        "url": url,
    }

    r = jsonify(data)
    r.status_code = 200
    return r


def main():
    app.run(host=CFG.host,
            port=CFG.port,)
