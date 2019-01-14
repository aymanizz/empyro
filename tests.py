# This is a helper script for discovering the modules inside the package and
# running the doctests.
# usage: python3 tests.py [-r] -- option -r reports the modules found
# any other doctest module options can be passed such as -f and -v
# any modules outside the package folder are not considered for testing.

import sys
import doctest
import importlib
from pathlib import Path

if __name__ == '__main__':
    # discover all python files inside the package and run the doc tests
    report = any([arg == '-r' for arg in sys.argv])
    modules = []
    package = Path('.') / 'empyro'
    print('DISCOVERING MODULES...')
    for module_path in package.glob('**/*.py'):
        module_parent = '.'.join(module_path.parts[:-1])
        module_name = module_parent + '.' + module_path.stem
        modules.append(importlib.import_module(module_name))
    if report:
        print('\n== {} MODULES FOUND =='
              .format(len(modules)))
        for module in modules:
            print('  -- {}'.format(module.__name__))
        print('\n')
    print('TESTING MODULES...')
    for module in modules:
        doctest.testmod(module, exclude_empty=True)
    print('DONE')
