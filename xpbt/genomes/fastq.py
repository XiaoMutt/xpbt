import gzip
from xpbt.core import FastQ
import xpbt.core


class FastQIntegrator(xpbt.core.FastQIntegrator):
    pass


class Reader(object):
    def __init__(self, file_path: str):
        self._file_path = file_path
        self._file_handler = None

    def open(self):
        if self._file_handler is None:
            if self._file_path.endswith(".gz"):
                self._file_handler = gzip.open(self._file_path, "rb")
            else:
                self._file_handler = open(self._file_path, "rb")
        else:
            self._file_handler.seek(0)

    def close(self):
        if self._file_handler is not None:
            self._file_handler.close()
            self._file_handler = None

    def __enter__(self):
        self.open()
        return self

    def __iter__(self):
        self.open()
        return self

    def __next__(self):
        def next_line():
            return next(self._file_handler).decode().strip('\n')

        while True:
            name = next_line()
            if name.startswith('@'):
                break
        seq = next_line()
        desc = next_line()
        qual = next_line()
        if not desc.startswith('+') or len(seq) != len(qual):
            raise Exception("The file is not in FASTQ format")

        return FastQ(name[1:], seq, desc[1:], qual)

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
