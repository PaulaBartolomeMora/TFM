# Makefile for compiling the End-of-degree project (TFG)

# Trashy file formats
TRASH = *.aux *.ist *.log *.out *.sbl *.acn *.lol *.lot *.toc *.lof *.xml main-blx.bib *.bbl *.blg *.auxlock *.glo *.gls *.glg *.alg *.acr *.fls *.fdb_latexmk

# LaTeX compiler flags
FLAGS = -shell-escape

all: main clean

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
	rm -f $(TRASH)

clean_pdf:
	rm -f *.pdf
