#!../myenv/bin/python3

import os
from pathlib import Path
from getpass import getuser
from collections import OrderedDict
from .htmlelement import HtmlElement, FactoryElement

class Pages(dict):

    """ 
        Wrapper dict around pages collection Document object:
        Allowing to avoid the index name for the first web page :

        labels : name + filename(== name except 1st == index).html
    """

    def filenames(self):
        index,*others = list(self.keys())
        index = 'index.htlm'
        others = (f'{title}.html' for title in others)

        return (index,*others)

    def labels(self):
        return tuple(zip(self.keys(),self.filenames()))

    def all_items(self):
        return tuple(zip(self.keys(),self.values(),self.filenames()))

class HtmlDocument(FactoryElement):

    """ 
        Document object: contains the name of the project,
        directories src and dest to put the files, the language, the css files,
        and the authors informations.
        pages == each independant part of the global document
    """ 

    def __init__(self,name : str,
                 src_dir : [str | os.PathLike] = '.',
                 dest_dir :[str | os.PathLike] = '~/Bureau',
                 lang : str='fr'):
        self.name = name
        self.lang = lang
        self.pages = Pages()

        try :
            src = Path(src_dir).expanduser().absolute()

        except FileNotFoundError :
            print(f"{src_dir} : Path is not a directory !!")
            return

        if src.is_dir() is False:
            return

        super().__init__(src)

        try :
            dest = Path(dest_dir).expanduser().absolute()

        except FileNotFoundError :
            print(f"{dest_dir} : Path is not a directory !!")
            return

        if dest.is_dir() is False :
            return

        self.dest = dest / name
        self.dest.mkdir(exist_ok = True)

    def add(self,title : str, element : HtmlElement):

        if title not in self.pages.keys():
            self.pages[title] = element
        else:
            print("Page exist, can't duplicate !!")

        return self

    def remove(self,title : str):

        if title in self.pages.keys():
            self.pages.pop(title)
        else:
            print("Not in the document !!")

        return self

    def main_menu(self,attrib :dict = {'class' : 'global'}, **extra) -> HtmlElement :

        nav = HtmlElement('nav')
        ul=HtmlElement('ul')

        for name, filename in self.pages.labels():
            li = HtmlElement('li')
            a = HtmlElement('a',name,{'href': f'{filename}', 'title' : f'Aller à {name}'})
            ul += li + a
        nav += ul

        return nav
        
    def __repr__(self):

        ret = (f'{n} -> {f}' for n,f in self.pages.labels())
        return '\n'.join(ret)

    def to_file(self, menu_on : bool = False):
        
        html = []
         
        for name,page,filename in self.pages.all_items():
            file = self.dest / filename

            head =  f'<html lang ="{self.lang}">'
            head += f'<head><meta charset = "utf-8" />'
            head += f'<title>{name}</title>'
            head += f'<meta name="author" content="{getuser()}" />'
            head += f'<meta name="viewport" content="width=device-width" initial-scale = "1.0" />'
            for css in self.src.glob('*.css'):
                head += f'<link rel="stylesheet" href="{css.resolve()}" />'

            head += f'</head>\n'

            html.append(head)

            if menu_on is True :
                menu = self.main_menu()
                page.insert(0,menu)

            body = page.to_html_string()
            html.append(body)
            
            html.insert(0, """<!DOCTYPE html>\n""")
            html.append("""\n</html>""")
 
            h = ''.join(html)

            with file.open('w',encoding = 'utf-8') as f:
                f.write(h)

    def tostring(self):
        
        for name,page in self.pages.items():
            ret = f'*** page : {name} ***:\n'
            ret += page.to_html_string()
            ret += f'\n*** end page : {name} ***\n'
        return ret
