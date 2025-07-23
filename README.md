# Piclasso
Pikchr with classes

# Building
The pikchr.js is being made by using the Dockerfile + data-orig.patch which patches the original pikchr.y. It also add extra properties to every other object like data-orig (box, circle), data-orig-name (name of the rule that generated this), data-orig-first (the first line for matching)

# merge.py
merge.py can be used to create a bundle offline which can then be selected in the brower
