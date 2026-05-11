#!../../myenv/bin/python3

import os
from pathlib import Path
from getpass import getuser
from .htmlelement import FactoryElement


class Pages(dict):
    """
    Wrapper dict around pages collection Document object:
    Allowing to avoid the index name for the first web page
    labels : name + filename(== name except 1st == index).html
    """

    def filenames(self):
        index, *others = list(self.keys())
        index = "index.html"
        others = (f"{title}.html" for title in others)

        return (index, *others)

    def labels(self):
        return tuple(zip(self.keys(), self.filenames()))

    def all_items(self):
        return tuple(zip(self.keys(), self.values(), self.filenames()))


class HtmlDocument(FactoryElement):
    """
    Document object: contains the name of the project,
    directories src and dest to put the files, the language, the css files,
    and the authors informations.
    pages == each independant part of the global document
    """

    def __init__(
        self,
        name: str,
        logo: [str | os.PathLike] = None,
        src_dir: [str | os.PathLike] = ".",
        dest_dir: [str | os.PathLike] = "~/Bureau",
        lang: str = "fr",
    ):

        self.name = name
        self.lang = lang
        self.pages = Pages()

        try:
            self.logo = Path(logo).name

        except TypeError:
            self.logo = None

        try:
            src = Path(src_dir).expanduser().absolute()

        except (FileNotFoundError, NotADirectoryError):
            print(f"{dest_dir} : Path is not a valid filenanme or not a directory !!")
            return

        super().__init__(src)

        try:
            dest = Path(dest_dir).expanduser().absolute()

        except (FileNotFoundError, NotADirectoryError):
            print(f"{dest_dir} : Path is not a valid filenanme or not a directory !!")
            return

        self.dest = dest / name
        self.dest.mkdir(exist_ok=True)

    def add(self, title: str, element):

        if title not in self.pages.keys():
            self.pages[title] = element
        else:
            print("Page exist, can't duplicate !!")

        return self

    def remove(self, title: str):

        if title in self.pages.keys():
            self.pages.pop(title)
        else:
            print("Not in the document !!")

        return self

    def __repr__(self):

        ret = (f"{n} -> {f}" for n, f in self.pages.labels())
        return "\n".join(ret)

    def save(
        self,
        menu_on: bool = True,
        attr: dict = {"class": "global"},
        indent: bool = False,
    ):

        css_dir = self.src / "styles"
        js_dir = self.src / "js"

        for name, page, filename in self.pages.all_items():
            html = []
            file = self.dest / filename

            head = f'<html lang ="{self.lang}">'
            head += f'<head><meta charset = "utf-8" />'
            head += f'<meta name="author" content="{getuser()}" />'
            head += f'<meta name="viewport" content="width=device-width" initial-scale = "1.0" />'
            head += f"<title>{name}</title>"
            for css in css_dir.glob("*.css"):
                head += f'<link rel="stylesheet" href="styles/{css.name}"/>'
            for js in js_dir.glob("*.js"):
                head += f'<script defer src="js/{js.name}"></script>'

            head += f"</head>\n<body>\n"

            html.append(head)

            header = self.html_tag("header", attr)
            div = self.html_tag("div")

            if self.logo is not None:
                lg = self.html_tag("img", {"src": f"images/{self.logo}"})
                div += lg

            if len(self.pages) > 1:
                nav = self.html_tag("nav")
                ul = self.html_tag("ul")
                tmpdict = {n: f for n, f in self.pages.labels() if n != name}

                for n, f in tmpdict:
                    li = self.html_tag("li")
                    a = self.html_tag(
                        "a", name, {"href": f"{filename}", "title": f"Aller à {name}"}
                    )
                    ul += li + a
                nav += ul
                div += nav

            header += div

            html.append(header.to_html_string())

            content = page.to_html_string(indent=indent)
            html.append(content)

            html.insert(0, """<!DOCTYPE html>\n""")
            footer = self.html_tag("footer", attr)
            footer += self.html_tag("p", content=name)

            html.append(footer.to_html_string())
            html.append("""\n</body>\n</html>""")

            h = "".join(html)

            with file.open("w", encoding="utf-8") as f:
                f.write(h)

    def tostring(self):

        ret = ""
        for k, v in self.pages.items():
            ret += f"\n*** page : {k} ***:\n"
            ret += v.to_html_string()
            ret += f"\n*** end page : {k} ***"

        return ret
