from io import StringIO 

# an in-memory file like object
xml = StringIO("""
<library xmlns:book="http://example.com/books">
  <book:book category="fiction">
    <book:title lang="en">The Great Gatsby</book:title>
    <book:author>F. Scott Fitzgerald</book:author>
    <book:price currency="USD">12.99</book:price>
  </book:book>
  <book:book category="non-fiction">
    <book:title lang="en">The Elements of Style</book:title>
    <book:author>William Strunk Jr.</book:author>
    <book:author>E. B. White</book:author>
    <book:price currency="USD">9.99</book:price>
  </book:book>
  <book:book category="fiction">
    <book:title lang="fr">Le Petit Prince</book:title>
    <book:author>Antoine de Saint-Exupéry</book:author>
    <book:price currency="EUR">8.99</book:price>
  </book:book>
  <magazine category="science">
    <title>Scientific American</title>
    <issue>October 2023</issue>
    <price currency="USD">5.99</price>
  </magazine>
</library>
""")

"""
nodename	Selects all nodes with the name "nodename"
/	Selects from the root node
//	Selects nodes in the document from the current node that match the selection no matter where they are
.	Selects the current node
..	Selects the parent of the current node
@	Selects attributes
"""

from lxml import etree

# etree supports the standard ElementPath methods find, findall and findtext (limited xpath)
# But also supports the complete xpath syntax with xpath()

# reads from a file
tree = etree.parse(xml)

# Using some of the ElementTree methods
result = tree.find("/magazine/title") # find returns the first match
print(result) # <Element title at 0x7f135a684fc0>
print(result.tag, result.text) #title Scientific American

result = tree.find("//issue") # Finds the first node issue from the current node (root)
print(result)
print(result.tag, result.text)

result = tree.find("/book") 
print(result) # None


# We need to search on the namespace
namespaces = {'book': 'http://example.com/books'}
result = tree.find("//book:title", namespaces) # we need to provide find an ns map
print(result) # <Element {http://example.com/books}title at 0x7fcff5b09380>
print(result.tag, result.prefix, result.text) # {http://example.com/books}title book The Great Gatsby

# We can do this using xpath like:
result = tree.xpath("//book:title", namespaces=namespaces)[0]
# So we still need to provide the namespaces
print(result)
print(result.tag, result.prefix, result.text) # {http://example.com/books}title book The Great Gatsby

# select the magazine that has a title element = Scientific American and return the price element for it
result = tree.find('//magazine[title="Scientific American"]/price')
print(result)
print(result.tag, result.prefix, result.text)

# Find the book by author F. Scott Fitzgerald that is in english and is in the book namespace
# result = tree.find('//book:book[book:author="F. Scott Fitzgerald" and book:title[@lang="en"]]/book:price', namespaces)
# print(result) # invalid predicate
# print(result.tag, result.prefix, result.text)

result = tree.xpath('//book:book[book:author="F. Scott Fitzgerald" and book:title[@lang="en"]]/book:price', namespaces=namespaces)[0]
print(result)
print(result.tag, result.prefix, result.text)

from functools import partial

# xpath always returns a list
def get_xpath(tree, xpath, namespaces=None):
    res = tree.xpath(xpath, namespaces=namespaces)
    if len(res) == 1:
      return res[0]
    elif len(res) == 0:
      return None
    else:
      return res
    
get_xpath = partial(get_xpath, tree)

result = get_xpath('//book:book[book:author="F. Scott Fitzgerald" and book:title[@lang="en"]]/book:price', namespaces)
print(result)