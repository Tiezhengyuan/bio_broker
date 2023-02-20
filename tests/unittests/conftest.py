from datetime import datetime
from unittest import TestCase, mock, skip
from ddt import ddt, data, unpack
import os, sys

DIR_BIN = "F:\\bio_broker\\bin"
DIR_CACHE = "F:\\bio_broker\\cache"
DIR_DOWNLOAD = "F:\\bio_broker\\download"