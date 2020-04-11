#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
'''
svgGuitarChord.py
Inkscape extension for rendering custom guitar chords.

Copyright (C) 2013 Pablo Fernández <pablo.fbus(a)gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
'''

__version__ = "1.0"

import inkex
from lxml import etree

def createGrid(rf, coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'1.6', 'stroke-linecap':'round'}
    if rf == 3:
        path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' h 90 '\
        'm -90,32 h 90 m -90,32 h 90 m -90,32 h 90 '\
        'M ' + str(coor[0]) + ',' + str(coor[1]) + ' v 96 '\
        'm 18,-96 v 96 m 18,-96 v 96 m 18,-96 v 96 '\
        'm 18,-96 v 96 m 18,-96 v 96'
    elif rf == 4:
        path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' h 90 '\
        'm -90,32 h 90 m -90,32 h 90 m -90,32 h 90 '\
        'm -90,32 h 90 '\
        'M ' + str(coor[0]) + ',' + str(coor[1]) + ' v 128 '\
        'm 18,-128 v 128 m 18,-128 v 128 m 18,-128 v 128 '\
        'm 18,-128 v 128 m 18,-128 v 128'
    elif rf == 5:
        path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' h 90 '\
        'm -90,32 h 90 m -90,32 h 90 m -90,32 h 90 '\
        'm -90,32 h 90 m -90,32 h 90 '\
        'M ' + str(coor[0]) + ',' + str(coor[1]) + ' v 160 '\
        'm 18,-160 v 160 m 18,-160 v 160 m 18,-160 v 160'\
        'm 18,-160 v 160 m 18,-160 v 160 '
    return {'d':path, 'style':str(inkex.Style(style))}

def createNut(coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'3.2', 'stroke-linecap':'round'}
    path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' h 90 '
    return {'d':path, 'style':str(inkex.Style(style))}

def createHeader(coor):
    textstyle = {'font-size': '18',
        'font-family': 'Libertinus Serif',
        'text-anchor': 'middle',
        'fill': '#000000'}
    return { 'style':str(inkex.Style(textstyle)),
    'x': str(coor[0]), 'y': str(coor[1]) }

def createTuning(coor):
    textstyle = {'font-size': '8',
        'font-family': 'Libertinus Serif',
        'text-anchor': 'middle',
        'fill': '#000000'}
    tu = []
    for n in range(6):
        tu.append({'style':str(inkex.Style(textstyle)),
        'x': str(coor[n][0]), 'y': str(coor[n][1])})
    return tu

def createPerStringComments(rf, coor):
    if rf == 3:
        cps = [[coor[0]+90, coor[1]+108], [coor[0]+72, coor[1]+108],
            [coor[0]+54, coor[1]+108], [coor[0]+36, coor[1]+108],
            [coor[0]+18, coor[1]+108], [coor[0], coor[1]+108]]
    elif rf == 4:
        cps = [[coor[0]+90, coor[1]+140], [coor[0]+72, coor[1]+140],
            [coor[0]+54, coor[1]+140], [coor[0]+36, coor[1]+140],
            [coor[0]+18, coor[1]+140], [coor[0], coor[1]+140]]
    elif rf == 5:
        cps = [[coor[0]+90, coor[1]+172], [coor[0]+72, coor[1]+172],
            [coor[0]+54, coor[1]+172], [coor[0]+36, coor[1]+172],
            [coor[0]+18, coor[1]+172], [coor[0], coor[1]+172]]
    textstyle = {'font-size': '10',
        'font-family': 'Libertinus Serif',
        'text-anchor': 'middle',
        'fill': '#000000'}
    ps = []
    for n in range(6):
        ps.append({'style':str(inkex.Style(textstyle)),
        'x': str(cps[n][0]), 'y': str(cps[n][1])})
    return ps

def createFirstFret(coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
            'font-weight':'bold', 'text-anchor':'end', 'fill': '#000000'}
    return {'style':str(inkex.Style(textstyle)),
    'x': str(coor[0]-7), 'y': str(coor[1]+28) }

def Fret2text(ff):
    romans = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X',
        'XI', 'XII', 'XIII', 'XIV', 'XV', 'XVI']
    return romans[ff-1]

def createCapo2(coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'1.6', 'stroke-linecap':'round'}
    path = 'M ' + str(coor[0]) + ',' + str(coor[1]) + ' v 4 '\
        'm 18,-4 v 4 m 18,-4 v 4 m 18,-4 v 4 m 18,-4 v 4 m 18,-4 v 4'
    return {'d':path, 'style':str(inkex.Style(style))}

def createCapoPos(coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
            'font-weight':'bold', 'text-anchor':'end', 'fill': '#000000'}
    return { 'style':str(inkex.Style(textstyle)),
    'x': str(coor[0]-5), 'y': str(coor[1]+4) }

def createXAt(xp, coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'1.1', 'stroke-linecap':'round'}
    path = 'M '+ str(coor[xp][0]) + ',' +  str(coor[xp][1]) + ' m 4,4 '\
    'l -8,-8 M '+ str(coor[xp][0]) + ',' +  str(coor[xp][1]) + ''\
    'm -4,4 l 8,-8'
    return {'d':path, 'style':str(inkex.Style(style))}

def create0At(op, coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'1.1', 'stroke-linecap':'round'}
    path = 'M '+ str(coor[op][0]) + ',' +  str(coor[op][1]) + ' m -4,0 '\
    'a 4,4 0 1, 0 8 0 a 4,4 0 1, 0 -8 0'
    return {'d':path, 'style':str(inkex.Style(style))}

def createStringPressedAt(fp, coor):
    style = {'color':'#000000', 'fill':'#000000'}
    path = 'M '+ str(coor[fp[0]][fp[1]][0]) + ','\
    + str(coor[fp[0]][fp[1]][1]) + ' m -6,0 '\
    'a 6,6 0 1, 0 12 0 a 6,6 0 1, 0 -12 0'
    return {'d':path, 'style':str(inkex.Style(style))}

def leftFingerNumberAt(fp, coor):
    textstyle = {'font-size': '8', 'font-family': 'Latin Modern Roman',
            'font-weight':'bold', 'text-anchor':'start', 'fill': '#000000'}
    return { 'style':str(inkex.Style(textstyle)),
    'x': str(coor[fp[0]][fp[1]][0]), 'y': str(coor[fp[0]][fp[1]][1]) }

def createBarreAt(bp, coor):
    style = {'color':'#000000', 'fill':'none', 'stroke':'#000000', 
            'stroke-width':'2', 'stroke-linecap':'round'}
    path = 'M '+ str(coor[bp[0]][bp[1]][0]) + ','\
        + str(coor[bp[0]][bp[1]][1]) + 'L'\
        + str(coor[bp[2]][bp[3]][0]) + ','\
        + str(coor[bp[2]][bp[3]][1])
    return {'d':path, 'style':str(inkex.Style(style))}

class SVGGuitarChord(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument("--tab", type=str, dest="tab")
        self.arg_parser.add_argument("--headerTrue", type=inkex.Boolean, default="True", dest="headerTrue")
        self.arg_parser.add_argument("--header", type=str, default="Em", dest="header")
        self.arg_parser.add_argument("--nFrets", type=int, dest="nFrets", default=4)
        self.arg_parser.add_argument("--firstFret", type=int, dest="firstFret", default=1)
        self.arg_parser.add_argument("--capoPos", type=str, default="No", dest="capoPos")
        self.arg_parser.add_argument("--tuningTrue", type=inkex.Boolean, default="False", dest="tuningTrue")
        self.arg_parser.add_argument("--tuning", type=str, default='E-A-D-G-B-E', dest="tuning")
        self.arg_parser.add_argument("--perStringCommentsTrue", type=inkex.Boolean, default="False", dest="perStringCommentsTrue")
        self.arg_parser.add_argument("--perStringComments", type=str, default='R-5-R-3-5-R', dest="perStringComments")
        self.arg_parser.add_argument("--leftFingerNumberTrue", type=inkex.Boolean, default="True", dest="leftFingerNumberTrue")
        self.arg_parser.add_argument("--firstStringFret", type=str, default='x', dest="firstStringFret")
        self.arg_parser.add_argument("--firstStringFinger", type=str, default='x', dest="firstStringFinger")
        self.arg_parser.add_argument("--secondStringFret", type=str, default='x', dest="secondStringFret")
        self.arg_parser.add_argument("--secondStringFinger", type=str, default='x', dest="secondStringFinger")
        self.arg_parser.add_argument("--thirdStringFret", type=str, default='x', dest="thirdStringFret")
        self.arg_parser.add_argument("--thirdStringFinger", type=str, default='x', dest="thirdStringFinger")
        self.arg_parser.add_argument("--fourthStringFret", type=str, default='x', dest="fourthStringFret")
        self.arg_parser.add_argument("--fourthStringFinger", type=str, default='x', dest="fourthStringFinger")
        self.arg_parser.add_argument("--fifthStringFret", type=str, default='x', dest="fifthStringFret")
        self.arg_parser.add_argument("--fifthStringFinger", type=str, default='x', dest="fifthStringFinger")
        self.arg_parser.add_argument("--sixthStringFret", type=str, default='x', dest="sixthStringFret")
        self.arg_parser.add_argument("--sixthStringFinger", type=str, default='x', dest="sixthStringFinger")

    def effect(self):

        # Coordinates of upper left corner   
        ul = self.svg.namedview.center
        
        # Coordinates of capo, if applicable
        ulc = list(ul)

        # CapoPos to int
        if self.options.capoPos != 'No':
            capoPos2 = int(self.options.capoPos)
        else:
            capoPos2 = 0

        # Corrected coordinates if there is a Capo
        if self.options.capoPos != 'No'\
            and not self.options.firstFret > capoPos2 + 1:
            ulc[1] = ul[1] - 4
        else:
            ulc[1] = ul[1]
        
        # Coordinates of header
      
        if self.options.tuningTrue:
            ch = (ulc[0]+45, ulc[1]-20)
        else:
            ch = (ulc[0]+45, ulc[1]-15)
        
        # Coordinates of tuning indication
        ct = [[ulc[0]+90, ulc[1]-13], [ulc[0]+72, ulc[1]-13],
            [ulc[0]+54, ulc[1]-13], [ulc[0]+36, ulc[1]-13],
            [ulc[0]+18, ulc[1]-13], [ulc[0], ulc[1]-13]]
        
        # Possible coordinates of pressed strings
        
        pfp = [ [ [ul[0]+90, ul[1]+20], [ul[0]+90, ul[1]+52],
            [ul[0]+90, ul[1]+84], [ul[0]+90, ul[1]+116], [ul[0]+90, ul[1]+148] ],
            [ [ul[0]+72, ul[1]+20], [ul[0]+72, ul[1]+52],
            [ul[0]+72, ul[1]+84], [ul[0]+72, ul[1]+116], [ul[0]+72, ul[1]+148] ],
            [ [ul[0]+54, ul[1]+20], [ul[0]+54, ul[1]+52],
            [ul[0]+54, ul[1]+84], [ul[0]+54, ul[1]+116], [ul[0]+54, ul[1]+148] ],
            [ [ul[0]+36, ul[1]+20], [ul[0]+36, ul[1]+52],
            [ul[0]+36, ul[1]+84], [ul[0]+36, ul[1]+116], [ul[0]+36, ul[1]+148] ],
            [ [ul[0]+18, ul[1]+20], [ul[0]+18, ul[1]+52],
            [ul[0]+18, ul[1]+84], [ul[0]+18, ul[1]+116], [ul[0]+18, ul[1]+148] ],
            [ [ul[0], ul[1]+20], [ul[0], ul[1]+52],
            [ul[0], ul[1]+84], [ul[0], ul[1]+116], [ul[0], ul[1]+148] ] ]
        
        # Possible coordinates of finger numbers
        pfn = [[] for n in range(6)]
        for n in range(6):
            pfn[n] = [ [] for m in range(5)]
        for n in range(6):
            for m in range(5):
                pfn[n][m].append(pfp[n][m][0]+2)
                pfn[n][m].append(pfp[n][m][1]-6.5)
        
        # Coordinates of mute and open strings
        xAnd0 = [[ulc[0]+90, ulc[1]-7], [ulc[0]+72, ulc[1]-7],
            [ulc[0]+54, ulc[1]-7], [ulc[0]+36, ulc[1]-7],
            [ulc[0]+18, ulc[1]-7], [ulc[0], ulc[1]-7]]
    
        # Fret and finger per string
        fretFinger = [{'fret':self.options.firstStringFret,
            'finger':self.options.firstStringFinger},
            {'fret':self.options.secondStringFret,
            'finger':self.options.secondStringFinger},
            {'fret':self.options.thirdStringFret,
            'finger':self.options.thirdStringFinger},
            {'fret':self.options.fourthStringFret,
            'finger':self.options.fourthStringFinger},
            {'fret':self.options.fifthStringFret,
            'finger':self.options.fifthStringFinger},
            {'fret':self.options.sixthStringFret,
            'finger':self.options.sixthStringFinger}]

        # Create list of lists [nString, nFret]
        nStringFret = []
        for n in range(6):
            if fretFinger[n]['fret'] != 'x' and fretFinger[n]['fret'] != '0':
                nStringFret.append([n, int(fretFinger[n]['fret'])-1])

        # Increase the number of frets in the grid automatically, if needed
        frets = []
        for n in range(len(nStringFret)):
            frets.append(nStringFret[n][1])
        if len(frets) > 0 and (max(frets) + 1) > self.options.nFrets:
            self.options.nFrets = max(frets) + 1 

        # Create list with muted strings
        nStringX = []
        for n in range(6):
            if fretFinger[n]['fret']=='x':
                nStringX.append(n)
        
        # Create list with open strings
        nString0 = []
        for n in range(6):
            if fretFinger[n]['fret']=='0':
                nString0.append(n)
        
        #Barres
        stringBarre = []
        fretBarre = []
        for n in range(6):
            for m in range(n+1, 6):
                if fretFinger[n]['fret']!='x' and fretFinger[n]['fret']!='0'\
                    and fretFinger[n]['finger'] != 'x'\
                    and fretFinger[n]['finger'] == fretFinger[m]['finger']:
                        stringBarre.append(n)
                        stringBarre.append(m)
                        fretBarre.append(int(fretFinger[n]['fret'])-1)
                        fretBarre.append(int(fretFinger[m]['fret'])-1)
                        break
        zipped = list(zip(stringBarre, fretBarre))
        barres = []
        for n in range(0, len(stringBarre)-1, 2):
            barres.append(zipped[n] + zipped[n+1])

        # Tuning
        tuning = self.options.tuning.split('-')
        tuning.reverse()


        # Comments per String
        perStringComments = self.options.perStringComments.split('-')
        perStringComments.reverse()

        ## Create Grid
        attribs_grid = createGrid(self.options.nFrets, ul)
        etree.SubElement(self.svg.get_current_layer(),
            inkex.addNS('path','svg'), attribs_grid)

        ## Create Nut
        if self.options.firstFret==1 and self.options.capoPos == 'No':
            attribs_nut = createNut(ul)
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_nut)

        ## Create first fret indication
        if (self.options.firstFret!=1 and self.options.capoPos == 'No')\
            or (self.options.firstFret > capoPos2 + 1\
            and self.options.capoPos != 'No'):
            attribs_firstFret = createFirstFret(ul) 
            textFirstFret = etree.SubElement(self.svg.get_current_layer(),
                'text', attribs_firstFret)
            textFirstFret.text = Fret2text(self.options.firstFret)

        ## Create capo indication
        if self.options.capoPos != 'No':
            attribs_capoPos = createCapoPos(ulc) 
            textCapoPos = etree.SubElement(self.svg.get_current_layer(),
                'text', attribs_capoPos)
            textCapoPos.text = 'C ' + Fret2text(capoPos2)

        ## Create capo
        if self.options.capoPos != 'No' and\
                not (self.options.firstFret > capoPos2 + 1):
            attribs_capo1 = createNut(ulc)
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_capo1)
            attribs_capo2 = createCapo2(ulc)
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_capo2)

        ## Create Header
        if self.options.headerTrue:
            attribs_header = createHeader(ch)
            textHeader = etree.SubElement(self.svg.get_current_layer(),
                'text', attribs_header)
            textHeader.text = self.options.header

        ## Create Tuning
        if self.options.tuningTrue:
            attribs_tuning = createTuning(ct)
            try:
                for n in range(6):
                    tuning[n]
                for n in range(6):
                    textTuning = etree.SubElement(self.svg.get_current_layer(),
                        'text', attribs_tuning[n])
                    textTuning.text = tuning[n]
            except IndexError: 
                inkex.debug("WARNING: Wrong tuning input.\n"\
                    "Use 5 hyphens to separate notes. Example: E-A-D-G-B-E")

        ## Create per string comments
        if self.options.perStringCommentsTrue:
            attribs_psComments = createPerStringComments(self.options.nFrets, ul)
            try:
                for n in range(6):
                    perStringComments[n]
                for n in range(6):
                    textTuning = etree.SubElement(self.svg.get_current_layer(),
                        'text', attribs_psComments[n])
                    textTuning.text = perStringComments[n]
            except IndexError: 
                inkex.debug("WARNING: Wrong comments input.\n"\
                    "Use 5 hyphens as separators. A blank space leaves\n"\
                    "a string without a comment. Example: R-5-R- - -5")

        # Create string pressed 
        for n in range(len(nStringFret)):
            attribs_stringPressed = createStringPressedAt(nStringFret[n], pfp)
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_stringPressed)

        # Create left finger number
        for n in range(len(nStringFret)):
            if self.options.leftFingerNumberTrue and\
            fretFinger[nStringFret[n][0]]['finger']!='x':
                attribs_leftFinger = leftFingerNumberAt(nStringFret[n], pfn)
                textLeftFinger = etree.SubElement(self.svg.get_current_layer(),
                    'text', attribs_leftFinger)
                textLeftFinger.text = fretFinger[nStringFret[n][0]]['finger']

        ## Create X (muted string)
        for n in range(len(nStringX)):
            attribs_x = createXAt(nStringX[n], xAnd0) 
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_x)

        ## Create O (open string)
        for n in range(len(nString0)):
            attribs_o = create0At(nString0[n], xAnd0) 
            etree.SubElement(self.svg.get_current_layer(),
                inkex.addNS('path','svg'), attribs_o)

        ## Create barre
        if len(barres) != 0:
            for n in range(len(barres)):
                attribs_barre = createBarreAt(barres[n], pfp)
                etree.SubElement(self.svg.get_current_layer(),
                    inkex.addNS('path','svg'), attribs_barre)

if __name__ == '__main__':  
    e = SVGGuitarChord()
    e.run()
