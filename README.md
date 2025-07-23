# Piclasso
Pikchr with classes, live on https://tdewin.github.io/piclasso/

## Know issues
To convert back to native pikchr, piclasso does replace " rpl " with " box ". The regex might replace inline text as a consequence.

# Building
The pikchr.js is being made by using the Dockerfile + data-orig.patch which patches the original pikchr.y. It also add extra properties to every other object like data-orig (box, circle), data-orig-name (name of the rule that generated this), data-orig-first (the first line for matching).

Credits to https://github.com/felixr/pikchr-wasm/blob/main/example.html for his example how to to use emscripten and a starter page

# merge.py
merge.py can be used to create a bundle offline which can then be selected in the brower
