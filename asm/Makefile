# Run `make X' to assemble X.asm and put a Roigisim JSON-friendly hex
# representation of it into the clipboard.

.PHONY: help clean

help:
	@echo "This Makefile will assemble LC-3 assembly and put a Roigisim JSON-friendly"
	@echo "hex representation in your clipboard."
	@echo
	@echo "To use it, run \`make X' for some X.asm."

%.obj: %.asm
	as2obj $<

%.hex: %.obj
	./obj2hex.py $<

%: %.hex
	xclip -i -selection clipboard <$<

clean:
	rm -f *.obj *.hex
