import sympy
import sympy.physics.units as sympy_physics_units
from latex2sympy.latex2sympy import LatexToSympy
from latex2sympy.lib import LATEXLexerToken
from latex2sympy.utils.json import has_type_or_token
from latex2sympy.units import UNIT_ALIASES, PREFIX_ALIASES, find_unit, find_prefix, is_unit


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

    def convert_letters_to_postfix_list_items(self, atom_text):
        # do not call parent class
        new_list_items = []
        if '\\: ' in atom_text:
            atom_text_split = atom_text.split('\\: ')
            for t in atom_text_split:
                if t == '.':
                    raise Exception('"." is an invalid symbol')
                if len(t) > 0:
                    new_list_items.append({'exp': {'comp': {'atom': {'atom_expr': {'text': t, 'type': LATEXLexerToken.LETTER.value}}}}})
        return new_list_items

    def convert_atom(self, atom):
        if has_type_or_token(atom, LATEXLexerToken.LETTERS):
            atom_text = atom.get('text')
            unit = find_unit(atom_text)
            if unit is not None:
                return unit
            # prefixes can be combined in `convert_postfix_list`
            prefix = find_prefix(atom_text)
            if prefix is not None:
                return prefix
            raise Exception('Unrecognized unit')

        # fallback to parent class
        return super().convert_atom(atom)

    def get_atom_symbol_for_atom_expr(self, atom_name, type):
        # do not call parent class
        search_name = '\\' + atom_name if type == LATEXLexerToken.GREEK_CMD else atom_name
        unit = find_unit(search_name)
        if unit is not None:
            return unit
        # prefixes can be combined in `convert_postfix_list`
        prefix = find_prefix(search_name)
        if prefix is not None:
            return prefix
        raise Exception('Unrecognized unit')

    def handle_mul_flat(self, lh, rh, lh_atom=None):
        # check if an adjacent items should be combined into a prefixed unit
        # this happens with a prefix or unit that uses a greek letter latex command
        # .e.g. "\mu H" or "k\Omega "
        lh_is_prefix = isinstance(lh, sympy_physics_units.prefixes.Prefix)
        lh_is_quantity = isinstance(lh, sympy_physics_units.Quantity)
        rh_is_quantity = isinstance(rh, sympy_physics_units.Quantity)
        # prefix without a quantity after it is invalid
        if lh_is_prefix and not rh_is_quantity:
            raise Exception('Only a prefix and a quantity can be combined')
        prefix_text = None
        if lh_is_prefix:
            prefix_text = str(lh.name)
        # handle the edge case where a unit’s abbrev is the same as a prefix
        # e.g. "M\Omega ", where "M" is parsed as "molar", but should become "megaohm"
        # `is_postfix_list` excludes the case of explicit multiplication e.g. "molar*ohm"
        elif lh_is_quantity and lh_atom is not None and lh_atom.get('atom_expr', {}).get('text') in PREFIX_ALIASES:
            prefix_text = str(PREFIX_ALIASES[lh_atom.get('atom_expr').get('text')].name)
        if prefix_text is not None and rh_is_quantity:
            unit_name = prefix_text + str(rh.name)
            # check if the combined prefix name + unit name are valid
            if unit_name in UNIT_ALIASES:
                return UNIT_ALIASES[unit_name]
            else:
                raise Exception('Unrecognized unit')

        # fallback to parent class
        return super().handle_mul_flat(lh, rh, lh_atom)
