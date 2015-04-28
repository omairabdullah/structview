#!/usr/bin/env python3

import structview
import struct_parser
import unittest

class TestStrConversion(unittest.TestCase):

    # in big-endian
    known_values = (('00', b'\x00'),
                    ('10', b'\x10'),
                    ('ab', b'\xab'),
                    ('ba', b'\xba'),
                    ('ff', b'\xff'),
                    ('0$', b'\x00'),
                    ('xx', b'\x00'),
                    ('fx', b'\x00'),
                    ('00fa', b'\xfa\x00'),
                    ('0fa0', b'\xa0\x0f'),
                    ('f00a', b'\x0a\xf0'),
                    ('fa00', b'\x00\xfa'),
                    ('faff', b'\xff\xfa'),
                    ('0c0d0e', b'\x0e\x0d\x0c'),
                    ('0e0d0c', b'\x0c\x0d\x0e'),
                    ('e0d0c0', b'\xc0\xd0\xe0'),
                    ('fffefd', b'\xfd\xfe\xff'),
                    ('00010203', b'\x03\x02\x01\x00'),
                    ('03020100', b'\x00\x01\x02\x03'),
                    ('f3e2d1c0', b'\xc0\xd1\xe2\xf3'),
    )

    def test_str_conversion(self):
        for string, byte in self.known_values:
            result = structview.get_bytes_from_hexstr(string, endian='big')
            self.assertEqual(byte, result)

class TestStructParser(unittest.TestCase):
    sample_comments = (('/* abcdef1234567890!@#$%^&*()-=_+[]{}|;:",./<>?~`\n\r\n\r */', ''),
                       ('some /*abcdef*/ code', 'some  code'),
                       ('some /* abcdef */\ncode1', 'some \ncode1'),
                       ('some /* abcdef */\n/*abcc*/code2', 'some \ncode2'),
                       ('// abcdef1234567890!@#$%^&*()-=_+[]{}|;:",./<>?~`', ''),
                       ('some// abcdef', 'some'),
                       ('// abcdef \ncode3', '\ncode3'),
                       ('// abcdef \r\ncode4', '\ncode4'),
    )

    sample_keywords = (('const static unsigned int', '  unsigned int'),
                       ('const static void *myptr', '  void *myptr'),
                       ('struct abc { const int *p; } __attribute__((packed));', 'struct abc {  int *p; } ;'),
    )

    sample_spaces = ((' testing\tspace   regular\t\nexpression \n\n.', ' testing space regular expression .'),
    )

    sample_paren = (('struct abc { union bde { int x,y; } myu; } myabc;', 41),
                    ('struct abc { union bde { int x,y; struct xx { unsigned int yy; }; } myu; } myabc;', 73),
                    ('{}', 1),
                    ('{{}}', 3),
                    ('{{}{}{}}', 7),
                    ('code without any parenthesis', -1),
                    ('}{', -1),
                    ('{xxx{yyy}', -1),
                    ('{xxx{yy{a}{b}{c}y}', -1),
                    ('{xxx{yy{{{d}}}y}', -1),
    )

    sample_structs = (('char c; union bde { int x,y; } myu; } myabc;', (18, 29)),
                      ('struct abc { char c; union bde { int x,y; struct xx { unsigned int yy; }; } myu; } myabc;', (11, 81)),
    )

    def run_test(self, kv_pair, tested_function):
        for code, parsed in kv_pair:
            result = tested_function(code)
            self.assertEqual(parsed, result)

    def test_remove_comments(self):
        self.run_test(self.sample_comments, struct_parser.remove_comments)

    def test_remove_keywords(self):
        self.run_test(self.sample_keywords, struct_parser.remove_keywords)

    def test_remove_spaces(self):
        self.run_test(self.sample_spaces, struct_parser.remove_spaces)

    def test_find_matchin_paren(self):
        self.run_test(self.sample_paren, struct_parser.find_matching_paren)

    def test_find_first_substructure(self):
        self.run_test(self.sample_structs, struct_parser.find_first_substructure)

    sample_structs1 = (((18, 29), 'char c; union bde { int x,y; } myu; } myabc;', (6, 35, "union bde myu")),
                       ((11, 81), 'struct abc { char c; union bde { int x,y; struct xx { unsigned int yy; }; } myu; } myabc;', (-1, 89, "struct abc myabc")),
                       ((52, 71), 'struct abc { char c; union bde { int x,y; struct xx { unsigned int yy; }; } myu; } myabc;', (40, 73, "struct xx")),
                       ((11, 65), 'struct ABC { char c; struct XYZ { int b; char y; } myXYZ; int l; } myABC;', (-1, 73, "struct ABC myABC")),
                       ((32, 49), 'struct ABC { char c; struct XYZ { int b; char y; } myXYZ; int l; } myABC;', (19, 57, "struct XYZ myXYZ")),
                      # not a valid TC
                      #((24, 41), 'struct ABC { struct XYZ { int b; char y; } myXYZ; int l; } myABC;', (12, 49, "struct XYZ myXYZ")),
    )
    def test_get_struct_name(self):
        for args, code, parsed in self.sample_structs1:
            result = struct_parser.get_struct_name(code, *args)
            self.assertEqual(parsed, result)

if __name__ == '__main__':
    unittest.main()
