#! /usr/bin/env python3

import argparse
import sys
from copy import deepcopy
import xml.etree.ElementTree as ET
from io import IOBase

class SvgAnimator(object):
    def __init__(self, static, transition, loop, precision, basic):
        self.static = static
        self.transition = transition
        self.loop = loop
        self.precision = precision
        self.basic = basic

    def Animate(self, output, inputs, close=True):
        roots = []
        for input in inputs:
            tree = ET.ElementTree(file=input)
            roots.append(tree.getroot())
            if close and isinstance(input, IOBase):
                input.close()
            assert roots[-1].tag.split('}')[1] == 'svg'
        result = ET.Element(roots[0].tag)

        tree = ET.ElementTree(result)
        tree.write(output)
        if close and isinstance(output, IOBase):
            output.close()

if __name__ == '__main__':
    #Setup and parse the arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('output_file', help='The name of the SVG file that the animation will be written to.',
                        type=argparse.FileType('wb'))
    parser.add_argument('-b', '--basic', help='Basic mode. This is more likely to work but will have larger file sizes and ' +
                        'transitions will only be fades not interpolations.', action='store_true')
    parser.add_argument('-s', '--static', help='The number of seconds to statically display each svg.',
                        type=float, default = 1.0, metavar='STATIC_DURATION')
    parser.add_argument('-t', '--transition', help='The number of seconds to transition between each svg.',
                        type=float, default = 0.0, metavar='TRANSITION_DURATION')
    parser.add_argument('-l', '--loop', help='The number of times to repeat the animation. A value of 0 will loop indefinitely.',
                        type=int, default=0, metavar='NUMBER_OF_LOOPS')
    parser.add_argument('-p', '--precision', help='The precision for animation timings. Can make a significant difference in file sizes.',
                        type=int, default=6)
    parser.add_argument('input_file', help='An SVG filename for each static frame of the animation.',
                        type=argparse.FileType('r'), nargs='+')
    args = parser.parse_args()

    if len(args.input_file) == 1:
        args.output_file.write(args.input_file[0].read())
        args.output_file.close()
        args.input_file[0].close()
        sys.exit()

    animator = SvgAnimator(static=args.static, transition=args.transition, loop=args.loop,
                           precision=args.precision, basic=args.basic)
    animator.Animate(output=args.output_file, inputs=args.input_file, close=True)
