# Run `make X' to assemble X.asm and put a Roigisim JSON-friendly hex
# representation of it into the clipboard.

.PHONY: help

help:
	@echo "This Makefile will assemble LC-3 assembly and put a Roigisim JSON-friendly"
	@echo "hex representation in your clipboard."
	@echo
	@echo "To use it, run \`make X' for some X.asm."

%.obj: %.asm
	as2obj $<

%.hex: %.obj
	tail -c +5 hello.obj | xxd -c 2 -p | tr '\n' ' ' | sed -s 's/ $$//g' >$@

%: %.hex
	xclip -i -selection clipboard <$<
