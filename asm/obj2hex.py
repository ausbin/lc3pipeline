#!/usr/bin/env python3

"""
Converts a Brandon LC-3 object file generated by as2oj to hex you can
load into a Roigisim ROM/RAM or paste into a Roigism JSON file.

This hack brought to you by Austin Adams, New Year's Eve 2017.
"""

import sys
from collections import namedtuple
from argparse import ArgumentParser

ObjectFileSegment = namedtuple('ObjectFileSegment', ('start', 'contents'))


class ObjectFile:
    """Parse a Brandon LC-3 object file"""

    # This is an LC-3 object file, so each word is 2 bytes
    WORD_SIZE = 2

    def __init__(self, objfile):
        self._segments = []

        self.parse(objfile)

    def parse(self, objfile):
        """Parse segments from `fp' until EOF."""

        while True:
            buf = objfile.read(self.WORD_SIZE)

            # EOF
            if not buf:
                break
            elif len(buf) != self.WORD_SIZE:
                raise ValueError('start address is only one byte!')

            start_addr = int.from_bytes(buf, byteorder='big')

            buf = objfile.read(self.WORD_SIZE)
            if len(buf) != self.WORD_SIZE:
                raise ValueError('short read for segment length')

            length = int.from_bytes(buf, byteorder='big')

            buf = objfile.read(length * self.WORD_SIZE)
            if len(buf) != length * self.WORD_SIZE:
                raise ValueError('short read for segment body')

            self._segments.append(ObjectFileSegment(start_addr, buf))

    def segments(self):
        """
        Return list of ObjectFileSegment instances which represent the
        segments in this object file.
        """

        return self._segments


class RoiHexdump:
    """
    Generate a Roigisim-friendly hexdump from a list of object file
    segments. Supports JSON abbreviated format or the row/column format
    supported by the load/save buttons in the edit ROM/RAM window.
    """

    def __init__(self, segments, word_size, full=False):
        self.words = []
        self.full = full
        self.word_size = word_size

        self.from_segments(segments)

    def __str__(self):
        if self.full:
            # Print a hexdump with rows and columns and stuff
            cols = 8 * self.word_size
            dump = ''
            i = 0

            while i < len(self.words):
                row_size = min(cols, len(self.words))
                dump += ' '.join(self.words[i:i + row_size])
                dump += '\n'
                i += row_size

            return dump
        else:
            return ' '.join(self.words)

    def pad(self, num_words):
        """
        Add num_words zero words at the end of the current wordlist.
        Useful for separating object file segments.
        """

        if self.full:
            self.words += ['00' * self.word_size] * num_words
        else:
            self.words.append('{}-{}'.format(num_words, '00' * self.word_size))

    def from_segments(self, segments):
        """Populate the wordlist using the object file segments provided."""

        current_addr = 0

        for segment in sorted(segments, key=lambda seg: seg.start):
            if segment.start > current_addr:
                # Need to fill in this much space
                self.pad(segment.start - current_addr)
                current_addr = segment.start

            for i in range(0, len(segment.contents), self.word_size):
                word = segment.contents[i:i + self.word_size]
                self.words.append(word.hex())

            current_addr += len(segment.contents) // self.word_size

        # For the load/store button format and just for good vibes with
        # the JSON format, zero out remaining space.
        num_addresses = 2**(8 * self.word_size)
        if num_addresses > current_addr:
            self.pad(num_addresses - current_addr)


def main(argv):
    """
    Accept a path to an LC-3 object file on the command line and convert
    it to Roi hex.
    """

    parser = ArgumentParser(prog=argv[0],
                            description='Convert Brandon LC-3 object files to '
                                        'hex ready for Roigisim RAMs/ROMs.')
    parser.add_argument('objfile', help='Path to a Brandon object file '
                                        'generated by as2obj')
    parser.add_argument('hexfile', nargs='?', default=None,
                        help="Path to which to write generated hex file. `-' "
                             "means stdout. Default: X.dat for an objfile of "
                             "X.obj")
    parser.add_argument('--full', '-f', action='store_true',
                        help="Generate full (gigantic) hexdump instead of "
                             "using Roi's JSON abbreviation syntax")
    args = parser.parse_args(argv[1:])

    with open(args.objfile, 'rb') as objfile:
        obj = ObjectFile(objfile)

    hexdump = RoiHexdump(obj.segments(), word_size=obj.WORD_SIZE,
                         full=args.full)

    if args.hexfile == '-':
        sys.stdout.write(str(hexdump))
    else:
        if args.hexfile is not None:
            hexpath = args.hexfile
        else:
            hexpath = '{}.dat'.format(args.objfile.rsplit('.', maxsplit=1)[0])

        with open(hexpath, 'w') as hexfile:
            hexfile.write(str(hexdump))

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
