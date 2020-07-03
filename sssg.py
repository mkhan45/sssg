from typing import Dict, List, Union, cast, Optional
import subprocess


class MetaTag:
    fields: Dict[str, str]

    def __init__(self, fields: Dict[str, str]):
        self.fields = fields

    def add_tag(self, name: str, val: str):
        self.fields[name] = val

    def __str__(self) -> str:
        retstr = "<meta"
        for (name, val) in self.fields.items():
            retstr += " " + f'{name}="{val}"'
        retstr += ">"
        return retstr


class CSS:  # pylint: disable=R0903
    path: str

    def __init__(self, path: str):
        self.path = path

    def __str__(self) -> str:
        return f'<link rel="stylesheet" href="{self.path}">'


class Header:  # pylint: disable=R0903
    tags: List[MetaTag]
    css: List[CSS]
    title: str
    canonical: Optional[str]

    def __init__(
        self,
        title: str = "Krypton Tutors",
        tags: Optional[List[MetaTag]] = None,
        css: Optional[List[CSS]] = None,
        canonical: Optional[str] = None,
    ):
        self.title = title
        self.tags = tags if tags is not None else []
        self.css = css if css is not None else []
        self.canonical = canonical

    def __str__(self) -> str:
        retstr = ""
        retstr += f"<title>{self.title}</title>\n"
        for tag in self.tags:
            retstr += str(tag) + "\n"
        for css in self.css:
            retstr += str(css) + "\n"
        retstr += f'<link rel="canonical" href="{self.canonical}">\n'
        return retstr


class Page:
    header: Header
    sitepath: str
    templatepath: str
    extrasubs: Dict[str, str]

    def __init__(self, sitepath: str, templatepath: str, title: str = "Krypton Tutors"):
        self.sitepath = sitepath
        self.templatepath = templatepath
        self.header = Header(title=title)
        self.header.tags = []
        self.header.css = []
        self.extrasubs = {}

    def set_title(self, title: str):
        self.header.title = title

    def add_meta_tag(self, tag: Union[MetaTag, Dict[str, str]]):
        if isinstance(tag, MetaTag):
            self.header.tags.append(cast(MetaTag, tag))
        else:
            self.header.tags.append(MetaTag(cast(Dict[str, str], tag)))

    def add_meta_tags(self, *tags: Union[MetaTag, Dict[str, str]]):
        for tag in tags:
            self.add_meta_tag(tag)

    def add_css(self, css: Union[str, CSS]):
        if isinstance(css, CSS):
            self.header.css.append(cast(CSS, css))
        else:
            self.header.css.append(CSS(cast(str, css)))

    def add_sub(self, key: str, val: str):
        self.extrasubs[key] = val

    def save(
        self,
        navbar: str = None,
        navbar_path: str = "navbar.html",
        footer: str = None,
        footer_path: str = "footer.html",
    ):
        template_cmd: List[str] = ["templater", self.templatepath]
        template_cmd.append(f"{{{{header}}}}={str(self.header)}")
        if navbar is None:
            with open(navbar_path, "r") as navbar_file:
                template_cmd.append(f"{{{{navbar}}}}={navbar_file.read()}")
        else:
            template_cmd.append(f"{{{{navbar}}}}={navbar}")

        if footer is None:
            with open(footer_path, "r") as footer_file:
                template_cmd.append(f"{{{{footer}}}}={footer_file.read()}")
        else:
            template_cmd.append(f"{{{{footer}}}}={footer}")

        extra_sub_cmd: List[str] = ["templater", "temp1.html"]
        for key, val in self.extrasubs.items():
            extra_sub_cmd.append(f"{{{{{key}}}}}={val}")

        fmt_cmd: List[str] = [
            "tidy",
            "-i",
            "--indent-spaces",
            "4",
            "-utf8",
            "-w",
            "120",
            "-q",
            "-o",
            self.sitepath,
            "temp2.html",
        ]
        with open("temp1.html", "w") as outfile:
            subprocess.run(template_cmd, stdout=outfile, check=False)
        with open("temp2.html", "w") as outfile:
            subprocess.run(extra_sub_cmd, stdout=outfile, check=False)
        subprocess.run(fmt_cmd, check=False)
        subprocess.run(["rm", "temp2.html"], check=False)
