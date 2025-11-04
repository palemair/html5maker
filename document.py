#!./env/bin/python3

from container import et,HtmlSection, HtmlText, SvgContainer
from pathlib import Path
from getpass import getuser

class Page(HtmlSection):

    def __init__(self,title : str = 'example', **kwargs):
        super().__init__('body',**kwargs)
        self.title = title

class Document:
    """ Website object: it contains the name of the project,
        directory where to put the files, the used language, the name of
        the css files, and the authors informations. """

    def __init__(self,name='LOREM IPSUM',
                      src_dir = '.',
                      dest_dir = '.',
                      md_dir = 'Markdown',
                      cssfile = 'styles/styles.css',
                      lang = 'fr',
                      **kwargs):

        self.name = name
        self.src_dir = Path(dest_dir)
        self.dest_dir = Path(dest_dir)
        self.md_dir = Path(md_dir)
        self.css = Path(cssfile)
        self.lang = lang
        self.pages = {}

    def get_page(self,name:str):
        return self._pages[name]

    def add_page(self, title : str):
        """Add a new web page. """
        if self.pages == {} :
            self.pages['index'] = Page(self.name)

        elif (title not in self.pages.keys()):
                self.pages[title] = Page(title)
        
        else :
            print("page exist, can't duplicate")

        return self
         
    def _build_head(self,page : Page)-> str:

        html =f'<html lang ="{self.lang}">\n'

        #head of the page
        html += f'<head><meta charset = "utf-8" />\n'
        html += f'<title>{page.title}</title>\n'
        html += f'<meta name = "author" content="{getuser()}" />\n'
        html += f'<meta name = "viewport" content="width=device-width" initial-scale = "1.0" />\n'
        html += f'<link href = "{self.css.resolve()}" rel = "stylesheet" />\n</head>\n'

        return html

    def _pages_menu(self):

        ul=et.Element('ul',**{'id':'menu'})

        for k,v in self.pages.items():
            if k != WebSite.firstpage:
                li=et.SubElement(ul,'li')
                a=et.SubElement(li,'a',href=f'{k}.html',title=f'Aller à {k}')
                a.text=k
                element=v._link_list()
                li.append(element)
        return ul

    def to_file(self):

        for name,page in self.pages.items():
            file = Path.expanduser(self.dest_dir) / name
            file = file.with_suffix('.html')
            head = self._build_head(page)
            body = page.tostring()
             
            with file.open('w',encoding = 'utf-8') as f:
                f.write('<!DOCTYPE html>\n')
                f.write(head)
                f.write(body)
                f.write('\n</html>')

if __name__ == '__main__' :

    config = { 'src_dir' : '.',
               'name': "Arbre binaire",
               'dest_dir': "~/Bureau/",
               'lang'    : 'fr',
               'md_dir' : 'Markdown' 
              }

    d = Document(**config)
    d.add_page('test')
    d.to_file()
