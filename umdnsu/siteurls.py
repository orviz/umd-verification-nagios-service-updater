from umdnsu.config import CFG
from umdnsu import log


logger = logging.getLogger(__name__)


def get_siteurls():
    with open(CFG.config_file, "rb") as f:
        return dict([line.split()
                     for line in f.readlines()
                     if line.split()])


SITEURLS = get_siteurls()
