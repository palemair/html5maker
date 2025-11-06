#!./env/bin/python3

from svgtag import *
from htmltag import *

from pathlib import Path
from getpass import getuser

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
        if(dest_dir.startswith("~")):
            dest = Path(dest_dir).expanduser()
        else:
            dest = Path(dest_dir)

        self.dest_dir = Path(dest) / self.name
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
        css = self.css.read_text(encoding="utf-8")
        html += f'<style>{css}\n</style>\n</head>\n'

        return html

    def main_menu(self,cls : str = 'heading'):

        header = Header(**{'class' : cls})

        ul=Ul(id='menu')

        for k,v in self.pages.items():
            if k != self.__class__.firstpage:
                ul.append(Li().append(A(k,href=f'{k}.html',title=f'Aller à {k}')))
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
    d = Document(**config)

    home = Body(d.name)
    home.add_from_markdown(Path('Markdown/projet.md'),parent = 'article')

    linestyle = {'stroke' : 'blue', 'stroke-width' : '2px', 'fill' : 'gray'}
    groupe1 = Groupe(**linestyle)

    groupe1.basicshape('line',300,200,456,234)
    groupe1.basicshape('circle',300,200,45)

    with Svg() as dessin:

        dessin.append(groupe1)

        dessin.append(Texte(200,300,"test"))

        dessin.basicshape('ellipse',600,500,45,70, stroke = 'red',fill = 'green')
        dessin.basicshape('rect',300,700,300,150,**linestyle)

        dessin.append(Use("stric", transform="translate(200,150) scale(3) rotate(17)"))

    home.append(dessin)
    home.add_from_markdown(Path('Markdown/article.md'))
    home.add_from_markdown(Path('Markdown/article2.md'))

    nex = Body("next")
    denex = Body("denext")
    nex.add_from_markdown(Path('Markdown/article2.md'))
    d.add_page(home,nex,denex)
    d.to_file()
