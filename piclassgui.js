function wrapsource(source,title) {
    const wrappedsource = `//piclass preamble, non default pikchr definitions
//based on veeam coloring scheme https://www.veeam.com/company/brand-resource-center.html
$grey = 0x505861
$lightgrey = 0xf0f0f0
$purple = 0x8e71f4
$green = 0x00d15f

color = $grey
linerad = 0.1
arrowht = 0.1
arrowwid = 0.12
fontscale = 1.5
boxwid = 1
boxht = 1

$o = boxht/8
$oh = $o/2
$o2 = $o*2
$o3 = $o*3
$o4 = $o*4
$o5 = $o*5
$o6 = $o*6
$o7 = $o*7
$o8 = $o*8
$mh = -$oh
$m2 = -$o2
$m3 = -$o3
$m4 = -$o4
$m5 = -$o5
$m6 = -$o6
$m7 = -$o7
$m8 = -$o8
$margin = $o2

define title { TITLE:text "${title}" with $1 at $2}
define titledBox {
 $minleft = max($1.w.x-$2.nw.x,0)+$margin
 $minright = max($2.ne.x-$1.e.x,0)+$margin
 line from $1.w left $minleft\
 then down until even with $2.sw -(0,$margin)\
 then right until even with $1.e\
 then right $minright\
 then up until even with $1.e\
 then left until even with $1.e\
 then to $1.e rad 0.2 color $3 thickness 200% 
}

//below icon label
define blbl { text with .n at $1.s $3 color $2;move to $1.end}
//above icon label
define albl { text with .s at $1.n $3 color $2;move to $1.end}

define conn { line from $1 to previous dot.n color $grey chop }
define netdot { dot at $1 vertex of NET color $grey rad 0.05;conn($2) }

//end piclass preamble

`+source;
return wrappedsource
}