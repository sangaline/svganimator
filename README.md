# svganimator
The application svganinmator attempts to build a single animated SVG out of a sequence of distinct static SVG files. It's not a substitute for using proper tools to create animated SVG files but it can be helpful if you're using an external library to generate images and it doesn't allow for animations. If you're in that situation then it's worth a try.

If you run it with the --basic option it will group each input image into a separate frame and then animate between them. This can result in very large file sizes as any redundant elements are included multiple times but it will probably produce a working animation as long as the individual frames weren't already animated or interactive. It does compare favorably to fetching a number of different SVG files and then cycling between them using css or javascript because it reduces the number of file requests and allows all of the frames to be compressed at once. This tends to result in a smaller overall size than the separately compressed SVG files due to the increased redundancy.

Without the --basic option, svganimator will attempt to find matching elements between frames an animate between them. This allows for smooth transitions between frames and also dramatically reduces the file sizes. This is relatively fragile at the moment but when it does work it can produce some pretty cool results. It works best in scenarios where you're using SVG files that are likely very similar in structure, which is often the case when using an external library that programatically generates the images.

# gallery
Here are a couple of simple examples that were generated from SVG images constructed using matplotlib. 

Note that you have to wait a very long time because the animations are quite. Just kidding, github blocks SVG due to XSS concerns so you need to click through each image to see the animation.

<a href="http://nuclear.ucdavis.edu/~sangaline/github/svganimator/morphing_histograms.svg">
<img src="http://nuclear.ucdavis.edu/~sangaline/github/svganimator/morphing_histograms.png" />
</a>

<a href="http://nuclear.ucdavis.edu/~sangaline/github/svganimator/animated_time_series.svg">
<img src="http://nuclear.ucdavis.edu/~sangaline/github/svganimator/animated_time_series.png" />
</a>

# usage
```
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
  -b, --basic           Basic mode. This is more likely to work but will have
                        larger file sizes and transitions will only be fades
                        not interpolations. (default: False)
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
```
