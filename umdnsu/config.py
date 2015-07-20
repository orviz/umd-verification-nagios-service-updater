import argparse
import logging
import os.path
import sys

from umdnsu import log


logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description=("SAM Nagios BDII "
                                                  "site URLs updater."))
    parser.add_argument("-c", "--config-file",
                        default="/etc/bdii/gip/site-urls.conf",
                        help="site-urls configuration file.")

    args = parser.parse_args()
    if not os.path.isfile(args.config_file):
        logger.error("Config file not found: '%s'" % args.config_file)
        sys.exit(100)
    return args


CFG = parse_args()
