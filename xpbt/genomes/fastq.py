import gzip
from xpbt.core import FastQ
import xpbt.core


class FastQIntegrator(xpbt.core.FastQIntegrator):
    def __init__(self):
        """
        Combine a collection of FastQs:
        * pick the base based a the collective phred qualities
        * update the Phred quality based on bayes updates

        Example:  Unique Molecule Barcodes show that a group of FastQs which are from the same initial DNA molecules.
        Then these FastQs can be added to the FastQIntegrator, and the initial DNA sequence as well as the sequencing
        quality can be deduced.
        """
        super(FastQIntegrator, self).__init__()

    def add(self, fastq: FastQ) -> None:
        """
        Add a FastQ record. The FastQ object is not stored, but the information is extracted for calculation
        :param fastq:
        :return: None
        """
        super(FastQIntegrator, self).add(fastq)

    def integrate(self, newId: str = "Integrated") -> FastQ:
        """
        Integrate the added FastQs to a new FastQ
        :param newId: the new ID given to the resulted FastQ
        :return: the integrated FastQ
        """
        return super(FastQIntegrator, self).integrate(newId)

    @staticmethod
    def p2phred(p) -> str:
        """
        Convert probability to Phred character
        :return: Phred character
        """
        return FastQIntegrator.p2phred(p)

    @staticmethod
    def phred2p(c) -> float:
        """
        Convert Phred character to probability
        :param c:
        :return: probability
        """
        return FastQIntegrator.phred2p(c)

    @staticmethod
    def count2ascii(c) -> str:
        """
        Convert base count (an integer) to a character.
        Mapping is chr(min(32+c, 126)).

        :param c: base count
        :return: a character
        """
        return FastQIntegrator.count2ascii(c)

    @staticmethod
    def ascii2count(c) -> int:
        """
        Convert base count character back to count.

        :param c: the count character
        :return: the count
        """
        return FastQIntegrator.ascii2count(c)

    @staticmethod
    def integratePair(fastq1: FastQ, fastq2: FastQ, newId: str = "integrated") -> FastQ:
        """
        Integrate a pair of FastQs.
        :param fastq1:
        :param fastq2:
        :param newId: the new ID given to the resulting FastQ
        :return: Integrated FastQ
        """
        return FastQIntegrator.integratePair(fastq1, fastq2, newId)


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
