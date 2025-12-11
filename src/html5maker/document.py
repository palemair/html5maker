#!../myenv/bin/python3

import os
from pathlib import Path
from getpass import getuser
from .htmlelement import HtmlElement as htmlE
from .htmlelement import FactoryElement

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
                 logo : [str | os.PathLike] = None,
                 src_dir : [str | os.PathLike] = '.',
                 dest_dir :[str | os.PathLike] = '~/Bureau',
                 lang : str='fr'):

        self.name = name
        self.lang = lang
        self.pages = Pages()

        if logo is not None:
            self.logo = str(Path(logo).absolute())
        else:
            self.logo = None

        try :
            src = Path(src_dir).expanduser().absolute()

        except FileNotFoundError :
            print(f"{dest_dir} : Path is not a valid filenanme !!")
            return

        if src.is_dir() is False:
            print(f"{src_dir} : Path is not a directory !!")
            return

        super().__init__(src)

        try :
            dest = Path(dest_dir).expanduser().absolute()

        except FileNotFoundError :
            print(f"{dest_dir} : Path is not a valid filenanme !!")
            return

        if dest.is_dir() is False :
            print(f"{src_dir} : Path is not a directory !!")
            return

        self.dest = dest / name
        self.dest.mkdir(exist_ok = True)

    def add(self,title : str, element : htmlE):

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

    def __repr__(self):

        ret = (f'{n} -> {f}' for n,f in self.pages.labels())
        return '\n'.join(ret)

    def save(self, menu_on : bool = True, attr : dict = {"class" : "global"},indent : bool = False):
        
        css_dir = self.src / 'styles'

        for name,page,filename in self.pages.all_items():
            html = []
            file = self.dest / filename

            head =  f'<html lang ="{self.lang}">'
            head += f'<head><meta charset = "utf-8" />'
            head += f'<title>{name}</title>'
            head += f'<meta name="author" content="{getuser()}" />'
            head += f'<meta name="viewport" content="width=device-width" initial-scale = "1.0" />'
            for css in css_dir.glob('*.css'):
                head += f'<link rel="stylesheet" href="{css.resolve()}" />'

            head += f'</head>\n<body>\n'

            html.append(head)

            header = htmlE('header',attr)

            if self.logo is not None:
                lg = htmlE('img',{'src' : self.logo})
                header += lg

            if len(self.pages) > 1 :
                nav = htmlE('nav')
                ul = htmlE('ul')
                tmpdict = { n:f for n,f in self.pages.labels() if n != name}

                for n, f in tmpdict:
                    li = htmlE('li')
                    a = htmlE('a',name,{'href': f'{filename}', 'title' : f'Aller à {name}'})
                    ul += (li + a)
                nav += ul
                header += nav

            header += htmlE('h1',content = name)

            html.append(header.to_html_string())

            content = page.to_html_string(indent = indent)
            html.append(content)
           
            html.insert(0, """<!DOCTYPE html>\n""")
            html.append("""\n</body>\n</html>""")
 
            h = ''.join(html)

            with file.open('w',encoding = 'utf-8') as f:
                f.write(h)

    def tostring(self):
        
        ret = ''
        for k, v in self.pages.items():
            ret += f'\n*** page : {k} ***:\n'
            ret += v.to_html_string()
            ret += f'\n*** end page : {k} ***'

        return ret
