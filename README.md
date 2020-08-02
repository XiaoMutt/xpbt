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
- The package will be ready in the folder xpbt/ (see below regarding the project folder explanation)

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
  
## Folder Explanation
### src/
C++ source code. The will be compiled to filed in xpbt/core/.

### swigis/
Files used to build the .i file for SWIG.

### tests/
Tests written in Python3 using unittest. Use requirement.txt to generate Python environment for the tests.

### xpbt/
The xpbt package folder.
- core/ contains the C++ files produced by SWIG. SWIG produced wrapper around C++ classes. You can directly use these 
classes, but using the classes in the other folders are encouraged. In xbpt, python holds the ownership of all objects. 
If you created an object in python and pass it to the C++ code, C++ code will not know if the object got garbage 
collected or not, which will stall the run or raise exceptions. In stead of using classed in the core/, use the 
wrapped classes in the other folder.
- other folders: contains secondary wrapped SWIG proxy class. They have python docs and types and takes care 
of the ownership/C++ memory. They also contain other useful python classes that can be used together with the 
wrapped C++ classes.

### examples/
Examples. Not added yet. Please see the tests in the tests/ folder for examples. 

## Implemented Components

### DnaKmerHasher
Hashes a DNA Kmer to an unsigned integer

### DnaKmerBloomFilter
A Bloom filter for DNA Kmers.

### Sequence
A class holds methods for DNA and RNA sequences.

### Distance
A class holds method for calculating distances between strings

### FastQ
An immutable FASTQ record class. The fastq module also provide a FASTQ File Reader.

### FastQIntegrator
An Integrator to combine FastQ's belongs to the same inital DNA molecule.

### RedBlackIntervalTree
A RedBlackIntervalTree for fast interval search.

### ReadLazyStitcher
A read1 read2 stitcher using a lazy-overlapping method.

### In Progress
- 0-based genome coordinates
- CIGAR and AlignedRead

### Proposed
- Distance::levenshtein




