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
cat swigis/head.i >"$2"
echo "/* Add head files for this script */" >>"$2"
echo "%{" >>"$2"
scriptAddHeads "$1" "$2" ${#1}
echo -e "%};" >>"$2"

echo "/* Add head files for the package */" >>"$2"
packageAddHeads "$1" "$2" ${#1}

cat swigis/tail.i >>"$2"
