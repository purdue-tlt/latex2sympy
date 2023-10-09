import os.path
import pickle

# export UNIT_ALIASES
# -------------------
# load UNIT_ALIASES from a pickled file, if the file exists
# or import from code

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
pickle_file_path = f'{ROOT_DIR}/unit_aliases.pkl'
pickle_file_exists = os.path.isfile(pickle_file_path)
if pickle_file_exists:
    pickle_file = open(pickle_file_path, 'rb')
    UNIT_ALIASES = pickle.load(pickle_file)
    pickle_file.close()
else:  # pragma: no cover
    from latex2sympy.units.unit_aliases.unit_aliases import UNIT_ALIASES
