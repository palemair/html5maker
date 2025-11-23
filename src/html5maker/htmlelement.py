#!../myenv/bin/python3

import os
from pathlib import Path
from xml.etree import ElementTree as et
from .converter import MdConverter

#abstract class htmlcontainer
class AbstractElement(et.Element):
    """
    AbstractElement is a derived class from an xml.etree.ElementTree.Element

    This is the base class for :

    html tags like Article, Section, Body ...

    svg, Text html tags like paragraph, li, h[1-6] ...

    """
    def __init__(self,tag : str, attrib : dict = {},**extra) :
        """ Allow using '_' instead of '-' """

        change_extra = [ k.replace('_','-') for k in extra.keys()]
        attrib.update(dict(zip(change_extra,extra.values())))
        super().__init__(tag,attrib)

    def __add__(self,element):
        """ Using '+' operator to append Element """

        self.append(element)
        return self

    def to_html_string(self)->str:
        return et.tostring(self,encoding = 'unicode',method = 'html',short_empty_elements = True)

class HtmlElement(AbstractElement):
        
    """ 
    HTML Element : section, article, aside.... 

    """
    def __init__(self,tag : str,content : str = '',attrib : dict = {}, **extra):

        super().__init__(tag,attrib,**extra)
        self.text = content

    def content_list(self, block : str = 'article',target : str = 'h2',attrib = {},**extra)-> AbstractElement :

        """Create a ul li listed elements from an element

        Arguments:

            target : Element searched

        Returns:

            An HtmlElement aka xml.etree.ElementTree 
        """

        ol = HtmlElement('ol', attrib, **extra)

        elts = (elt for elt in self.iterfind(f'.//{block}'))
        
        for elt in elts:
            h = elt.find(f'{target}')
            string = h.text
            elt.set('id',string)
            li=et.SubElement(ol,'li')
            a=et.SubElement(li,'a',href=f'#{string}',title=f'Aller à {string}')
            a.text=string

        return ol

#class svgcontainer
class SvgElement(AbstractElement):

    """ Svg Element : Svg, use, defs, animate.... """
    
    def basicshape(self,forme : str, *args, attrib = {}, **extra):
        
        match forme:
            case "line":
                if(len(args) == 4):
                    param = ('x1','y1','x2','y2')
                    attrib.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "circle":
                if(len(args) == 3):
                    param = ('cx','cy','r')
                    attrib.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "ellipse":
                if(len(args) == 4):
                    param = ('cx','cy','rx','ry')
                    attrib.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "rect":
                if(len(args) >= 4):
                    param = ('x','y','width','height','rx','ry')
                    attrib.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polyline":
                if(len(args) >= 1):
                    param = ('points')
                    attrib[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polygon":
                if(len(args) >= 1):
                    param = ('points')
                    attrib[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case _:
                raise SyntaxError ('Not a basic shape')

        self.append(SvgElement(forme,attrib,**extra))
        return self

class FactoryElement:

    converter = MdConverter(extensions=['pymdownx.extra','pymdownx.keys','pymdownx.mark'],output_format = "html")

    def __init__(self,src_dir : [str | os.PathLike] = '.'):

        """ 
        Factory class to produce:
            Htmltag, SvgTag, Html from markdown
        """
        self.src : [str | os.PathLike] = src_dir

    def svg_tag(tag : str, attrib : dict = {},**extra) -> SvgElement:

        return SvgElement(tag,attrib, **extra)

    def html_tag(tag : str, content : str ='', attrib : dict = {},**extra):

        return HtmlElement(tag, content, attrib, **extra)

    def from_markdown(self,*input_contents : [ str | os.PathLike ], parent : str = 'article', attributes = {}, **kwargs):

        """
        Add element from a Markdown File or string written in markdown syntax

        you can choose, with 'parent' attribute the tag root element append

        """
        for content in input_contents:

            try :
                filesrc = Path(self.src / content)

            except IsADirectoryError :
                print(f"{content} : Path is a directory, not a file !!")
                continue

            except FileNotFoundError :
                print(f"{content} : Not a correct filename !!")
                continue

            else:

                content = filesrc.read_text(encoding = 'utf-8-sig')

            tree = self._mdconvert(content)
            
            tree.tag = parent
            tree.attrib.update(attributes)
            return tree

    def _mdconvert(cls,md_string : str): 

        root = cls.converter.convert_to_tree(md_string)
        cls.converter.reset()
        return root

