#!python3

from string import ascii_uppercase, ascii_lowercase, digits
import sys
import argparse


class Base64:
    def __init__(self, key):
        # Initialise default Base64 table
        table = list(ascii_uppercase + ascii_lowercase + digits + "+" + "/")
        indices = [i for i in range(64)]
        if key is not None:
            # Apply KSA
            keyLength = len(key)
            j = 0
            for i in range(64):
                j = (j + indices[i] + key[i % keyLength]) % 64
                indices[i], indices[j] = indices[j], indices[i]

        self.table = [""] * 64
        for i in range(64):
            self.table[i] = table[indices[i]]

    def chunk(self, data, length):
        return [data[i : i + length] for i in range(0, len(data), length)]

    def encode(self, data):
        override = 0
        if len(data) % 3 != 0:
            override = (len(data) + 3 - len(data) % 3) - len(data)
        data += b"\x00" * override

        threechunks = self.chunk(data, 3)

        binstring = ""
        for chunk in threechunks:
            for x in chunk:
                binstring += "{:0>8}".format(bin(x)[2:])

        sixchunks = self.chunk(binstring, 6)

        outstring = ""
        for element in sixchunks:
            outstring += self.table[int(element, 2)]

        if override == 0:
            return outstring
        outstring = outstring[:-override] + "=" * override
        return outstring

    def decode(self, data):
        override = data.count("=")
        data = data.replace("=", "A")

        binstring = ""
        for char in data:
            binstring += "{:0>6b}".format(self.table.index(char))

        eightchunks = self.chunk(binstring, 8)

        outbytes = b""
        for chunk in eightchunks:
            outbytes += bytes([int(chunk, 2)])

        if override == 0:
            return outbytes
        return outbytes[:-override]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="kase64",
        description="Base64 encrypt or decrypt FILE, or standard input, to standard output, using a key",
        epilog="When -k KEY flag is given, RC4's Key-scheduling algorthim (KSA) is used to permute Base64 encoding table. This generates a new table which is used to encode the data. Base64 implementation was taken from https://gist.github.com/trondhumbor/ce57c0c2816bb45a8fbb. RC4 Key-scheduling algorithm: https://en.wikipedia.org/wiki/RC4",
    )
    parser.add_argument("FILE", nargs="?")
    parser.add_argument(
        "-k",
        "--key",
        help="key for permuting table. If not given, the default Base64 table is used",
    )
    parser.add_argument("-d", "--decode", action="store_true", help="decode data")
    args = parser.parse_args()

    if args.FILE is None:
        data = sys.stdin.buffer.read()
    else:
        with open(args.FILE, "rb") as f:
            data = f.read()

    b64 = Base64(args.key.encode() if args.key else None)

    if args.decode:
        output = b64.decode(data.decode())
        sys.stdout.buffer.write(output)
    else:
        output = b64.encode(data)
        print(output)
