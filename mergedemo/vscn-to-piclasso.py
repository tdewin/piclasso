#!/usr/bin/env python3
import argparse
import base64
import json
import math

def calculateres(resources,wlid,wlres,wllabel,wlarrow,names={"pname":"proxy","pnameid":"PROXY"}):
    repoid =  ""
    proxyid = ""
    resi = 0
    for res in resources:
        multi = "3"
        resname = "backup-repository"
        resnameid = "REPO"
        isproxy = False
        if 300 in res.get("Roles"):
            multi = "1"
            resname = names["pname"]
            resnameid = names["pnameid"]
            isproxy = True
        
        resid='{}_{}{}'.format(wlid,resnameid,resi)
    
        diskoutput = ""
        for d in res.get("Disks"):
            if d.get("Purpose") == 3:
                diskoutput = d.get("CapacityString")
        mover = "boxwid*{}".format(multi)
        
        wlres.append('{}: rpl "{}" with .w at {}.e+({},0)\n     move'.format(resid,resname,wlid,mover))

        c = math.ceil(res.get("Cores")/2)*2
        m = math.ceil(res.get("RamGB")/2)*2

        c = round(res.get("Cores"),2)
        m = round(res.get("RamGB"),2)
        wllabel.append('      blbl({},$grey,"C:{} M:{}" "{}")'.format(
            resid,c,m,diskoutput))
        resi +=1

        if isproxy:
            proxyid = resid
        else:
            repoid = resid
    if proxyid !="":
        wlarrow.append('{}_{}: arrow from {}\\\n           to {} ""  above chop'.format(wlid,proxyid,wlid,proxyid))
        if repoid!="":
          wlarrow.append('{}_{}: arrow from {}\\\n           to {} "backup"  above chop'.format(proxyid,repoid,proxyid,repoid))


def main():
    parser = argparse.ArgumentParser(description="Read location names from a JSON file.")
    parser.add_argument("filepath", help="Path to the JSON file containing location data")
    parser.add_argument("--link", action="store_true", help="Enable link mode (optional flag)")
    args = parser.parse_args()

    try:
        
        with open(args.filepath, 'r') as file:
            data = json.load(file)

            basetxt = []
            preamble = []
            preamble.append('boxwid = 1')
            preamble.append('boxht = 1')
            preamble.append('$hboxwid = boxwid/2')
            preamble.append('$locationcolor = $lightgrey')
            preamble.append('$locationrad = 0.3')
            preamble.append('$cols = 3')
            preamble.append('$locationwidth = ($cols*2)*boxwid')


            title = data.get("Name")
            locations = data.get("Locations", [])
            workloads = data.get("WorkloadMap")
            #jq '.WorkloadMap.VMScope."TypedWorkloads"[] | .BaseInputs.SourceTB,.BaseInputs.SiteId'
            vms = workloads.get("VMScope")
            agents = workloads.get("AgentScope")
           

            i = 0
            titleprint = [""]
            wlprint = []
            maxload = 1
            for location in locations:
                n = location.get("Name")
                
                iid = location.get("Id")
                locid = "LOC{}".format(i)
                #color $locationcolor
                basetxt.append("{}: box wid $locationwidth ht $locationheight invis;move boxwid/1.5;".format(locid))
                titleprint.append('{}_TITLE: box "{}" fit with .c at LOC{}.n invis\n                  titledBox({}_TITLE,{},$lightgrey)'.format(locid,n,i,locid,locid))
                i += 1
                wli = 0

                wlprint.append("\n//SITESTART: {}\n      down;move to {}.nw+(boxwid,-$hboxwid)".format(n,locid))
                wlres = [""]
                wllabel = [""]
                wlarrow = [""]
                wloads = 0
                if vms:
                    typedworkloads = vms.get("TypedWorkloads")
                    for wl in typedworkloads:
                        if wl.get("SourceLocationId") == iid:
                          wloads += 1
                          baseinputs = wl.get("BaseInputs")
                          sitename = baseinputs.get('Name')
                          wlid = '{}_VM{}'.format(locid,wli)
                          wlprint.append('{}: rpl "vm"\n     move'.format(wlid))

                          wllabel.append('      blbl({},$grey,"{}" "{} TB")'.format(wlid,sitename,baseinputs.get("SourceTB")))
                          wli +=1
                          resources = wl.get("Resources")
                          
                          calculateres(resources,wlid,wlres,wllabel,wlarrow)
 
                              
                          
                if agents:
                    typedworkloads = agents.get("TypedWorkloads")
                    for wl in typedworkloads:
                        if wl.get("SourceLocationId") == iid:
                          wloads += 1
                          baseinputs = wl.get("BaseInputs")
                          sitename = baseinputs.get('Name')
                          wlid = '{}_AGENT{}'.format(locid,wli)
                          wlprint.append('{}: rpl "veeam-agent"\n     move'.format(wlid))
                          wllabel.append('      blbl({},$grey,"{}" "{} TB")'.format(wlid,sitename,baseinputs.get("SourceTB")))
                          wli +=1   

                          resources = wl.get("Resources")
                          calculateres(resources,wlid,wlres,wllabel,wlarrow,{"pname":"data-mover","pnameid":"DATAMOVER"})
                          
                wlprint += wlres
                wlprint += wllabel
                wlprint += wlarrow
                wlprint.append("//SITEEND: {}".format(n))
                if wloads > maxload:
                    maxload = wloads
            basetxt +=titleprint
            basetxt +=wlprint

            preamble.append("".join(['$rows=',str(maxload),'\n$locationheight = ($rows*1.5+0.5)*boxht']))
            preamble += basetxt
            if args.link:
                print("https://tdewin.github.io/piclasso/?f={}&t={}&i={}".format(
                    base64.b64encode("'ES Build Full Bauhaus', 'Arial'".encode('utf-8')).decode('utf-8'),
                    base64.b64encode(title.encode('utf-8')).decode('utf-8'),
                    base64.b64encode("\n".join(preamble).encode('utf-8')).decode('utf-8')))
            else:
                print("\n".join(basetxt))
    except FileNotFoundError:
        print(f"File not found: {args.filepath}")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

if __name__ == "__main__":
    main()

