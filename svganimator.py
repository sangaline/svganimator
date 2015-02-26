#! /usr/bin/env python3

import argparse
import sys
from copy import deepcopy
import xml.etree.ElementTree as ET
from io import IOBase

comment_string = 'Animation generated by svganimator (https://github.com/sangaline/svganimator/)'

def extract_style(element):
    keys, values = [], []
    if 'style' in element.keys():
        for pair in element.get('style').split(';'):
            if ':' in pair:
                key, value = pair.split(':')
                keys.append(key)
                values.append(value)
    return keys, values

def encode_style(element, keys, values):
    s = ''
    for i in range(len(keys)):
        s += keys[i] + ':' + values[i] + ';'
    element.set('style', s)

def set_style_attribute(element, key, value):
    keys, values = extract_style(element)
    if key in keys:
        i = keys.index(key)
        values[i] = value
    else:
        keys.append(key)
        values.append(value)
    encode_style(element, keys, values)

def get_style_attribute(element, key):
    keys, values = extract_style(element)
    if key in keys:
        return values[keys.index(key)]
    return None

class SvgAnimator(object):
    def __init__(self, static, transition, loop, precision, basic):
        self.static = static
        self.transition = transition
        self.repeatCount = str(loop) if loop > 0 else 'indefinite'
        self.precision = precision
        self.precision_string = '{:.' + str(precision) + 'g}'
        self.basic = basic

    def _generate_timings(self, number_of_frames):
        self.total_time = round((self.static+self.transition)*number_of_frames, self.precision)
        self.transition_times = ['0']
        for i in range(number_of_frames):
            first = (self.static+self.transition)*i + self.static
            second = first + self.transition
            self.transition_times.append(self.precision_string.format(first/self.total_time))
            self.transition_times.append(self.precision_string.format(second/self.total_time))
        self.duration = self.precision_string.format(self.total_time) + 's'

    def _basic_animate(self, result, frames):
        attributes = { 'attributeName' : 'opacity', 'attributeType' : 'CSS', 'begin' : '0s',
                      'dur' : self.duration, 'repeatCount' : self.repeatCount}
        for i, frame in enumerate(frames):
            g = ET.SubElement(result, 'g', { 'style' : 'opacity:' + ('1' if i == 0 else '0') + ';'})
            if i == 0 or i == len(frames)-1:
                attributes['values'] = '1;1;0;0;1' if i == 0 else '0;0;1;1;0'
                indices = [0, 1, 2, -2, -1] if i == 0 else [0, -4, -3, -2, -1]
                attributes['keyTimes'] = '{:s};{:s};{:s};{:s};{:s}'.format(*[self.transition_times[index] for index in indices])
            else:
                attributes['values'] = '0;0;1;1;0;0'
                indices = [0, i*2-1, i*2, i*2+1, i*2+2, -1]
                attributes['keyTimes'] = '{:s};{:s};{:s};{:s};{:s};{:s}'.format(*[self.transition_times[index] for index in indices])
            ET.SubElement(g, 'animate', attributes)
            g.extend(frame.getchildren())

    def _experimental_animate(self, result, frames):
        frame_children = [frame.getchildren() for frame in frames]
        child_lengths = [len(children) for children in frame_children]
        max_length = max(child_lengths)
        child_index = 0
        while True:
            if child_index >= max_length:
                return

            current_children = []
            #the node with the most children is considered most 'complete'
            best_frame = frame_children[child_lengths.index(max_length)]
            force_opacity = False
            for i, frame in enumerate(frames):
                #this is a very shallow comparison but works well in some scenarios
                if child_index >= child_lengths[i] or frame[child_index].tag != best_frame[child_index].tag:
                    copied_node = ET.Element(best_frame[child_index].tag, best_frame[child_index].attrib)
                    set_style_attribute(copied_node, 'opacity', '0')
                    force_opacity = True
                    frame.insert(child_index, copied_node)
                    frame_children[i].insert(child_index, copied_node)
                    child_lengths[i] += 1
                    max_length = max((child_lengths[i], max_length))
                current_children.append(frame_children[i][child_index])
            if force_opacity:
                for child in current_children:
                    if get_style_attribute(child, 'opacity') == None:
                        set_style_attribute(child, 'opacity', '1')

            first_frame_child = frames[0].getchildren()[child_index]
            result_child = ET.SubElement(result, first_frame_child.tag, first_frame_child.attrib)

            #apply recursively down the tree
            self._experimental_animate(result_child, current_children)
            child_index += 1

    def animate(self, output, inputs, close=True):
        roots = []
        for input in inputs:
            tree = ET.ElementTree(file=input)
            roots.append(tree.getroot())
            if close and isinstance(input, IOBase):
                input.close()
            assert roots[-1].tag.split('}')[1] == 'svg'
        self._generate_timings(len(roots))

        result = ET.Element(roots[0].tag)
        result.attrib = roots[0].attrib
        result.append(ET.Comment(comment_string))
        if self.basic:
            self._basic_animate(result, roots)
        else:
            self._experimental_animate(result, roots)

        tree = ET.ElementTree(result)
        namespace = result.tag.split('}')[0][1:]
        ET.register_namespace('', namespace)
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
    animator.animate(output=args.output_file, inputs=args.input_file, close=True)
