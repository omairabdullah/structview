#!/usr/bin/env python3

from structurefield import StructureField
import re

# TODO: replace by libclang

__comments_multiline_re = re.compile(r'/\*.*?\*/', re.DOTALL)
__comments_singleline_re = re.compile(r'//.*$', re.MULTILINE)
__unused_keywords_re = re.compile(r'static|const|extern|inline|virtual|volatile|typedef|__attribute__\(\(.*\)\)')
__extra_spaces_re = re.compile(r'[\s]+')

def remove_comments(code):
    code = __comments_singleline_re.sub("", code)
    code = __comments_multiline_re.sub("", code)
    return code

def remove_keywords(code):
    return __unused_keywords_re.sub("", code)

def remove_spaces(code):
    return __extra_spaces_re.sub(" ", code)

def find_matching_paren(code, open_paren='{', close_paren='}'):
    ''' Returns the index of the closing parenthesis matching the opening one. '''

    unmatched_paren_count = 0
    for i in range(len(code)):
        if code[i] == open_paren:
            unmatched_paren_count += 1
        elif code[i] == close_paren:
            unmatched_paren_count -= 1
            if unmatched_paren_count == 0:
                return i

    return -1

def find_first_substructure(code):
    """ Returns the indexes of the first embedded structure found in the declarations. """

    start_subexpr = code.find('{')
    # no embedded struct found
    if start_subexpr == -1:
        return (-1, -1)

    end_subexpr = find_matching_paren(code)
    if end_subexpr == -1:
        raise SyntaxError("invalid syntax - no match for opening parenthesis "
                          "in '{0}', start: {1}".format(code, start_subexpr))

    return (start_subexpr, end_subexpr)

def get_struct_name(code, start_subexpr, end_subexpr):
    """ Get the name of a structure given the positions of its open & close parentheses. """

    struct_name = ""
    # find expression just before this struct
    prev_expr = code.rfind(';', 0, start_subexpr)
    if prev_expr != -1:
        name_start = prev_expr + 1
        struct_name += code[name_start : start_subexpr - 1]
    # does not handle the case of this struct being the first substruct in the code
    # the calling function takes care to not include the enclosing struct declaration
    elif start_subexpr > 0:
        struct_name += code[:start_subexpr - 1]

    # find expression just after this struct
    next_expr = code.find(';', end_subexpr)
    if next_expr != -1:
        name_end = next_expr
        struct_name += code[end_subexpr + 1 : name_end]
        next_expr += 1
    else:
        raise SyntaxError("semicolon missing at end of structure - "
                          "'{0}'".format(code[prev_expr+1:]))

    struct_name = struct_name.lstrip().rstrip()
    return (prev_expr, next_expr, struct_name)

def parse_expr(code):
    """ Parse a set of declarations and return a list of StructureFields.

    Partitions the declaration into 3 -
    before first sub-structure, first sub-structure, and after first sub-structure.
    Then recursively calls itself to parse the partitioned bits.

    struct ABC { char c; struct XYZ { int b; char y; } myXYZ; int l; } myABC;
                       ^            ^                ^       ^
                       1            2                3       4
        1 - prev_expr
        2 - start_substruct
        3 - end_substruct
        4 - next_expr
    """
    fields_list = []
    code = code.lstrip().rstrip()

    if len(code) == 0:
        return fields_list

    (start_substruct, end_substruct) = find_first_substructure(code)
    # no substructures found
    if start_substruct == -1:
        fields = code.split(';')[:-1]
        # FIXME: handle comma separated fields
        # FIXME: handle unions
        fields_list = [ StructureField.create_from_string(f) for f in fields]
        return fields_list

    (prev_expr, next_expr, struct_name) = get_struct_name(code, start_substruct, end_substruct)

    fields_list.extend(parse_expr(code[:prev_expr + 1]))
    struct_fields = parse_expr(code[start_substruct + 1:end_substruct])
    fields_list.append((struct_name, struct_fields))
    fields_list.extend(parse_expr(code[next_expr:]))

    return fields_list

def parse_c_struct(code):
    """ Parses a C structure declaration to generate a list of fields. """

    # convert to unix style newlines
    code = code.replace('\r', '\n')

    code = remove_comments(code)
    code = remove_keywords(code)
    code = remove_spaces(code)

    return parse_expr(code)
