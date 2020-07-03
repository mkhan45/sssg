from typing import List, Dict
from sssg import Page, CSS

css: List[CSS] = []
defaultTags: List[Dict] = [
    {
        "name": "og:title",
        "property": "og:title",
        "content": "SSSG | Simple Static Site Generator",
    },
    {
        "name": "description",
        "content": "Simple Python Static Site generator for informational websites \
                    that need a consistent header, navbar, and footer with unique meta tags",
    },
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    {"charset": "utf-8"},
]

indexPage = Page("index.html", "templates/index.html")  # pylint: disable=C0103
indexPage.set_title("SSSG | Simple Static Site Generator")
indexPage.add_meta_tags(*defaultTags)
indexPage.add_sub("extrasub1", "<span><h1>test</h1></span>")
indexPage.header.css = css
indexPage.save(navbar_path="templates/navbar.html", footer_path="templates/footer.html")
