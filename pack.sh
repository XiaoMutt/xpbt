
echo "###Create tmp folder..."
mkdir tmp

echo "###Build xpbt.i"
bash swigis/buildi.sh src src/xpbt.i

echo "###Create SWIG wrap files..."
swig -python -c++ -I./src -outdir ./xpbt/core ./src/xpbt.i

ofiles=() # track o files
echo "###Compile c++ files..."
for f in ./src/*.cpp; do
  ofile=${f##*/}
  ofile="./tmp/${ofile%.*}.o"
  echo "${f}->${ofile}"
  g++ -fPIC -c -O2 -std=c++11 "${f}" -lstdc++ -o "${ofile}"
  ofiles+=("${ofile}")
done

echo "###Compile xpbt cxx file..."
g++ -fPIC -c -O2 -std=c++11 ./src/xpbt_wrap.cxx -I/usr/include/python3.8 -lstdc++ -o ./tmp/xpbt_wrap.o
ofiles+=("./tmp/xpbt_wrap.o")

echo "### Make xbpt.core/..."
mkdir xbpt/core

echo "# This module contains the SWIG-ported C++ classes" > ./xpbt/core/__init__.py
echo "from .xpbt import *" >> ./xpbt/core/__init__.py

echo "###Pack " "${ofiles[@]}" "into xpbt/core/_xpbt.so..."
g++ -shared "${ofiles[@]}" -o ./xpbt/core/_xpbt.so

echo "###Remove tmp files"
rm -r ./tmp
echo "###Remove xpbi.i"
rm ./src/xpbt.i

echo "###Remove xpbt_wrap.cxx"
rm ./src/xpbt_wrap.cxx
