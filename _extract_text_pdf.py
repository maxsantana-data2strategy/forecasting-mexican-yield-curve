import re, zlib

# Extract raw text from PDF objects using font maps.
data = open('docs/reference/ejercicio.pdf', 'rb').read()
objects = {int(n): b for n, b in re.findall(rb'(\d+) 0 obj(.*?)endobj', data, re.S)}


def stream(n):
    b = objects[n]
    a = b.find(b'stream')
    a = b.find(b'\n', a) + 1
    e = b.find(b'endstream', a)
    raw = b[a:e].rstrip(b'\r\n')
    return zlib.decompress(raw) if b'/FlateDecode' in b[:a] else raw


def cmap(n):
    s = stream(n).decode('latin1')
    out = {}
    for block in re.findall(r'beginbfchar(.*?)endbfchar', s, re.S):
        for a, b in re.findall(r'<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>', block):
            out[int(a, 16)] = bytes.fromhex(b).decode('utf-16-be')
    for block in re.findall(r'beginbfrange(.*?)endbfrange', s, re.S):
        for a, b, c in re.findall(r'<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>', block):
            for i in range(int(a, 16), int(b, 16) + 1):
                out[i] = bytes.fromhex(f'{int(c,16)+i-int(a,16):04x}').decode('utf-16-be')
    return out

maps = {'f0': cmap(120), 'f1': cmap(123), 'f2': cmap(126), 'f3': cmap(129)}
for page, obj in enumerate((131, 132), 1):
    s = stream(obj).decode('latin1')
    font = 'f1'
    print(f'--- PAGE {page} ---')
    for token in re.finditer(r'/([f][0-3])\s+\d+\s+Tf|\[((?:\\.|[^]])*)\]\s*TJ|\((.*?)\)\s*Tj', s, re.S):
        if token.group(1):
            font = token.group(1)
            continue
        raw = token.group(2) if token.group(2) is not None else token.group(3)
        vals = re.findall(r'\\([0-7]{1,3})|\\([\\()\\])|([^()\\]+)', raw)
        bs = bytearray()
        for octal, escaped, plain in vals:
            if octal:
                bs.append(int(octal, 8))
            elif escaped:
                bs.extend(escaped.encode('latin1'))
            else:
                bs.extend(plain.encode('latin1'))
        m = maps[font]
        text = ''.join(m.get(int.from_bytes(bs[i:i+2], 'big'), '') for i in range(0, len(bs)-1, 2))
        if text.strip():
            print(text)
