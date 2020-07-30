function build_xpbt_i() {
  function scriptAddHeads() {
    for file in "$1"/*; do
      if [ -d "$file" ]; then
        scriptAddHeads "$file" "$2" "$3"
      else
        if [ "${file: -2}" == ".h" ]; then
          echo "#include \"${file:$3+1}\"" >>"$2"
        fi
      fi
    done
  }
  function packageAddHeads() {
    for file in "$1"/*; do
      if [ -d "$file" ]; then
        packageAddHeads "$file" "$2" "$3"
      else
        if [ "${file: -2}" == ".h" ]; then
          echo "%include \"${file:$3+1}\"" >>"$2"
        fi
      fi
    done
  }

  cat xpbt_template.i >"$2"
  echo "/* Add head files for this script */" >>"$2"
  echo "%{" >>"$2"
  scriptAddHeads "$1" "$2" ${#1}
  echo -e "%};" >>"$2"

  echo "/* Add head files for the package */" >>"$2"
  packageAddHeads "$1" "$2" ${#1}
}

echo "###Create tmp folder..."
mkdir tmp

echo "###Build xpbt.i"
build_xpbt_i src src/xpbt.i

echo "###Create SWIG wrap files..."
swig -python -c++ -I./src -outdir ./xpbt ./src/xpbt.i

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

echo "###Pack " "${ofiles[@]}" "into _xpbt.so..."
g++ -shared "${ofiles[@]}" -o ./xpbt/_xpbt.so

echo "###Remove tmp files"
rm -r ./tmp
echo "###Remove xpbi.i"
rm ./src/xpbt.i

echo "###Remove xpbt_wrap.cxx"
rm ./src/xpbt_wrap.cxx
