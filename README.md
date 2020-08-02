# xpbt (xiao's probability-based biological tools)
The xpbt package is a high-performance package for python focusing on probability-based tools and algorithms. The package is written in C++ and is built to python package using SWIG.

## Installation on Ubuntu
- Install PCRE which is required by SWIG.
```shell script
apt-get install libpcre3 libpcre3-dev # you may need sudo
```
- Install [SWIG](http://www.swig.org/Doc3.0/Preface.html#Preface_unix_installation). In brief, download SWIG and install to the default location:
```shell script
./configure
make
make install # you may need sudo
```
- Install Python3 dev package.
```shell script
apt-get install python3-dev # you may need sudo
```
- Build xpbt python module using the provided pack.sh file. The xpbt.py (python module) and _xpbt.so (compiled code) files in the dist/ folder are the module files for python.
```shell script
bash pack.sh
```
- Note: depending on the python3 version on your system, you may need to change the -I/usr/include/python3.7 version accordingly in the following command in the pack.sh:
```shell script
g++ -fPIC -c -O2 -std=c++11 ./src/xpbt_wrap.cxx -I/usr/include/python3.7 -lstdc++ -o ./tmp/xpbt_wrap.o
```

- To use the Tests and Examples in Python
  - Install python venv
  ```shell script
  apt-get install python3-venv
  ```
  - Create venv
  ```shell script
  python3 -m venv venv
  venv/bin/pip install -r requirement.txt
  ```

## Examples
Not added yet. Please see the tests in the tests folder for examples. 

## Tests
Tests are written in Python3 using unittest. Use requirement.txt to generate Python environment for test.

## Components
### RandomDnaKmer
This is a class to generate random DNA K-mer. A k-mer is a DNA sequence with length K.

#### Interface

### DnaKmerHasher
Hashes a DNA K-mer to an unsigned integer
#### Interface
```python
class DnaKmerHasher(object):
    def __init__(self, kmerLength: int, bitWidth: int):
        # kmerLength: the length of the K-mer, i.e. the K
        # bitWidth: the K-mer will be hashed to an integer 
        # uniformly distributed in  [0, 2^bitWidth-1)
        pass

    def __init2__(self, string:str):
        # string is a string created by DnaKmerHasher.str()
        pass

    def str(self)->str:
        # save the DnaKmerHasher to a string,
        pass

    def hash(self, kmer: str)->int:
        # hash the kmer to an integer
        # this function does not check the length of the kmer
        # and the length of the kmer must equal to the kmerLength set in the __init__
        pass
```     


### DnaKmerBloomFilter
A Bloom filter for DNA K-mers.
#### Interface
```python
class DnaKmerBloomFilter(object):
    def __init__(self, kmerLength: int, falsePositiveRate: float, storageBitWidth: int):
        # kmerLength: the length of the K-mer, i.e. the K
        # falsePositiveRate: the false positive rate of the Bloom filter
        # storageBitWidth: the storage space of the Bloom filter is 2^storageBitWith/8 bytes. This must be [4, 32]
        pass

    def __init2__(self, kmerLength: int, numOfKmers: int, storageBitWidth: int):
        # kmerLength: the length of the K-mer, i.e. the K
        # numOfKmers: maximum number of K-mers to store. ATTENTION: use 1e6 is a float number and do not use this kind of expression for numOfKmers of this constructor
        # storageBitWidth: the storage space of the Bloom filter is 2^storageBitWith/8 bytes. This must be [4, 32]
        pass

    def __init3__(self, fileName: str):
        # load the Bloom filter from the file indicated by the fileName
        pass

    def add(self, dna: str)->bool:
        # add dna in to the Bloom filter
        # the length of the dna must be the same as kmerLength set by the constructor
        # return True if the Bloom filter did not contain this dna and it has been added
        # return False if the Bloom filter already contains this dna and there is no need to add it
        pass
    
    def contains(self, dna: str)->bool:
        # return True if the Bloom filter contains the dna; otherwise False.
        pass
    
    def getKmerK(self)->int:
        # return the length of the K-mer
        pass
    
    def getFalsePositiveRate(self)->float:
        # return the false positive rate of the Bloom filter
        pass
    
    def getMaxCapacity(self)-> int:
        # return the max number of K-mers can be added to the Bloom filter 
        # under the constrain of the falsePositiveRate and the storageBitWidth
        pass
    
    def getStorageBitSize(self)->int:
        # return the storage size of the Bloom filter in bits
        pass

    def saveToFile(self, fileName:str):
        # save the Bloom to the fileName
        pass
    
```
### Distance
A class holds methods for calculating distance.
#### Interface

```python
class Distance(object):
    @staticmethod
    def hamming(a:str, b:str)->int:
        # return the hamming distance between the two strings
        pass
```
### Sequence
A class holds methods for DNA and RNA sequences.
#### Interface
```python
class Sequences(object):
    @staticmethod
    def reverse(seq: str)->str:
        # reverse a string (no need to be a DNA or RNA sequence)
        pass
    
    @staticmethod
    def complementDna(dna: str)->str:
        # complement a DNA sequence
        pass

    @staticmethod
    def complementRna(dna: str)->str:
        # complement a RNA sequence
        pass

    @staticmethod
    def reverseComplementDna(dna: str)->str:
        # reverse and complement a DNA sequence
        pass

    @staticmethod
    def reverseComplementRna(dna: str)->str:
        # reverse and complement a RNA sequence
        pass
    
    @staticmethod
    def randomDnaKmer(k:int)->str:
        # generate a random DNA sequence with length k, i.e. generate a random Kmer
        pass

    @staticmethod
    def randomRnaKmer(k:int)->str:
        # generate a random RNA sequence with length k, i.e. generate a random Kmer
        pass
```
    
### Testing (Need More Tests)
- FastQ (FastQ)
- Multiple Fastq records combine into one (including quality score) (FastQIntegrator)
- Read1 and Read2 Stitch (ReadStitcher)

### In Progress
- 0-based genome coordinates
- RedBlackIntervalTree for AlignedSegments
- Class wrapping for a better interface with Python

### Proposed
- Distance::levenshtein




