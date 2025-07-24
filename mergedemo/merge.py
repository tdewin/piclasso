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



def recursive_remove(parent):
    for child in list(parent):
        bgs = ['OLS_ICONS','BG','BG-2']
        if ( child.tag.endswith('rect') and child.get('id') in bgs ):
            print("gotcha",child.get('id'))
            parent.remove(child)
        elif ( child.tag.endswith('g') and child.get('id') in bgs) :
            print("gotg",child.get('id'))
            parent.remove(child)
        else:
            recursive_remove(child)

def replace_class_by_style(parent,styles):
   for child in list(parent):
       if child.get("class"):
           classes = child.get("class")
           styleline = []
           for cls in classes.split(" "):
                cls = cls.strip()
                if cls in styles:
                   for k in styles[cls]:
                       styleline.append("{}:{}".format(k,styles[cls][k]))
                else:
                   print("ERR: unmatched style",cls)

           child.set("class","")
           child.set("style",";".join(styleline))
           #print(child.get("style"))

       replace_class_by_style(child,styles)  

def find_style_element(root):
    # Search recursively for <style> elements
    for elem in root.iter():
        if elem.tag.endswith('style'):
            return elem  # Return the first <style> element found

    return None


def parse_css(css_text):
    class_styles = {}
    # Match blocks like ".cls-1, .cls-2 { ... }"
    blocks = re.findall(r'([^{]+)\{([^}]+)\}', css_text)
    for selectors, properties in blocks:
        selector_list = [s.strip().lstrip('.') for s in selectors.split(',')]


        for prop in properties.strip().split(';'):
            if ':' in prop:
                key, value = map(str.strip, prop.split(':', 1))
                for selector in selector_list:
                    if not selector in class_styles:
                        class_styles[selector] = {}
                    class_styles[selector][key] = value

    return class_styles

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

        basename = os.path.basename(svg_file)
        bname = os.path.splitext(basename)[0]
        m = selectpattern.match(bname)
        if m:
          bname = m.group(1)
        
        bname = clean_string(bname)

        viewbox = root.get('viewBox')   
        if viewbox is not None:   
            g = ET.SubElement(merged_svg, 'g', {
                'data-template-id': bname,
                'id': basename,
                'data-viewBox': root.get('viewBox'),
                'transform': "translate({} 0)".format(x)
            })
            #<rect id="BG" class="cls-2" width="50" height="50"/>
            recursive_remove(root)

            style = find_style_element(root)
            if style != None:
                styles = parse_css(style.text)
                replace_class_by_style(root,styles)
            else:
                print("couldnt find style")

            
            for child in list(root):
                if child.tag != "{http://www.w3.org/2000/svg}defs":
                    if child.tag.startswith("{http://www.w3.org/2000/svg}"):
                        g.append(child)
                    
           
            x += 10+float(viewbox.strip().split()[2])
            print("Merged {} from \"{}\"".format(bname,svg_file))
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


