# This is a helper script for discovering the modules inside the package and
# running the doctests.
# usage: python3 tests.py [-r] [-a] [-e=filename]
#   -- option -r reports the modules found
#   -- option -a to include all python files, including those in subpackages
#   -- option -e tp exclude a file
# any other doctest module options can be passed such as -f and -v
# any modules outside the package folder are not considered for testing.

import sys
import doctest
import importlib
from pathlib import Path

if __name__ == '__main__':
    # discover all python files inside the package and run the doc tests
    # refactor to use argparse if got big
    excluded, report, search_in_all = [], False, False
    for arg in sys.argv:
        if arg.startswith('-e'):
            excluded.append(arg.split('=', maxsplit=1))
        elif arg == '-r':
            report = True
        elif arg == '-a':
            search_in_all = True

    modules = []
    package = Path('.') / 'empyro'

    print('DISCOVERING MODULES...')

    glob_pattern = '**/*.py' if search_in_all else '*.py'

    for module_path in package.glob(glob_pattern):
        print(module_path)
        if module_path.stem in excluded:
            continue
        module_parent = '.'.join(module_path.parts[:-1])
        module_name = module_parent + '.' + module_path.stem
        modules.append(importlib.import_module(module_name))

    if report:
        print('\n== {} MODULES FOUND =='
              .format(len(modules)))
        for module in modules:
            print('  - {}'.format(module.__name__))
        print('\n')

    print('TESTING MODULES...')

    for module in modules:
        doctest.testmod(module, exclude_empty=True)

    print('DONE')
