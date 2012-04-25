import os

import sublime_plugin


#==============================================================================
# Helpers
#==============================================================================
def get_tests_path(filename):
    """
    >>> get_tests_path('/Users/t0ster/Desktop/whatever/whatever/views/users.py')
    ('/Users/t0ster/Desktop/whatever/tests', 'whatever/views/users.py')
    """
    testspath = None
    file_relpath = None
    path = filename.split(os.sep)

    while not testspath and path:
        _testspath = os.path.join(os.sep, *(path + ['tests']))
        if os.path.exists(_testspath):
            testspath = _testspath
        path.pop()

    if testspath:
        file_relpath = os.path.relpath(filename, os.path.dirname(testspath))

    return testspath, file_relpath


def relpath2module(relpath):
    """
    >>> relpath2module('whatever/views/users.py')
    ['whatever', 'views', 'users']
    """
    module = os.path.splitext(relpath)[0].split(os.sep)
    return module


def create_file(path):
    """
    >>> create_file('/Users/t0ster/Desktop/whatever/wtf/tfw')
    >>> os.path.exists('/Users/t0ster/Desktop/whatever/wtf/tfw')
    True
    """
    if not os.path.exists(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        open(path, 'w').close()


def create_module(path, module):
    """
    >>> create_module('/Users/t0ster/Desktop/whatever/tests', ['views', 'blah', 'blah'])
    >>> os.path.exists('/Users/t0ster/Desktop/whatever/tests/views/blah/blah.py')
    True
    >>> os.path.exists('/Users/t0ster/Desktop/whatever/tests/views/blah/__init__.py')
    True
    """
    for i in range(1, len(module)):
        create_file(os.path.join(path, *(module[:i] + ['__init__.py'])))
    module_file = os.path.join(path, *(module[:-1] + ["%s.py" % module[-1]]))
    create_file(module_file)
    return module_file
#------------------------------------------------------------------------------


class TestCommand(object):
    def get_module(self, relpath):
        module = relpath2module(relpath)
        module = module[1:]
        module[-1] = "test_%s" % module[-1]
        return module

    def run(self, edit):
        testspath, relpath = get_tests_path(self.view.file_name())

        if testspath:
            module = self.get_module(relpath)

            module_file = create_module(testspath, module)
            self.view.window().open_file(module_file)


class CreateUnitTestFileCommand(TestCommand, sublime_plugin.TextCommand):
    def get_module(self, relpath):
        module = super(CreateUnitTestFileCommand, self).get_module(relpath)
        module.insert(0, 'unittests')
        return module


class CreateFunctionalTestFileCommand(TestCommand, sublime_plugin.TextCommand):
    def get_module(self, relpath):
        module = super(CreateFunctionalTestFileCommand, self).get_module(relpath)
        module.insert(0, 'functionaltests')
        return module
