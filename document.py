#!./env/bin/python3

from pathlib import Path
from getpass import getuser

from html5.htmltag import *
from html5.svgtag import *

class Document:
    """ Web document object: it contains the name of the project,
        directory where to put the files, the language, the css files,
        and the authors informations. """

    firstpage = 'index'

    def __init__(self,name='LOREM IPSUM',
                      src_dir = '.',
                      dest_dir = '/home/patrice/Bureau',
                      md_dir = 'Markdown',
                      cssfile = 'styles/styles.css',
                      lang = 'fr',
                      **kwargs):

        self.name = name
        self.src_dir = Path(dest_dir)
        dest = Path(dest_dir)
        self.dest_dir = Path(dest) / self.name
        self.dest_dir = self.dest_dir.expanduser().absolute()
        self.dest_dir.mkdir(exist_ok = True)
        self.md_dir = Path(md_dir)
        self.css = Path(cssfile)
        self.lang = lang
        self.pages = {}

    def get_page(self,name:str):
        return self.pages[name]

    def add_page(self, *pages : Body)->Body:
        """Add new page. """

        for page in pages:
            if self.pages == {} :
                page.title = self.name
                self.pages[self.__class__.firstpage] = page

            elif (page.title not in self.pages.keys()):
                    self.pages[page.title] = page
        
            elif not isinstance(page,Body):
                print("Object have to be Body class")
            else :
                print("page exist, can't duplicate")

        return pages[-1]
         
    def _build_head(self,page : Body)-> str:

        html =f'<html lang ="{self.lang}">\n'

        #head of the page
        html += f'<head><meta charset = "utf-8" />\n'
        html += f'<title>{page.title}</title>\n'
        html += f'<meta name="author" content="{getuser()}" />\n'
        html += f'<meta name="viewport" content="width=device-width" initial-scale = "1.0" />\n'
        css = self.css.resolve()
        html += f'<link rel="stylesheet" href="{css}" />\n</head>\n'

        return html

    def main_menu(self,cls : str = 'heading'):

        header = Header(**{'class' : cls})

        ul=Ul(id='menu')

        for k,v in self.pages.items():
            if k != self.__class__.firstpage:
                t = k
            else:
                t = self.name
            ul.append(Li().append(A(t,href=f'{k}.html',title=f'Aller à {t}')))

        return header + ul
        
    def to_file(self):
        
        menu = self.main_menu()

        for name,page in self.pages.items():
            file = self.dest_dir / name
            file = file.with_suffix('.html')
            head = self._build_head(page)
            page.insert(0,menu)
            body = page.tostring()
             
            with file.open('w',encoding = 'utf-8') as f:
                f.write('<!DOCTYPE html>\n')
                f.write(head)
                f.write(body)
                f.write('\n</html>')

if __name__ == '__main__' :

    config = { 'src_dir' : '.',
               'name': "Lorem Ipsum",
               'dest_dir': "~/Bureau/",
               'lang'    : 'fr',
               'md_dir' : 'Markdown', 
               'cssfile' : 'styles/styles.css'
              }

    mydoc = Document(**config)

    home = Body(mydoc.name)

    main = Main()

    main += H1('Gros titre',CLASS('titres'))
    main.add_from_markdown(Path('Markdown/projet.md'),parent = 'article')

    linestyle = {'stroke' : 'blue', 'stroke-width' : '2px', 'fill' : 'gray'}

    with Svg(width = 600,height = 100) as dessin:

        dessin.basicshape('circle',300,50,25, stroke = 'blue',fill = 'green')
        dessin.basicshape('rect',0,0,150,50,**linestyle)

    main += dessin
    main.add_from_markdown(Path('Markdown/article.md'))
    main.add_from_markdown(Path('Markdown/article2.md'))

    home += main

    nex = Body("next")

    denex = Body("denext")
    nex.add_from_markdown(Path('Markdown/article2.md'))
    mydoc.add_page(home,nex,denex)
    mydoc.to_file()
