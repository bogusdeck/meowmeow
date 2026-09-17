import markdown
from pygments.formatters import HtmlFormatter
from AppKit import NSAttributedString, NSData, NSDictionary

md_text = """
Hello **bold blue** world!
```python
def foo(x):
    return x + 1
```
"""
html_body = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])
css = HtmlFormatter(style='monokai').get_style_defs('.codehilite')
full_html = f"<html><head><style>body {{ font-family: -apple-system; font-size: 14px; color: white; }} strong {{ color: #7cb9e8; }} {css}</style></head><body>{html_body}</body></html>"

html_data = NSData.dataWithBytes_length_(full_html.encode('utf-8'), len(full_html.encode('utf-8')))
options = NSDictionary.dictionaryWithDictionary_({"DocumentType": "NSHTMLTextDocumentType"})
res = NSAttributedString.alloc().initWithHTML_options_documentAttributes_(html_data, options, None)
if res:
    attr_str, doc_attrs = res
    print("Length:", attr_str.length())
    print("Attr at 6:", attr_str.attributesAtIndex_effectiveRange_(6, None))
