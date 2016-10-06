from HTMLParser import HTMLParser
import sys

"""
pattern parser - using a pattern to parse web pages

pattern:
tag - name of a html tag
>   - separate parent and child tag
:   - separate tag and attributes
&   - separate multiple name-value pairs
[]  - specifiy a attribute to return
"""
class PParser(HTMLParser):
	def __init__(self, pattern, filter):
		HTMLParser.__init__(self)
		self.tags = []
		self.rules = []
		self.found = []
		self.name = ''
		self.roffset = 0
		self.tstack = []
		self.filter = filter
		self._parse_pattern(pattern)

	def _reset(self):
		self.found = [False for x in range(len(tags))]
		self.roffset = 0
		self.tstack = []

	def _check_rules(self, attrs):
		"""
		check if a tag has specified attrs
		"""
		if not len(self.rules[self.roffset]):
			return True

		found = False
		for k, v in self.rules[self.roffset]:
			found = False
			for k2, v2 in attrs:
				if not k == k2:
					continue
				found = True
				if v == -1:
					continue
				if not v == v2:
					found = False
		return found

	def _get_value(self, attrs):
		"""
		return the value specified by self.name
		"""
		for k, v in attrs:
			if k == self.name:
				return v

	def _call_filter(self, attrs):
		"""
		call the filter
		"""
		if self.name == '':
			self.filter(attrs)
		else:
			self.filter(self._get_value(attrs))

	def handle_starttag(self, tag, attrs):
		if any(self.found):
			self.tstack.append((tag, -1))

		if not self.tags[self.roffset] == tag:
			return

		if not self._check_rules(attrs):
			return

		self.found[self.roffset] = True
		if all(self.found):
			self._call_filter(attrs)
		else:
			self.roffset += 1

		self.tstack.append((tag, 1))
		
	def handle_startendtag(self, tag, attrs):
		if not self.tags[self.roffset] == tag:
			return

		if not self._check_rules(attrs):
			return

		self._call_filter(attrs)

	def handle_data(self, data):
		if all(self.found[:-1]) and self.tags[-1] == 'TEXT':
			self.filter(data)
				
	def handle_endtag(self, tag):
		if not any(self.found):
			return

		t, v = self.tstack.pop()
		if not t == tag or v == 1:
			return

		if all(self.found):
			offset = self.roffset
		else:
			offset = self.roffset - 1

		self.found[offset] = False
		self.roffset -= 1
			
	def _parse_pattern(self, pattern):
		"""
		parse pattern into two parallel arrays
		"""
		# split tags
		tags = pattern.split('>')
		for tag in tags:
			# split tag and its attributes
			tn_tv = tag.split(':')
			rlist = []
			try:
				tn, tv = tn_tv
				self.tags.append(tn)
			except:
				# in case no attributes
				self.tags.append(tn_tv[0])
				self.rules.append(rlist)
				continue

			# split name-value pairs
			key_values = tv.split('&')
			for kv in key_values:
				# split name and value
				try:
					k, v = kv.split('=')
				except:
					# in case no values
					k = kv
					v = -1
				# in case a certain attribute is specified
				if k.startswith('['):
					self.name = k[1:-1]
				else:
					rlist.append((k,v))
			self.rules.append(rlist)
		self.found = [False for x in range(len(self.tags))]

if __name__ == '__main__':

    def f(attrs):
        print 'in filter:', attrs

	url = 'this is a web page url'
	p = 'table>tbody>tr:height=20>td>a:[href]'
	pp = PParser(p, f)
	"""
	print pp.tags
	print pp.rules
	print pp.found
	print pp.name
	"""

    # get the page from url and feed it to pp
    #page = read_url(url)
    #pp.feed(page)
