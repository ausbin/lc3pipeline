# Assemble LC-3 assembly and put it in a Roigism-friendly form.

.PHONY: help clean

help:
	@echo "This Makefile will assemble LC-3 assembly and format a"
	@echo "Roigisim-friendly hexdump"
	@echo
	@echo "To use it, run \`make X.dat' for some X.asm."

%.obj: %.asm
	as2obj $<

%.dat: %.obj
	./obj2dat.py $<

clean:
	rm -f *.obj *.dat *.sym
