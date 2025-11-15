#!../myenv/bin/python3

import os
from pathlib import Path
from getpass import getuser

from .htmlelement import BlockElement, InlineElement

class Page(BlockElement):
    """
    Body element : root of the document without metadatas

    """
    def __init__(self,title : str, md_file : any = None, attrib : dict = {},**kwargs):
        super().__init__('body',attrib,**kwargs)
        self.title = title
        if md_file is not None:
            self.add_markdown(md_file)

class HtmlDocument:
    """ Document object: it contains the name of the project,
        directory where to put the files, the language, the css files,
        and the authors informations. """

    firstpage = 'index'

    def __init__(self,name : str,
                 src_dir : str | os.PathLike = None,
                 dest_dir : str | os.PathLike = None,
                 lang : str='fr'):

        self.pages = {}
        self.name = name
        self.lang = lang
        self.src_dir = Path(src_dir).expanduser().resolve()
        dest = Path(dest_dir).expanduser().resolve()
        self.dest_dir = dest / self.name 
        self.dest_dir.mkdir(exist_ok = True)

    def get_page(self,name:str):
        return self.pages[name]

    def add_page(self, *pages : Page)-> Page :
        """Add new page. """

        for page in pages:
            if self.pages == {} :
                page.title = self.name
                self.pages[self.__class__.firstpage] = page

            elif (page.title not in self.pages.keys()):
                    self.pages[page.title] = page
        
            else :
                print("page exist, can't duplicate")

        return self
         
    def __str__(self) ->str:

        ret = f'< Contenu du document :\n{self.name} :'
        for k,v in self.pages.items():
            ret += f'\n\t{v.title} -> "{k}.html"'
        ret += ' >'
        return ret

    def add_head(self,page : Page)-> str:

        html =f'<html lang ="{self.lang}">\n'

        #head of the page
        html += f'<head><meta charset = "utf-8" />\n'
        html += f'<title>{page.title}</title>\n'
        html += f'<meta name="author" content="{getuser()}" />\n'
        html += f'<meta name="viewport" content="width=device-width" initial-scale = "1.0" />\n'
        for file in self.src_dir.glob('*.css'):
            html += f'<link rel="stylesheet" href="{file.resolve()}" />\n'

        html += f'</head>\n'

        return html

    def main_menu(self,attrib :dict = {}, **extra) ->BlockElement :

        header = BlockElement('header',attrib,**extra)

        ul=BlockElement('ul',{'id' : 'menu'})

        for k,v in self.pages.items():
            if k != self.__class__.firstpage:
                t = k
            else:
                t = self.name
            li = InlineElement('li')
            a = InlineElement('a',t,{'href': f'{k}.html', 'title' : f'Aller à {t}'})
            ul += li + a

        return header + ul
        
    def to_file(self, menu_on : bool = False):
        
        menu = self.main_menu()

        for name,page in self.pages.items():
            file = self.dest_dir / name
            file = file.with_suffix('.html')
            head = self.add_head(page)
            if menu_on is True :
                page.insert(0,self.main_menu())
            body = page.tostring()
             
            with file.open('w',encoding = 'utf-8') as f:
                f.write('<!DOCTYPE html>\n')
                f.write(head)
                f.write(body)
                f.write('\n</html>')

    def tostring(self):
        
        ret = ''
        for name,page in self.pages.items():
            ret += f'*** page : {name} ***:\n'
            ret += page.tostring()
            ret += f'\n*** end page : {name} ***\n'
        return ret

    def srcfile(self,value :str):
        
        ret = Path(self.src_dir / value)
        if(ret.exists()):
            return ret
        else:
            print('Bad file name !!')
            return None
