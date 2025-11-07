#!./env/bin/python3

import container
from pathlib import Path

#Concrete html section 
class Body(container.HtmlSection):
    __slots__ = ('title',)
    def __init__(self,title : str,**kwargs):
        super().__init__('body',**kwargs)
        self.title = title

class Main(container.HtmlSection):

    """Simple html page object"""
    def __init__(self, **kwargs):
        super().__init__('main',**kwargs)

class Section(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('section', **kwargs)

class Article(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('article', **kwargs)

class Header(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('header', **kwargs)

class Footer(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('footer', **kwargs)

class Ul(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('ul', **kwargs)

class Li(container.HtmlSection):
    
    def __init__(self, **kwargs):
        super().__init__('li', **kwargs)

#Concrete html text 

class h1(container.HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('h1',input_str,**kwargs)

class h2(container.HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('h2',input_str,**kwargs)

class A(container.HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('a',input_str,**kwargs)

class Paragraph(container.HtmlText):
    
    def __init__(self,input_str : str = '', **kwargs):
        super().__init__('p',input_str,**kwargs)


# class Img(HtmlContainer):

#     def __init__(self,imgdatas:dict = None,attrib: dict = {'class':'image'}) :

#         super().__init__(attrib,caption)
#         self.imgdatas = imgdatas
#         self.__initialize()
    
#     def __initialize(self):
        
#         if self.imgdatas is not None:
#             elt=etree.Element('img')
#             for k,v in self.imgdatas.items():
#                 elt.set(k,v )
#             self._root.insert(0,elt)

# class Figure(HtmlContainer):
    
#     def __init__(self,caption_class : str = None, caption_text : str = None, **kwargs):

#         super().__init__('figure', **kwargs)
        
#         if self.caption is not None:
#             fc=et.Element('figcaption')
#             fc.set('class', caption_class)
#             fc.text= caption_text

#         self.root.append(fc)

if __name__ == '__main__':

    home = Main()
    home.append(h1("title"))
    home.add_from_markdown("#Mardownprojet \n \n tredffg",parent = 'nav')
    home.add_from_markdown(Path('Markdown/projet.md'),parent = 'article')
    home.add_from_markdown(Path('Markdown/article.md'))
    home.add_from_markdown(Path('Markdown/article2.md'))
    div = home.create_section_tag('div')
    home.append(Paragraph("Un deuxieme"))

    print(home,end ='')
