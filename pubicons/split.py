#!/usr/bin/env python3

#./split.py --rsvgconvert $(which rsvg-convert) --piclasso ./pikchr inception.pic
#../merge/merge.py -i . -o ../pubicons-bundle.svg

import argparse
import os
import re
import sys
import subprocess

def split_content(content):
    # Split based on pattern //begin sometext
    # This will keep the delimiter as part of the result
    parts = re.split(r'(//beginsplit\s+\S+)', content)
    
    # Combine each delimiter with its following content
    grouped = {}


    if len(parts) > 1:
        pre = parts[0]
        for i in range(1, len(parts), 2):
            header = parts[i].replace("//beginsplit ","")
            body = parts[i+1] if i+1 < len(parts) else ''
            
            grouped[header]=pre+'\n'+ body.strip()
    return grouped

def main():
    parser = argparse.ArgumentParser(description='Split content based on //begin pattern.')
    parser.add_argument('pic', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help='Input file or stdin')
    parser.add_argument('--piclasso',required=True)
    parser.add_argument('--rsvgconvert',required=True)
    parser.add_argument('--onlynew', action='store_true',
                        help='Only run the command if the output file does not already exist')

    args = parser.parse_args()

    content = args.pic.read()
    sections = split_content(content)

    
    for section in sections:
        for duplicate in section.split(","):
            picfile = f"{duplicate}.piclasso"
            svgfile = f"{duplicate}.svg"
            
            if args.onlynew and os.path.exists(picfile):
                print(f"Skipping execution: {picfile} already exists and --onlynew is set.")
                continue

            with open(picfile, 'w') as file:
                file.write(sections[section])
            
            print(f" Wrote {picfile}")

            
            # Run the shell command with the temp file as input
            piclasso = subprocess.Popen([args.piclasso,"--svg-only",picfile], stdout=subprocess.PIPE)
            rsvgconvert = subprocess.Popen([args.rsvgconvert,"-s","style.css","-f","svg","-o",svgfile,"-"], stdin=piclasso.stdout, stdout=subprocess.PIPE)

            piclasso.stdout.close()

            # Get the final output
            output, err = rsvgconvert.communicate()
            

            print(f"{svgfile} should be created")
            if output != "":
                print(f" Pipeline output {output} {err}")
            
            


if __name__ == '__main__':
    main()
