#!../myenv/bin/python3

from .htmlelement import BlockElement, InlineElement

#html section tags 
def Main(attrib : dict = {}, **extra):
    return BlockElement('main',attrib, **extra)

def Section(attrib : dict = {}, **extra):
    return BlockElement('section',attrib, **extra)

def Article(attrib : dict = {}, **extra):
    return BlockElement('article',attrib, **extra)

def Aside(attrib : dict = {}, **extra):
    return BlockElement('aside',attrib, **extra)

def Address(attrib : dict = {}, **extra):
    return BlockElement('address',attrib, **extra)

def Nav(attrib : dict = {}, **extra):
    return BlockElement('nav',attrib, **extra)

def Menu(attrib : dict = {}, **extra):
    return BlockElement('menu',attrib, **extra)

def Header(attrib : dict = {}, **extra):
    return BlockElement('header',attrib, **extra)

def Footer(attrib : dict = {}, **extra):
    return BlockElement('footer',attrib, **extra)

def Ul(attrib : dict = {}, **extra):
    return BlockElement('ul',attrib, **extra)

def Ol(attrib : dict = {}, **extra):
    return BlockElement('ol',attrib, **extra)

#html text tags 
def H1(content : str, attrib : dict = {}, **extra):
    return InlineElement('h1',content, attrib, **extra)

def H2(content : str, attrib : dict = {}, **extra):
    return InlineElement('h2',content, attrib, **extra)

def H3(content : str, attrib : dict = {}, **extra):
    return InlineElement('h3',content, attrib, **extra)

def H4(content : str, attrib : dict = {}, **extra):
    return InlineElement('h4',content, attrib, **extra)

def Li(content : str = '', attrib : dict = {}, **extra):
    return InlineElement('li',content, attrib, **extra)

def P(content : str, attrib : dict = {}, **extra):
    return InlineElement('p',content, attrib, **extra)

def A(content : str,href : str = "#", attrib : dict = {}, **extra):
    attrib.update({"href" : href})
    return InlineElement('a',content, attrib, **extra)

def Img(src : str , alt : str = '',attrib : dict = {}, **extra):
    attrib.update({"alt" : alt})
    return InlineElement('img',content, attrib, **extra)

def CLASS(cls : str) :
    """fonction to avoid python keyword 'class'"""
    return({'class' : cls})
