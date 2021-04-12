from html.parser import HTMLParser
from urllib import parse

class LinkFinder(HTMLParser):
    def __init__(self, base_url, page_url):
        super().__init__()
        self.base_url =base_url
        self.page_url = page_url
        self.links = set()

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (attr,val) in attrs:
                if(attr == 'href'):
                    url = parse.urljoin(self.base_url, val)
                    self.links.add(url)
    def page_links(self):
        return self.links


# finder = LinkFinder()
#
# finder.feed('<html><head></head><body><h1>I am parsed</h1></body></html>')