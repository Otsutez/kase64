# kase64

Base64 encrypt or decrypt FILE, or standard input, to standard output, using a key.

## Usage
```
usage: kase64 [-h] [-k KEY] [-d] [FILE]

Base64 encrypt or decrypt FILE, or standard input, to standard output,
using a key

positional arguments:
  FILE

options:
  -h, --help         show this help message and exit
  -k KEY, --key KEY  key for permuting table. If not given, the
                     default Base64 table is used
  -d, --decode       decode data

When -k KEY flag is given, RC4's Key-scheduling algorthim (KSA) is
used to permute Base64 encoding table. This generates a new table
which is used to encode the data. Base64 implementation was taken from
https://gist.github.com/trondhumbor/ce57c0c2816bb45a8fbb. RC4 Key-
scheduling algorithm: https://en.wikipedia.org/wiki/RC4
```

## Example
Normal Base64 encoding
```bash
echo -n "Many hands make light work." | ./kase64.py
```

Base64 encryption using a key
```bash
echo -n "Many hands make light work." | ./kase64.py -k secret_key
```

Decryption using a key
```bash
echo -n "a8qtnpZlN8EOLKZ1N815o6Ixy/PQoReFLCht" | ./kase64.py -d -k secret_key
```
