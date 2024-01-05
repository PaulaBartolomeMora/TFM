# Makefile for compiling the End-of-degree project (TFG)

# Trashy file formats
TRASH = *.aux, *.ist, *.log, *.out, *.sbl, *.acn, *.lol, *.lot, *.toc, *.lof, *.xml, *.bbl, *.blg, *.auxlock, *.glo, *.gls, *.glg, *.alg, *.acr, *.fls, *.fdb_latexmk

# LaTeX compiler flags
FLAGS = -shell-escape

all: main

dbg: main

# We need to run it twice for the refs and stuff to be picked up!
main: main.tex
	xelatex $(FLAGS) -jobname $@ $<
	bibtex main.aux
	makeglossaries main
	xelatex $(FLAGS) -jobname $@ $<
	xelatex $(FLAGS) -jobname $@ $<
	
	
.PHONY: clean clean_pdf

clean:
	rm  *.aux *.ist *.log *.out *.acn *.lol *.lot *.toc *.lof *.bbl *.blg *.auxlock *.glo *.gls *.glg *.alg *.acr

clean_pdf:
	rm *.pdf

clean2:
	Remove-Item -Path  *.aux, *.ist, *.log, *.out, *.sbl, *.acn, *.lol, *.lot, *.toc, *.lof, *.xml, *.bbl, *.blg, *.auxlock, *.glo, *.gls, *.glg, *.alg, *.acr, *.fls, *.fdb_latexmk
