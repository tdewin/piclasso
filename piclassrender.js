function postrender(svgelement,catalog) {
    candidates = svgelement.getElementsByTagName("g")

    blankpre = `<rect fill="#506060" width="100" height="100" rx="15" ry="15" id="rect1" x="0" y="0" />`
    blankpretext = `<text x="50" y="60" fill="#fff" font-family="${fontfamily}" font-size="18px" stroke-width="0" text-align="center" text-anchor="middle"  style="line-height:0.9;text-decoration-color:#000000" xml:space="preserve">`
    blankpost = `</text>`


    for(let i=0;i <candidates.length;i++) {
        let g = candidates[i];
        if (g.attributes["data-orig"] && g.attributes["data-orig-first"] && g.attributes["data-orig"].value == 'rpl') {
            let n = g.attributes["data-orig-first"].value
            let fht = g.attributes["data-future-height"].value
            let fwid = g.attributes["data-future-width"].value
            
            if (n in catalog) {
                let item = catalog[n]
                let vb = item["viewBox"]

                let scalewid = fwid/(vb[2]-vb[0])
                let scaleht = fht/(vb[3]-vb[1])

                while(g.firstChild) { g.removeChild(g.firstChild) }
                g.innerHTML = item["inner"]
                let transform = g.attributes["transform"]

                transform.value = `${transform.value} scale(${scalewid} ${scaleht})`
             } else {
                let scalewid = fwid/100
                let scaleht = fht/100
                let transform = g.attributes["transform"]
                while(g.firstChild) { g.removeChild(g.firstChild) }

                
                ratio = fht / fwid
                scalex = 1
                scaley = 1
                fontreset = 0

                if (ratio > 1) {
                  scaley = 1/ratio
                } else {
                  scalex = ratio
                  fontreset = ((50/ratio)-50)
                }

                g.innerHTML = blankpre+`<g transform="scale(${scalex} ${scaley}) translate(${fontreset} 0)">`+blankpretext+n+blankpost+`</g>`
                transform.value = `${transform.value} scale(${scalewid} ${scaleht})`
            }
            //
        }
    }
}


function catalogloader(rawxml) {
    const parser = new DOMParser();
    const templateroot = parser.parseFromString(rawxml,"text/xml");

    let catalog = {}
    for(let i=0; i < templateroot.documentElement.children.length;i++) {
        let c = templateroot.documentElement.children[i]

        if (c.hasAttribute("data-template-id") && c.hasAttribute("data-viewBox")) {
            let templateid = c.getAttribute("data-template-id").toLowerCase().replaceAll(" ","-")
            let vbox = c.getAttribute("data-viewBox")
            let vboxsplit = vbox.split(" ")
            


            catalog[templateid] = {"inner":c.innerHTML,
              "viewBox": vboxsplit,
              "vBstr":vbox,
            }
            
        }
    }
    return catalog
}

function addfont(svgelement,fontfamily) {
    svgdef = document.createElementNS("http://www.w3.org/2000/svg","defs")
    svgstyle = document.createElementNS("http://www.w3.org/2000/svg","style")
    svgstyle.innerHTML = `
svg { font-family: ${fontfamily}}
`
    svgdef.append(svgstyle)
    svgelement.append(svgdef)
}