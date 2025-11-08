#!./myenv/bin/python3

"""abstract module defining the concrete classes"""

from abc import ABC, abstractmethod
from pathlib import Path
import pathlib
import xml.etree.ElementTree as et

import markdown


#Specific Markdown Converter
class MdConverter(markdown.core.Markdown):
    
    def convert_to_tree(self, source: str) -> str:
        """
        Convert a Markdown string to an xml.etree.Element

        The markdown converter is an overloaded function
        
        Arguments:
            source: Markdown formatted text as Unicode or ASCII string.

        Returns:
            An xml.etree.Element
        """

        # Fix up the source text
        if not source.strip():
            return ''  # a blank Unicode string

        try:
            source = str(source)
        except UnicodeDecodeError as e:  # pragma: no cover
            # Customize error message while maintaining original traceback
            e.reason += '. -- Note: Markdown only accepts Unicode input!'
            raise

        # Split into lines and run the line preprocessors.
        self.lines = source.split("\n")
        for prep in self.preprocessors:
            self.lines = prep.run(self.lines)

        # Parse the high-level elements.
        root = self.parser.parseDocument(self.lines).getroot()

        # Run the tree-processors
        for treeprocessor in self.treeprocessors:
            newRoot = treeprocessor.run(root)
            if newRoot is not None:
                root = newRoot

        return root

class Container(ABC):
    
    "Abstract element container"
    __slots__ = ('_root',)    

    def __init__(self,tag : str, attrib : dict = {},**kwargs):

        self._root = et.Element(tag,attrib,**kwargs)

    def __str__(self)-> str:
        
        b = []
        return Container._str_buffer(b,self._root,indent = 4)

    def append(self,*containers):
        
        for container in containers:
            if (not isinstance(container,Container)):
                raise TypeError("Need an xml.etree.element !!")

            match container._root.tag:
                case  'main' :
                    raise ValueError(f"You can only assign '{container._root.tag}' in a page")

            self._root.append(container._root)

        return self

    def insert(self,number : int,container):
        
        self._root.insert(number,container._root)

        return self

    def __add__(self,container):

        self._root.append(container._root)
        return self

    def tostring(self)->str:
        return et.tostring(self._root,encoding = 'unicode',method = 'html',short_empty_elements = True)

    @staticmethod
    def _str_buffer(buffer : list[str],root : et.Element, start : int = 0,indent : int = 2) -> str :
        
        "pretty printing tree"
        if root is not None:

            content = root.text if root.text is not None else '\n'
            buffer.append(f"{start*' '}<{root.tag}>{content}")
            for child in root:
                Container._str_buffer(buffer,child,start + indent)

            if root.findall("*") != []:
                buffer.append(f"{start*' '}</{root.tag}>\n")
            else :
                buffer.append(f"</{root.tag}>\n")

        return ''.join(buffer)

    @staticmethod
    def _content_list(source : et.Element = 'section', target : str = 'h2') -> et.Element :

        """Create a linked element list from an element

        Arguments:
            source : Element in wich 'target' is listed

            target : Element searched in the 'source'

        Returns:
            An xml.etree.Element 
        """

        ul = et.Element('ul')

        liste_elt = (elt for elt in source.iterfind(f'.//{target}'))
        
        for elt in liste_elt:
            elt.set('id',titre.text)
            li=et.SubElement(ul,'li')
            a=et.SubElement(li,'a',href=f'{self.title}.html#{titre.text}',title=f'Aller à {titre.text}')
            a.text=titre.text

        return ul

#abstract class htmlcontainer
class HtmlSection(Container):
        
    """ HTML conteneur : section, article, aside.... """

    converter = MdConverter()

    def __init__(self,tag : str,attrib : dict = {}, **kwargs) :

        super().__init__(tag,attrib,**kwargs)

    def add_from_markdown(self,*input_contents : [ str | pathlib.PurePosixPath ], parent : str = 'div', **kwargs):

        """Add element from a Markdown File or string written in markdown syntax

           you can choose, with 'parent' attribute the tag root element append """

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

                    print(f"{content} : Neither a correct string !!")
                    continue

            tree = self.convert(content)
            tree.tag = parent
            self._root.append(tree)

    @classmethod
    def convert(cls,md_string : str) -> et.Element :

        root = cls.converter.convert_to_tree(md_string)
        cls.converter.reset()
        return root

    @staticmethod
    def create_section_tag(tag : str, **kwargs):

        match tag:
            case 'main':
                raise ValueError("You can only assign 'main' with a main object !!")
            case 'body':
                raise ValueError("You can only assign 'main' with a main object !!")
            case _:
                return HtmlSection(tag, **kwargs)

    @staticmethod
    def create_text_tag(tag : str, **kwargs) -> Container :

        return HtmlText(tag, **kwargs)

class HtmlText(Container):

    "HTML text container : p,h1,..."
    def __init__(self,tag : str,content : str = '',attrib : dict = {}, **kwargs):

        super().__init__(tag,attrib,**kwargs)
        self._root.text = content

    def set_text(self,input_text : str):

        self._root.text = input_text

#abstract class svgcontainer
class SvgContainer(Container):

    "Svg generic container : Use, defs, animate...."
    def __init__(self,tag : str,attrib : dict = {}, **kwargs) :

        super().__init__(tag,attrib,**kwargs)
    
    def basicshape(self,forme : str, *args,**kwargs):
        
        coord = {}
        match forme:
            case "line":
                if(len(args) == 4):
                    param = ('x1','y1','x2','y2')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "circle":
                if(len(args) == 3):
                    param = ('cx','cy','r')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "ellipse":
                if(len(args) == 4):
                    param = ('cx','cy','rx','ry')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "rect":
                if(len(args) >= 4):
                    param = ('x','y','width','height','rx','ry')
                    coord.update(dict(zip(param,[str(x) for x in args])))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polyline":
                if(len(args) >= 1):
                    param = ('points')
                    coord[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case "polygon":
                if(len(args) >= 1):
                    param = ('points')
                    coord[param] = ' '.join((f'{p[0]},{p[1]}' for p in args))
                else:
                    raise SyntaxError('bad number of arguments')

            case _:
                raise SyntaxError ('Not a basic shape')

        coord.update(kwargs)
        self._root.append(et.Element(forme,coord))
        
        return self

    @staticmethod
    def svg_tag(tag : str, **kwargs) -> Container :

        match tag:
            case 'svg':
                raise ValueError("You can only assign 'svg' with a Svg object !!")
            case _:
                return SvgContainer(tag, **kwargs)
