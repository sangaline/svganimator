# svganimator
The application svganinmator attempts to build a single animated svg out of a sequence of distinct static svg files.

# usage
usage: svganimator.py [-h] [-s STATIC_DURATION] [-t TRANSITION_DURATION]
                      [-l NUMBER_OF_LOOPS] [-p PRECISION]
                      output_file input_file [input_file ...]

positional arguments:
  output_file           The name of the SVG file that the animation will be
                        written to.
  input_file            An SVG filename for each static frame of the
                        animation.

optional arguments:
  -h, --help            show this help message and exit
  -s STATIC_DURATION, --static STATIC_DURATION
                        The number of seconds to statically display each svg.
                        (default: 1.0)
  -t TRANSITION_DURATION, --transition TRANSITION_DURATION
                        The number of seconds to transition between each svg.
                        (default: 0.0)
  -l NUMBER_OF_LOOPS, --loop NUMBER_OF_LOOPS
                        The number of times to repeat the animation. A value
                        of 0 will loop indefinitely. (default: 0)
  -p PRECISION, --precision PRECISION
                        The precision for animation timings. Can make a
                        significant difference in file sizes. (default: 6)

