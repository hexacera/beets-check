import sys
import os
import tempfile
import logging
import shutil
from contextlib import contextmanager
from StringIO import StringIO

import beets
from beets.library import Item
from beets.mediafile import MediaFile

from beetsplug import check

logging.getLogger('beets').propagate = True

class LogCapture(logging.Handler):

    def __init__(self):
        super(LogCapture, self).__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(record.msg)


@contextmanager
def captureLog(logger='beets'):
    capture = LogCapture()
    log = logging.getLogger(logger)
    log.addHandler(capture)
    try:
        yield capture.messages
    finally:
        log.removeHandler(capture)

@contextmanager
def captureStdout():
    org = sys.stdout
    sys.stdout = StringIO()
    try:
        yield sys.stdout
    finally:
        sys.stdout = org

@contextmanager
def controlStdin(input=None):
    org = sys.stdin
    sys.stdin = StringIO(input)
    sys.stdin.encoding = 'utf8'
    try:
        yield sys.stdin
    finally:
        sys.stdin = org

class TestHelper(object):

    def tearDown(self):
        if hasattr(self, 'temp_dir'):
            shutil.rmtree(self.temp_dir)

    def setupBeets(self):
        self.temp_dir = tempfile.mkdtemp()
        os.environ['BEETSDIR'] = self.temp_dir

        self.config = beets.config
        self.config.clear()
        self.config.read()

        self.config['plugins'] = ['check']
        self.config['verbose'] = True
        self.config['color'] = False

        self.libdir= os.path.join(self.temp_dir, 'libdir')
        os.mkdir(self.libdir)
        self.config['directory'] = self.libdir

        self.lib = beets.library.Library(self.config['library'].as_filename(),
                      self.libdir)

        self.fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
        
    def setupImportDir(self):
        self.import_dir = os.path.join(self.temp_dir, 'import')
        shutil.copytree(self.fixture_dir, self.import_dir)

    def setupFixtureLibrary(self):
        self.import_dir = os.path.join(self.temp_dir, 'import')
        for file in os.listdir(self.fixture_dir):
            src = os.path.join(self.fixture_dir, file)
            dst = os.path.join(self.libdir, file)
            shutil.copy(src, dst)
            item = Item(path=dst)
            item.add(self.lib)
            check.set_checksum(item)

    def modifyFile(self, path, title='a different title'):
        mediafile = MediaFile(path)
        mediafile.title = title
        mediafile.save()