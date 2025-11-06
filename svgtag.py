#!./env/bin/python3

from pathlib import Path
import container

#Concrete Svg container 
class Svg(container.SvgContainer):

    __slots__ = ('width','height','cssfile')    
    "Svg : Element root of the drawing"

    def __init__(self, width : int = 1000, height : int = 1000, cssfile = ''):
        
        attrib_svg ={'version' : "1.1",
                     'baseProfile' : "full",
                     'xmlns' : "http://www.w3.org/2000/svg"                                                                                         
                     }

        super().__init__('svg', **attrib_svg)
        self.width = width
        self.height = height
        self.css = Path(cssfile)

    def to_svg_file(self,dest_file : str):
        
        self._root.set('width' , f"{self.width}")
        self._root.set('height' , f"{self.height}")

        if (self.css.is_file()):
            style = et.Element('style',{"type":"text/css"})
            style.text = self.css.read_text('utf-8')
            self._root.insert(0,style)

        file = Path.home() / 'Bureau' / dest_file
        file = file.with_suffix('.svg')

        with file.open('w',encoding = 'utf-8') as f:
            f.write('<?xml version = "1.0" encoding="UTF-8">\n')
            f.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"\n "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">\n')
            f.write(f"{container.et.tostring(self._root,encoding = 'unicode')}")

        if (self._root.find('style') is not None):
            self._root.remove(style)

    def __enter__(self):

        return self

    def __exit__(self,exc_type, exc_value, traceback):
        
        self._root.set('width' , '100%')
        self._root.set('height' , '100%')
        self._root.set('viewBox', f"0 0 {self.width} {self.height}")

class Groupe(container.SvgContainer):

    def __init__(self, **kwargs):
        super().__init__('g', **kwargs)

class Defs(container.SvgContainer):

    def __init__(self, **kwargs):
        super().__init__('defs', **kwargs)

class Use(container.SvgContainer):

    def __init__(self, href : str, **kwargs):
        
        attrib = {"xlink:href" : f'#{href}'}
        attrib.update(kwargs)
        super().__init__('use', **attrib)

class Texte(container.HtmlText):

    """ Must be use in svg only"""
    def __init__(self, xpos : int, ypos : int , text : str, **kwargs):
        
        attrib = dict(x = str(xpos), y = str(ypos))
        attrib.update(kwargs)
        super().__init__('text', **attrib)
        self.set_text(text)

if __name__ == '__main__':


    linestyle = {'stroke' : 'blue', 'stroke-width' : '2px', 'fill' : 'gray'}
    groupe1 = Groupe(**linestyle)

    groupe1.basicshape('line',300,200,456,234)
    groupe1.basicshape('circle',300,200,45)

    with Svg() as dessin:

        dessin.append(groupe1)

        dessin.append(Texte(200,300,"test"))

        dessin.basicshape('ellipse',600,500,45,70, stroke = 'red',fill = 'green')
        dessin.basicshape('rect',300,700,300,150,**linestyle)

    dessin.to_svg_file('tes')
