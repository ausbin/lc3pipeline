%.obj: %.asm
	as2obj $<

%.hex: %.obj
	tail -c +5 hello.obj | xxd -c 2 -p | tr '\n' ' ' | sed -s 's/ $$//g' >$@

%: %.hex
	xclip -i -selection clipboard <$<
