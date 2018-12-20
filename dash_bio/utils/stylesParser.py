import sys
import numpy as np
import json

def createStyle(pdbPath, style, molcolor, chainsDict=None, atmColor=None):
    '''
    Function to create the different styles (stick, cartoon, sphere) using the
    protein data bank (PDB) file as input. This function outputs the styles as a JSON file

    @param pdbPath 
    Name of the biomolecular structure file in PDB format

    @param style
    Type of representation of the biomolecule (options: stick, cartoon, sphere)

    @param molcolor
    Coloring scheme for depicting biomolecules

    @param chainsDict
    optional parameter to specify the color scheme for different chains in JSON format

    @param atmColor
    optional parameter to specify the color scheme for different atoms in JSON format
    '''
    datS=""
    ## Read input file
    with open (pdbPath, 'r') as infile:
        ## store only non-empty lines
        lines=[l.strip() for l in infile if l.strip()]

    ## Define dictionary of atom and chain colors
    if (chainsDict is None):
        chainsDict = {
            "A":"#32cd32",
            "B":"#8a2be2",
            "C":"#ff4500",
            "D":"#00bfff",
            "E":"#ff00ff",
            "F":"#ffff00",
            "G":"#4682b4",
            "H":"#ffb6c1",
            "I":"#a52aaa",
            "J":"#ee82ee",
            "K":"#75FF33",
            "L":"#FFBD33",
            "M":"#400040",
            "N":"#004000",
            "O":"#008080",
            "P":"#008080",
            "x":"#9c6677",
            "Y":"#b7c5c8"
        }

    residueID = {
        'ALA':'#C8C8C8',
        'ARG':'#145AFF',
        'ASN':'#00DCDC',
        'ASP':'#E60A0A',
        'CYS':'#E6E600',
        'GLN':'#00DCDC',
        'GLU':'#E60A0A',
        'GLY':'#EBEBEB',
        'HIS':'#8282D2',
        'ILE':'#0F820F',
        'LEU':'#0F820F',
        'LYS':'#145AFF',
        'MET':'#E6E600',
        'PHE':'#3232AA',
        'PRO':'#DC9682',
        'SER':'#FA9600',
        'THR':'#FA9600',
        'TRP':'#B45AB4',
        'TYR':'#3232AA',
        'VAL':'#0F820F',
        'ASX':'#FF69B4',
        'GLX':'#FF69B4',
        'OTHER':'#BEA06E',
        'A':'#A0A0FF',
        'DA':'#A0A0FF',
        'G':'#FF7070',
        'DG':'#FF7070',
        'I':'#80FFFF',
        'C':'#FF8C4B',
        'DC':'#FF8C4B',
        'T':'#A0FFA0',
        'DT':'#A0FFA0',
        'U':'#FF8080'
    }

    residueProperty = {}
    for i in ['GLY', 'ALA', 'LEU', 'ILE', 'VAL', 'MET', 'PRO']:
        residueProperty[i] = '#00ff80'
    for i in ['ASN', 'GLN', 'SER', 'THR', 'CYS']:
        residueProperty[i] = '#ff00bf'
    for i in ['ASP','GLU']:
        residueProperty[i] = '#ff4000'
    for i in ['LYS', 'ARG', 'HIS']:
        residueProperty[i] = '#0040ff'
    for i in ['TRP', 'TYR', 'PHE']:
        residueProperty[i] = '#ffff00'
    for i in ['A', 'G', 'DA', 'DG']:
        residueProperty[i] = '#A00042'
    for i in ['DT', 'DC', 'U', 'I', 'C']:
        residueProperty[i] = '#4F4600'

    if (atmColor is None):
        atmColor = {
            "C":"#c8c8c8",
            "H":"#ffffff",
            "N":"#8f8fff",
            "S":"#ffc832",
            "O":"#f00000",
            "F":"#ffff00",
            "P":"#ffa500",
            "K":"#42f4ee",
            "G":"#3f3f3f"
        }


    ## Create the styles files in JSON format
    chain=[]; atmType=[]; resName=[]
    ct=0
    ct1=0
    data={}
    for l in lines:
        line=l.split()
        if("ATOM" in line[0] or "HETATM" in line[0]):
            chain.append(l[21:22].strip())
            atmType.append(l[77:78])
            val_rName=l[17:20].strip()
            resName.append(val_rName)

            index=str(ct1)
            if(line[0]=="ATOM"):
                if (molcolor == 'chainColor'):
                    if (chain[ct1] in chainsDict):
                        data[index]={
                            "color":chainsDict[chain[ct1]],
                            "visualization_type":style
                        }
                    else:
                        data[index]={
                        "color":'#BEA06E',
                        "visualization_type":style
                    }
                elif (molcolor == 'residueID'):
                    uresn=resName[ct1].upper()
                    if (uresn in residueID):
                        data[index]={
                        "color":residueID[resName[ct1]],
                        "visualization_type":style
                    }
                    else:
                        data[index]={
                        "color":'#BEA06E',
                        "visualization_type":style
                    }
                elif (molcolor == 'residueProperty'):
                    uresn=resName[ct1].upper()
                    if (uresn in residueProperty):
                        data[index]={
                        "color":residueProperty[resName[ct1]],
                        "visualization_type":style
                    }
                    else:
                        data[index]={
                        "color":'#BEA06E',
                        "visualization_type":style
                    }
                elif (molcolor == 'atomColor'):
                    if atmType[ct1] in atmColor:
                        data[index]={
                            "color":atmColor[atmType[ct1]],
                            "visualization_type":style
                        }
                    else:
                        data[index]={
                            "color":"#330000",
                            "visualization_type": style
                        }

            else:
                if atmType[ct1] in atmColor:
                    data[index]={
                        "color":atmColor[atmType[ct1]],
                        "visualization_type":"stick"
                    }
                else:
                    data[index]={
                        "color":"#330000",
                        "visualization_type":"stick"
                    }
            ct1 += 1

    return (json.dumps(data))