# The chars we get out of a python str are unicode characters
# The identity of a character is its code point from 0 -> 1,114,111
# or in hex with the U+ prefix from U+0000 to U+20AC
# The actual bytes used to represent a character depend on the encoding used
# In the UTF-8 encoding A (U+0041) is encoded as the SINGLE byte \x41
# Other characters may need more bytes to encode them depending on how big the code point is
# code point -> bytes = encoding and bytes -> code points = decoding

s = "cafè"
print(len(s))

b = s.encode('utf8')
print(b) # b'caf\xc3\xa8' è is encoded as two bytes 
c = b.decode('utf8')
print(c)

cafe = bytes("cafè", encoding="utf_8")
print(cafe)
print(cafe[0])
print(cafe[3])
print(cafe[:1])
cafe_arr = bytearray(cafe)
print(cafe_arr)
print(cafe_arr[-1:])
# a Byte is an int (0-255). For bytes in the range 32-126, the ASCII character is used
# See that \xc3 = dec 195 and so hex is used

for codec in ["latin_1", "utf_8", "utf_16"]:
    print(codec, "El Niño".encode(codec), sep="\t")

# Coping with unicode errors
city = "São Paulo"
city.encode("utf_8")
city.encode("utf_16")
# city.encode("cp437") # UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in position 1: character maps to <undefined>
# cp437 cannot support ñ
a = city.encode("cp437", errors='ignore') # Bad idea, silent data loss
print(a.decode("cp437")) # So Paulo
a = city.encode("cp437", errors='replace')
print(a.decode("cp437")) # S?o Paulo
a = city.encode("cp437", errors='xmlcharrefreplace') # Replace with an xml entity
print(a.decode("cp437")) # S&#227;o Paulo -> &#227; = ã
b = a.decode("cp437")

import html
print(html.unescape(b)) # São Paulo

# Suppose you have a byte sequence you are trying to decode, not all of those bytes may be valid utf-8 or utf-16
# When converting to text you may get a UnicodeDecodeError if any unexpected bytes are found
octets = b"Montr\xe9al"
print(octets.decode("cp1252")) # Montréal works
print(octets.decode("iso8859_7")) # Montrιal Decoded \xe9 as the wrong char
try:
    octets.decode("utf_8")
except UnicodeDecodeError as e:
    # 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
    print(e)

# So, how do you know what the encoding of a byte sequence is? You don't, you need to be told.
open("cafe.txt", "w", encoding="utf_8").write("cafè")
print(open("cafe.txt").read()) # But if we did this on a windows machine, by default it uses cp1252
# We should never rely on encoding defaults
f = open("cafe.txt", "rb").read()
print(f)

# Normalizing unicode for reliable comparisons
s1 = "café"
s2 = "cafe\N{COMBINING ACUTE ACCENT}" # Using a unicode literal
print(s1, s2)
print(len(s1), len(s2))
print(s1 == s2)

from unicodedata import normalize

s1 = "café"
s2 = "cafe\N{COMBINING ACUTE ACCENT}"
print(len(normalize("NFC", s1)), len(normalize("NFC", s2)))
print(normalize("NFC", s1) == normalize("NFC", s2))

from unicodedata import name
print(name("A"))
print(name("🐈"))