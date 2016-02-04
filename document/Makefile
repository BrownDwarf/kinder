all: ms.pdf

%.pdf: %.tex
	pdflatex $<
	pdflatex $<
	bibtex ms
	pdflatex ms
	pdflatex ms
	mv ms.pdf final/
	mv ms.tex final/
	rm -rf *Notes.bib
	rm -rf *.log
	rm -rf *.bbl
	rm -rf *.blg
	rm -rf *.dvi
	latexdiff old/ms_20160204.tex final/ms.tex > ms.tex
	pdflatex ms
	pdflatex ms
	bibtex ms
	pdflatex ms
	pdflatex ms
	rm -rf *Notes.bib
	rm -rf *.aux
	rm -rf *.log
	rm -rf *.blg
	rm -rf *.bbl
	rm -rf *.dvi
	rm -rf *.out
	mv ms.pdf diff.pdf
	cp final/ms.tex .
	mv diff.pdf final/diff.pdf
