#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" parse .properties file and print readable information """

import argparse
import os
import sys
import tclib.cmd as tc_cmd

# command line arguments
PARSER = argparse.ArgumentParser(
    description='Show readable information of .properties file',
)
PARSER.add_argument('file', action="store", type=str,
                    help="full path of input file")
PARSER.add_argument('-s', action="store", dest="size",
                    type=int, default=60, help="map width")


def seg_to_str(seg_data, size):
    "convert seg to str"
    char = seg_data['char']
    start = seg_data['start']
    count = seg_data['count']
    end = start + count - 1
    start = {"x": start % size, "y": (int)(start / size)}
    end = {"x": end % size, "y": (int)(end / size)}

    return "| {0:^6s} | ({1:3d}, {2:3d}) | ({3:3d}, {4:3d}) | {5:6d} |".format(
        char, start['x'], start['y'], end['x'], end['y'], count
    )


def get_full_path(arg_options):
    "check and return full path of file"
    path = arg_options.file
    if not path.endswith(".properties"):
        path = path + ".properties"

    path = os.path.realpath(path)
    if os.path.isfile(path):
        return path

    return ""


def read_prop_file(full_path):
    "read data from file"
    parsed_data = {}

    with open(full_path, "r") as property_file:
        for line in property_file:
            fields = line.split("=")
            if len(fields) < 2:
                continue

            segments = []
            segment = None
            key = fields[0]
            value = fields[1]

            prev_char = '0'
            index = 0
            for current_char in value:
                if current_char != prev_char:
                    if current_char != '0' and current_char != '\n':
                        segment = {'char': current_char,
                                   'start': index, 'count': 0}
                        segments.append(segment)
                    else:
                        segment = None
                if segment:
                    segment['count'] = segment['count'] + 1

                prev_char = current_char
                index = index + 1

            parsed_data[key] = segments

    return parsed_data


def print_prop_data(prop_data, size):
    "print all data"
    cmd = tc_cmd.INSTANCE
    for key in prop_data:
        segs = prop_data[key]
        cmd.show_data("{0:16s} | {1:3d} section(s):".format(key, len(segs)))
        cmd.show_output("-" * 45)
        cmd.show_output("| {0:^6s} | {1:^10s} | {2:^10s} | {3:^6s} |".format(
            'char', 'start', 'end', 'count'))
        cmd.show_output("-" * 45)
        for seg in segs:
            cmd.show_output(seg_to_str(seg, size))

        # print an empty line
        cmd.show_output("-" * 45)
        cmd.show_output("")


OPTIONS = PARSER.parse_args()
FULL_PATH = get_full_path(OPTIONS)
if not FULL_PATH:
    tc_cmd.INSTANCE.show_error("File [{0}] cannot be located.".format(OPTIONS.file))
    sys.exit(2)

PROP_DATA = read_prop_file(FULL_PATH)
print_prop_data(PROP_DATA, OPTIONS.size)
