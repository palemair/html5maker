#!../myenv/bin/python3

from .htmlelement import HtmlElement

#html section tags 
def Body(content : str = '', attrib : dict = {}, **extra) -> HtmlElement:
    return HtmlElement('body',content,attrib, **extra)

def Main(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('main',content ,attrib, **extra)

def Section(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('section',content ,attrib, **extra)

def Article(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('article',content ,attrib, **extra)

def Aside(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('aside',content ,attrib, **extra)

def Address(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('address',content ,attrib, **extra)

def Nav(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('nav',content ,attrib, **extra)

def Menu(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('menu',content ,attrib, **extra)

def Header(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('header',content ,attrib, **extra)

def Footer(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('footer',content ,attrib, **extra)

def Ul(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('ul',content ,attrib, **extra)

def Ol(content :str = '', attrib : dict = {}, **extra):
    return HtmlElement('ol',content ,attrib, **extra)

def Img(src : str , alt : str = '',attrib : dict = {}, **extra):
    attrib.update({"src" : src})
    return HtmlElement('img', alt ,attrib, **extra)

def H1(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h1', content ,attrib, **extra)

def H2(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h2', content, attrib, **extra)

def H3(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h3', content ,attrib, **extra)

def H4(content : str, attrib : dict = {}, **extra):
    return HtmlElement('h4', content ,attrib, **extra)

def Li(content : str = '', attrib : dict = {}, **extra):
    return HtmlElement('li', content ,attrib, **extra)

def P(content : str, attrib : dict = {}, **extra):
    return HtmlElement('p', content ,attrib, **extra)

def A(content : str,href : str = "#", attrib : dict = {}, **extra):
    attrib.update({"href" : href})
    return HtmlElement('a', content ,attrib, **extra)

def CLASS(cls : str) :
    """fonction to avoid python keyword 'class'"""
    return({'class' : cls})
