from latex2sympy.latex2sympy import LatexToSympy
from latex2sympy.lib import LATEXLexerToken
from latex2sympy.utils.json import has_type_or_token
from latex2sympy.units import find_unit, find_prefix, is_unit


def process_sympy_as_unit(latex: str, variable_values: dict = {}):
    instance = LatexToSympyAsUnit(latex, variable_values)
    return instance.process_sympy()


class LatexToSympyAsUnit(LatexToSympy):
    def __init__(self, latex: str, variable_values: dict = {}):
        super().__init__(latex, variable_values)

    def process_sympy(self):
        return_data = super().process_sympy()
        if not is_unit(return_data):
            raise Exception('Unrecognized unit')
        return return_data

    def convert_postfix_list(self, arr, i=0):
        if i >= len(arr):  # pragma: no cover
            raise Exception('Index out of bounds')

        # only run the merge logic once
        if i > 0:
            return super().convert_postfix_list(arr, i)

        # loop through list and merge adjacent atoms into a single LETTER atom_expr
        new_list_items = []
        new_atom_text = None
        for list_item in arr:
            atom = list_item.get('exp', {}).get('comp', {}).get('atom', {})
            atom_target = atom.get('atom_expr', {}) if 'atom_expr' in atom else atom
            if atom_target is not None and (has_type_or_token(atom_target, LATEXLexerToken.LETTER) or
                                            has_type_or_token(atom_target, LATEXLexerToken.GREEK_CMD) or
                                            has_type_or_token(atom_target, LATEXLexerToken.UNIT_SYMBOL)):
                atom_text = atom_target.get('text')

                # UNIT_SYMBOL contains a period to allow parsing chars after the period, but will be blocked here
                if atom_text == '.':
                    raise Exception('"." is an invalid symbol')

                # a space means multiplication, so add the new list item with all text before the space, if any
                if atom_text == '\\: ':
                    if new_atom_text is not None:
                        new_list_items.append(create_new_list_item(new_atom_text))
                    new_atom_text = None
                    continue

                # begin tracking text for a new list item or append text to the existing string
                if new_atom_text is None:
                    new_atom_text = atom_text
                else:
                    new_atom_text += atom_text

                # if this atom has a sub or sup, complete the list item and include the sub and sup
                if 'subexpr' in atom_target or 'supexpr' in atom_target:
                    new_list_items.append(create_new_list_item(new_atom_text, atom_target))
                    new_atom_text = None
                    continue
            else:
                # this `list_item` is NOT able to merge
                # add a new list item with the previously tracked text, if any
                if new_atom_text is not None:
                    new_list_items.append(create_new_list_item(new_atom_text))
                    new_atom_text = None
                # preserve the current item as-is
                new_list_items.append(list_item)

        # add a new list item with the previously tracked text, if any
        if new_atom_text is not None:
            new_list_items.append(create_new_list_item(new_atom_text))

        return super().convert_postfix_list(new_list_items, i)

    def get_atom_symbol_for_atom_expr(self, atom_name, type):
        # do not call parent class
        search_name = '\\' + atom_name if type == LATEXLexerToken.GREEK_CMD else atom_name
        unit = find_unit(search_name)
        if unit is not None:
            return unit
        prefix = find_prefix(search_name)
        if prefix is not None:
            return prefix
        raise Exception('Unrecognized unit')


def create_new_list_item(text, atom_expr=None):
    new_atom_expr = {'text': text, 'type': LATEXLexerToken.LETTER}
    if atom_expr is not None and 'subexpr' in atom_expr:
        new_atom_expr['subexpr'] = atom_expr.get('subexpr')
    if atom_expr is not None and 'supexpr' in atom_expr:
        new_atom_expr['supexpr'] = atom_expr.get('supexpr')
    return {'exp': {'comp': {'atom': {'atom_expr': new_atom_expr}}}}
