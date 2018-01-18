call _clean.bat

echo Copying common bib ...

call ck copy_file report:common-bib --file=paper.bib --dir=ck-assets
if %errorlevel% neq 0 (
  echo.
  echo Error: Copying common bib failed!
  exit /b 1
)

for /R %%f in (*.tex) do (
 echo Preprocessing tex paper sources via CK: %%f

 call ck preprocess # --doc=%%f
 if %errorlevel% neq 0 (
   echo.
   echo Error: CK preprocessing failed!
   exit /b 1
 )
)

echo Compiling paper ...

pdflatex paper

bibtex paper

pdflatex paper
pdflatex paper

start paper.pdf
