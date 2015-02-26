#! /usr/bin/env python3

import argparse
import sys

if __name__ == '__main__':
    #Setup and parse the arguments
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('output_file', help='The name of the SVG file that the animation will be written to.',
                        type=argparse.FileType('w'))
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
