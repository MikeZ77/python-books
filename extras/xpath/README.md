<bookstore>
  <book>
    <title lang="en">Harry Potter</title>
    <author>J K. Rowling</author>
    <year>2005</year>
    <price>29.99</price>
  </book>
</bookstore>

The most important types of nodes are element, attribute, text, namespace

lang="en" = attribute node
<bookstore> = root node
J K. Rowling = text

A namespace is a way to avoid naming conflicts between elements and attributes
Namespaces are declared using a URI (Uniform Resource Identifier) and are associated with a prefix

<root xmlns:ns1="http://example.com/ns1" xmlns:ns2="http://example.com/ns2">
  <ns1:element1>Value 1</ns1:element1>
  <ns2:element2>Value 2</ns2:element2>
</root>

Here xmlns:ns1 is an attribute that declares the namespace http://example.com/ns1. It uses the
prefix ns1 to assoicate the attribute and elements with the namespace.

So using the prefix ns1 associates that element with the namespace "http://example.com/ns1"
On the other hand <title lang="en"> is just an attribute because it does not use a prefix.

Relationship of Nodes:

In the bookstore exmaple:

<book> is a PARENT of <title> <author> <year> and <price>

<title> is a CHILD of <book>
<year> is a SIBLING of <price>
<bookstore> is the ANCESTOR of <year>, as is its PARENT <title>
<year> is a DESCENDANT of <bookstore>
