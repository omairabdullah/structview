#!/usr/bin/env python3

class StructureField:
    __sv_format = {
            's8'  : 'b',
            'u8'  : 'B',
            's16' : 'h',
            'u16' : 'H',
            's32' : 'i',
            'u32' : 'I',
            's64' : 'q',
            'u64' : 'Q',
    }
    __sv_widths = {
            's8'  : 8,
            'u8'  : 8,
            's16' : 16,
            'u16' : 16,
            's32' : 32,
            'u32' : 32,
            's64' : 64,
            'u64' : 64,
    }
    __canonical_names = {
            's8'            : 's8',
            'char'          : 's8',
            'int8_t'        : 's8',

            'u8'            : 'u8',
            'unsigned char' : 'u8',
            'unsigned short': 'u8',
            'uint8_t'       : 'u8',

            's16'           : 's16',
            'int16_t'       : 's16',
            'short'         : 's16',
            'short int'     : 's16',

            'u16'           : 'u16',
            'uint16_t'      : 'u16',
            'unsigned short': 'u16',
            'unsigned short int': 'u16',

            's32'           : 's32',
            'int32_t'       : 's32',
            'int'           : 's32',

            'u32'           : 'u32',
            'uint32_t'      : 'u32',
            'unsigned int'  : 'u32',

            's64'           : 's64',
            'int64_t'       : 's64',
            'long'          : 's64',
            'long int'      : 's64',
            'long long'     : 's64',
            'long long int' : 's64',

            'u64'           : 'u64',
            'uint64_t'      : 'u64',
            'unsigned long' : 'u64',
            'unsigned long int': 'u64',
            'unsigned long long': 'u64',
            'unsigned long long int': 'u64',
    }

    def __init__(self, name, canon_name='u32', width=32, value=0):
        self.var_name = name
        self.canon_name = canon_name
        self.bit_width = width
        self.value = value

    def __str__(self):
        return "<'{0}' - {1}: {2}>".format(self.var_name, self.canon_name, self.bit_width)

    def __repr__(self):
        return "<'{0}' - {1}: {2}>".format(self.var_name, self.canon_name, self.bit_width)

    @classmethod
    def create_from_string(cls, c_string):
        c_string = c_string.lstrip().rstrip()
        var_name_idx = c_string.rfind(' ')
        var_name = c_string[var_name_idx + 1:]
        var_type = c_string[:var_name_idx]

        if var_type not in cls.__canonical_names.keys():
            raise TypeError("unknown type: '{0}' for variable '{1}'".format(var_type, var_name))

        canon_name = cls.__canonical_names[var_type]
        width = cls.__sv_widths[canon_name]

        return (var_name, [cls(var_name, canon_name, width)])


