import argparse
import logging
import os.path
import sys

from umdnsu import log


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description=("SAM Nagios BDII "
                                                  "site URLs updater."))
    parser.add_argument("-i", "--host",
                        default="127.0.0.1",
                        help="interface to listen.")
    parser.add_argument("-p", "--port",
                        default="8080",
                        type=int,
                        help="port to listen.")
    parser.add_argument("-f", "--site-urls-file",
                        default="/etc/bdii/gip/site-urls.conf",
                        help="site-urls configuration file.")

    args = parser.parse_args()
    if not os.path.isfile(args.site_urls_file):
        logger.debug("Config file not found: '%s'" % args.site_urls_file)
        with open(args.site_urls_file, "w+"): pass
        logger.debug("Config file '%s' created" % args.site_urls_file)
    logger.info("Using site-urls file: %s" % args.site_urls_file)
    return args


CFG = parse_args()
