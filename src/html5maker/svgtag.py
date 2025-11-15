#!../../myenv/bin/python3

import os
from pathlib import Path
from .htmlelement import SvgElement, InlineElement

#Concrete Svg container 
class Svg(SvgElement):

    """
    Svg : Element root of the drawing 

    """
    def __init__(self, width : int = 500, height : int = 500, **extra):
        
        attrib_svg ={'version' : "1.1",
                     'baseProfile' : "full",
                     'xmlns' : "http://www.w3.org/2000/svg"                                                                                         
                     }
        super().__init__('svg', attrib_svg,**extra)
        self.width = width
        self.height = height

    def to_file(self,dest_file : str ,css_file : str | os.PathLike = None):
        
        self.set('width' , f"{self.width}")
        self.set('height' , f"{self.height}")
        
        if (css_file is not None and Path(ccs_file).exists()):
            style = self.new_tag('style',{"type":"text/css"})
            style.text = Path(css_file).read_text('utf-8')
            self.insert(0,style)

        dest = Path(dest_file)
        with dest.with_suffix('.svg').open('w',encoding = 'utf-8') as f:
            f.write('<?xml version = "1.0" encoding="UTF-8">\n')
            f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            f.write(f"{self.tostring()}")

        if (self.find('style') is not None):
            self.remove(style)

    def __enter__(self):

        return self

    def __exit__(self,exc_type, exc_value, traceback):
        
        self.set('width' , '100%')
        self.set('height' , 'auto')
        self.set('viewBox', f"0 0 {self.width} {self.height}")

def Groupe(attrib : dict = {}, **extra):
    return SvgElement('g',attrib, **extra)

def Defs(attrib : dict = {}, **extra):
    return SvgElement('defs',attrib, **extra)

def Use(href : str,attrib : dict = {}, **extra):

    attrib.update({"xink:href" : f'#{href}'})
    return SvgElement('use',attrib, **extra)

def Text(xpos : int, ypos : int, content : str, attrib : dict = {}, **extra):

    position = { 'x' : str(xpos), 'y' : str(ypos)}
    attrib.update(position)
    return InlineElement('text',content,attrib, **extra)
