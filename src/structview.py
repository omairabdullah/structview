#!/usr/bin/env python3

import struct_parser
import sys

def get_word_size(datastr):
    size = len(datastr[0])

    if size % 2 != 0:
        raise ValueError("invalid word size: {0}", size)

    # TODO: zero fill if inconsistent
    for data in datastr:
        if len(data) != size:
            raise ValueError("inconsistent word size")

    return size

def get_bytes_from_hexstr(data, endian='big'):
    ''' Convert a word from hexadecimal notation into a byte stream. '''
    if endian == 'little':
        return bytearray.fromhex(data)

    wd_size = len(data)
    start = wd_size - 2
    end = wd_size

    arr = bytearray()
    while start >= 0:
        try:
            byte = int(data[start:end], 16)
        except ValueError:
            print("invalid characters '{0}' - replacing with 0".format(data[start:end]))
            byte = 0

        arr.append(byte)
        end = start
        start -= 2

    return arr

# FIXME: increment bytestream and fill values
def fill_values(fields, bytestream):
    if len(fields) == 0:
        return

    (name, f) = fields[0]
    if len(f) == 1:
        var = f[0]
        print("{0}".format(var))
    else:
        fill_values(f, bytestream)

    fill_values(fields[1:], bytestream)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {0} '<hex data>'".format(sys.argv[0]))
        exit(1)

    datastr = sys.argv[1].split(' ')

    wd_size = get_word_size(datastr)
    print("word size: {0}".format(wd_size))

    bytestream = bytearray()
    for data in datastr:
        word = get_bytes_from_hexstr(data, endian='big')
        bytestream.extend(word)

    #print(bytestream)

    c1 = 'struct ABC { struct XYZ { int b; char y; } myXYZ; int l; } myABC;'

    struct_fields = struct_parser.parse_c_struct(c1)

    for f in struct_fields:
        fill_values(f, bytestream)
"""
NOTES:

    ALGO:
        1. get string data
        2. get structure type
        3. parse structure type
        4. convert string array into byte stream
        5. match byte stream to struct fields
        6. display structure fields

    Inputs:
    C-struct, python format etc
    data read from file, data read from command line as a string - ascii encoded
        data can be BE or LE

    Intermediate:
    data stored as a byte array

    Output:
    hex, dec and bin representation of data
    struct fields populated by hex,dec,bin
    highlighting of data based on struct fields

    Meta:
    single binary, no install, simple settings file
"""
