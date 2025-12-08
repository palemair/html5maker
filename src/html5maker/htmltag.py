#!../myenv/bin/python3

from .htmlelement import HtmlElement

#html section tags 
def Body(attrib : dict = {}, **extra) -> HtmlElement:
    return HtmlElement('body',attrib, **extra)

def Main(attrib : dict = {}, **extra):
    return HtmlElement('main',attrib, **extra)

def Section(attrib : dict = {}, **extra):
    return HtmlElement('section', attrib, **extra)

def Article(attrib : dict = {}, **extra):
    return HtmlElement('article' ,attrib, **extra)

def Aside(attrib : dict = {}, **extra):
    return HtmlElement('aside', attrib, **extra)

def Nav( attrib : dict = {}, **extra):
    return HtmlElement('nav', attrib, **extra)

def Address(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('address',attrib, content, **extra)

def Header(attrib : dict = {}, **extra):
    return HtmlElement('header', attrib, **extra)

def Footer(attrib : dict = {}, **extra):
    return HtmlElement('footer', attrib, **extra)

def Ul(attrib : dict = {}, **extra):
    return HtmlElement('ul',attrib, **extra)

def Ol(attrib : dict = {}, **extra):
    return HtmlElement('ol', attrib, **extra)

def Img(src : str , alt : str = '',attrib : dict = {}, **extra):
    attrib.update({"src" : src})
    return HtmlElement('img', alt ,attrib, **extra)

def H1(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h1', attrib,content, **extra)

def H2(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h2', attrib,content, **extra)

def H3(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h3', attrib,content, **extra)

def H4(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h4', attrib,content, **extra)

def Li(attrib : dict = {}, **extra):
    return HtmlElement('li', attrib, **extra)

def P(content : str, attrib : dict = {}, **extra):
    return HtmlElement('p', attrib, content, **extra)

def A(content : str,href : str = "#", attrib : dict = {}, **extra):
    attrib.update({"href" : href})
    return HtmlElement('a', attrib,content, **extra)

def CLASS(cls : str) :
    """fonction to avoid python keyword 'class'"""
    return({'class' : cls})
