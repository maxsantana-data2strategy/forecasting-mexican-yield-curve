import re
import zlib

# Reads the reference PDF and extracts the contents of the relevant objects.
data = open('docs/reference/ejercicio.pdf', 'rb').read()
objects = {int(number): body for number, body in re.findall(rb'([0-9]+) 0 obj(.*?)endobj', data, re.S)}


def stream(number):
    body = objects[number]
    start = body.find(b'stream')
    start = body.find(b'\n', start) + 1
    end = body.find(b'endstream', start)
    raw = body[start:end].rstrip(b'\r\n')
    return zlib.decompress(raw) if b'/FlateDecode' in body[:start] else raw


for number in (131, 132):
    print(f'--- CONTENT {number} ---')
    print(repr(stream(number)[:6000]))
