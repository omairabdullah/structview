#!/usr/bin/env python3

import structview as sv
import struct_parser as sp
import pprint

code = """typedef struct abc {
    //const void *p; \n
    unsigned int b; \n
    static const int d; \n
    extern int e; \n
    //virtual void *myfunc() = 0; \n
    volatile uint32_t f:22; \n
    u8      g:2; \n
    char y;  \n
    /* a multiline comment to simply mess with people */ \n
    //char x, y;     \n
    union myunion {  int q;  long d;  } part1; \n
    union {  \n
        struct {  \n
            u32 low:32;  \n
            u32 high:32; \n
        } part; \n
        u64 full;  \n
    } header; \n
    /* a multiline comment to simply mess with people \n\n 	 spanning multiple lines now */ \n
} some_type_t mystruct;
"""

pp = pprint.PrettyPrinter(indent = 4)
flds = sp.parse_c_struct(code)
pp.pprint(flds)
sv.fill_values(flds, b'\x00')
