#!/usr/bin/env python3

import argparse
import glob
import os
import re
from xml.etree import ElementTree as ET

def clean_string(s):
    # Replace non-alpha characters with hyphen
    s = re.sub(r'[^a-zA-Z]+', '-', s)
    # Remove leading/trailing hyphens
    s = s.strip('-')
    return s


def merge_svgs(input_dir, output_file,selectpattern):
    svg_files = glob.glob(os.path.join(input_dir, '**', '*.svg'), recursive=True)
    if not svg_files:
        print("No SVG files found in the directory.")
        return
    
    namespace = {'svg': 'http://www.w3.org/2000/svg'}
    
    ET.register_namespace('', "http://www.w3.org/2000/svg")
    merged_svg = ET.Element('{http://www.w3.org/2000/svg}svg')

    x =0
    for svg_file in svg_files:
        tree = ET.parse(svg_file)
        root = tree.getroot()

        bname = os.path.splitext(os.path.basename(svg_file))[0]
        m = selectpattern.match(bname)
        if m:
          bname = m.group(1)
        
        bname = clean_string(bname)

        viewbox = root.get('viewBox')   
        if viewbox is not None:   
            g = ET.SubElement(merged_svg, 'g', {
                'data-template-id': bname,
                'id': bname,
                'data-viewBox': root.get('viewBox'),
                'transform': "translate({} 0)".format(x)
            })
            
            for child in list(root):
                if child.tag != "{http://www.w3.org/2000/svg}defs" or child.tag.startswith("{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}"):
                    g.append(child)
           
            x += 10+float(viewbox.strip().split()[2])
            print("Merged ",bname,"from",svg_file)
        else:
          print("could not find viewBox in {}".format(svg_file))

    tree = ET.ElementTree(merged_svg)
    tree.write(output_file)
    print(f"Merged SVG saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Merge all SVG files in a directory into one.")
    parser.add_argument("--input_dir","-i", default="icons", help="Directory containing SVG files")
    parser.add_argument("--output_file","-o", default="bundle.svg", help="Path to the output merged SVG file")
    parser.add_argument("--select","-s", default="(.*)",type=str, help="Select regex for naming")
    args = parser.parse_args()

    selectpattern = re.compile(args.select)
    
    merge_svgs(args.input_dir, args.output_file,selectpattern)

if __name__ == "__main__":
    main()


