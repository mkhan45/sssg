# sssg

### Simple static site generator

For making a simple informational static site with a consistent navbar and footer as well as other common elements. Used for [kryptontutors.com](https://www.kryptontutors.com).

## Usage

```python
from sssg import Page, CSS
# put site-wide CSS in a global variable
css = [
    # buildwithboba.com
    CSS("boba/boba-extended.min.css"),
]

# commonly used global substitutions
example_sub = None
with open("templates/examblesub.html", "r") as f:
    examble_sub = f.read()
extrasubs = {
    "sub keyword" : examble_sub # replace {{sub keyword}} in html with the text of examble_sub
}

# initialize the Page with template "templates/index.html", site relative url "index.html", and canonical url "https://www.examplesite.com"
indexPage = Page("index.html", "templates/index.html", "https://www.examplesite.com/")

# set page to use the extra subs dictionary
indexPage.extrasubs = extrasubs

# set the title
indexPage.set_title(
    "Example Title"
)

# add a meta tag
indexPage.add_meta_tag(
    {
        "name" : "description",
        "content": "example description"
    }
)

# another meta tag
indexPage.add_meta_tag(
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
)

# set page to use the global CSS
indexPage.header.css = css 

# save the page taking the navbar from "templates/navbar.html" and footer from "templates/footer.html"
indexPage.save(navbar_path="templates/navbar.html", footer_path="templates/footer.html")
```
