#!../myenv/bin/python3

import pathlib
from pathlib import Path
from xml.etree import ElementTree as et
from xml.etree.ElementTree import Element

from .converter import MdConverter
from markdown.extensions import extra

#abstract class htmlcontainer
class HtmlElement(Element):
    """
    HtmlElement is a derived class from an xml.etree.ElementTree.Element

    This is the base class for :

    Section html tags like Article, Section, Body ...

    Text html tags like paragraph, li, h[1-6] ...

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

    def tostring(self)->str:
        return et.tostring(self,encoding = 'unicode',method = 'html',short_empty_elements = True)

class BlockElement(HtmlElement):
        
    """ 
    HTML section Element : section, article, aside.... 

    do not use that element to insert text in it
    """

    converter = MdConverter(extensions = ['extra'],output_format = "html")

    def add_markdown(self,*input_contents : [ str | pathlib.PurePosixPath ], parent : str = 'article', attrib = {}, **kwargs):

        """
        Add element from a Markdown File or string written in markdown syntax

        you can choose, with 'parent' attribute the tag root element append

        """
        for content in input_contents:

            try:
                content = content.read_text(encoding = 'utf-8')

            except IsADirectoryError :
                print(f"{content} : Path id a directory, not file !!")
                continue

            except FileNotFoundError :
                print(f"{content} : Not a correct filename !!")
                continue

            except AttributeError :

                if(type(content) != str):

                    print(f"{content} : Not a correct string !!")
                    continue

            tree = self.convert(content)
            tree.tag = parent
            attrib.update(kwargs)
            tree.attrib = attrib

            self.append(tree)

    def content_list(self, target : str = 'h2',attrib = {},**extra) :

        """Create a linked element list from an element

        Arguments:

            target : Element searched

        Returns:

            A BlockElement aka xml.etree.ElementTree 
        """

        ul = BlockElement('ul', attrib, **extra)

        elts = (elt for elt in self.iterfind(f'.//{target}'))
        
        for elt in elts:
            string = elt.text
            elt.set('id',string)
            li=et.SubElement(ul,'li')
            a=et.SubElement(li,'a',href=f'#{string}',title=f'Aller à {string}')
            a.text=string

        return ul

    @classmethod
    def convert(cls,md_string : str): 

        root = cls.converter.convert_to_tree(md_string)
        cls.converter.reset()
        return root

    @staticmethod
    def new_tag(tag : str, attrib : dict = {},**extra):

        return BlockElement(tag,attrib, **extra)

class InlineElement(HtmlElement):

    """ HTML text Element : section, article, aside.... """

    def __init__(self,tag : str,content : str = '',attrib : dict = {}, **extra):

        super().__init__(tag,attrib,**extra)
        self.text = content

    @staticmethod
    def new_tag(tag : str, content : str ='', attrib : dict = {},**extra):

        return InlineElement(tag, content, attrib, **extra)

#abstract class svgcontainer
class SvgElement(HtmlElement):

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

    @staticmethod
    def new_tag(tag : str, attrib : dict = {},**extra):

        return SvgElement(tag,attrib, **extra)
