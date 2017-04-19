#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections
import os
import re

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"output"


def get_sections(filename):
    with open(filename, 'r') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)

def get_clip(section):

    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    # Get Book Title
    clip['book'] = lines[0]

    # Get Position
    match = re.search(r'emplacement (\d+)', lines[1])
    if not match:
        return
    position = match.group(1)
    clip['position'] = int(position)

    # Get Content
    content = lines[2]

    # If note, add special char at the beginning of the line
    if lines[1].startswith('- Votre note '):
        content = '>>>' + content
    clip['content'] = content

    return clip


def export_txt(clips):
    """
    Export each book's clips to single file
    """
    
    # Reset output dir
    if os.path.isdir(OUTPUT_DIR):
        l = os.listdir(OUTPUT_DIR)
        for a in l:
            os.remove(OUTPUT_DIR + '/' + a)
    else:
        os.mkdir(OUTPUT_DIR)


    for book in clips:
        print(book)
        lines = []
        for pos in sorted(clips[book]):
            lines.append(clips[book][pos].encode('utf-8'))

        filename = os.path.join(OUTPUT_DIR, u"%s.markdown" % book)
        with open(filename, 'w') as f:
            f.write("\n\n".join(lines))

def parse_clippings():

    # Parse Clippings file
    sections = get_sections(u'My Clippings.txt')

    # For each section create a clip object
    clips = collections.defaultdict(dict)
    for section in sections:
        clip = get_clip(section)
        if clip:
            pos = clip['position']
            while(pos in clips[clip['book']]):
                pos+=1
            clips[clip['book']][pos]= clip['content']

    # save/export clips
    export_txt(clips)

if __name__ == '__main__':
    parse_clippings()
