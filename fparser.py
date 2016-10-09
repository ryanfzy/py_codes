from HTMLParser import HTMLParser

class FParser(HTMLParser):
    """
    A custermised parser class built by given filter(s).
    """
    def __init__(self, **filters):
        """
        A filter must be speicified as keyword argument.
        The key word is a valid HTML element.
        """
        # cannot use: super(MyParser, self).__init__()
        # because HTMLParser is a old style class
        HTMLParser.__init__(self)
        self.filters = {}
        self.values = {}
        self.add_filters(filters)

    def handle_starttag(self,tag,attrs):
        if(len(self.filters) > 0):
            for tagname, filter in self.filters.items():
                values = self.values.setdefault(tagname, [])
                if tag == tagname:
                    value = filter(attrs)
                    if value:
                        values.append(value)

    def get_values(self, tid):
        """
        Get values specified by the filter.
        The tagname must be the same as the key word for the filter.
        """
        return self.values[tid]

    def add_filters(self, filter):
        self.filters.update(filter)

if __name__ == '__main__':
    def filter1(attrs):
        #check attrs and return a desired value
        return 'a value'
    def filter2(attrs):
        return 'another value'

    page = 'a web page'
    parser = FParser(img=filter1, input=filter2)
    parser.feed(page)
    images = parser.get_values('img')
    input = parser.get_values('input')
