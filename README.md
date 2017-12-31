Pipelined LC-3 CPU
==================

To get some time to play around with [Roi Atalla's shiny new circuit
simulator][1] I/we hope to use in future semesters in CS 2110 at Georgia
Tech, I'm gonna try to make a pipelined [LC-3][2] processor in this
repo.

Shoutout to my main man Conte.

Assembler
---------

The `/asm/` directory of this repository includes a Makefile and Python
3.5+ script that will assemble LC-3 assembly into a `.dat` file ready
for loading into Roigisim. Really, this just means running [Brandon's
LC-3 assembler, `as2obj`][3], parsing the LC-3 object file it produces,
and writing that in a hexdump format compatible with Roigisim.

[1]: https://github.com/ra4king/CircuitSim
[2]: https://en.wikipedia.org/wiki/LC-3
[3]: https://github.com/TricksterGuy/complx
