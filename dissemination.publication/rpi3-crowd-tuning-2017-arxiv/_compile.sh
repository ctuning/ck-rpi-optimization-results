#!/bin/bash
source ./_clean.sh

echo "Copying common bib ..."

ck copy_file report:common-bib --file=paper.bib --dir=ck-assets
if [ "${?}" != "0" ] ; then
  echo ""
  echo "Error: Copying common bib failed!"
  exit 1
fi

for f in *.tex
do
 echo "Preprocessing tex paper sources via CK: $f"

 ck preprocess ^ --doc=$f
 if [ "${?}" != "0" ] ; then
   echo ""
   echo "Error: CK preprocessing failed!"
   exit 1
 fi
done

echo "Compiling article ..."

pdflatex paper

bibtex paper

pdflatex paper
pdflatex paper

#echo "Launching..."
#evince paper.pdf
