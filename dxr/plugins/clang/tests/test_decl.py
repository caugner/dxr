"""Tests for searches for declarations"""

from dxr.plugins.clang.tests import CSingleFileTestCase


class TypeDeclarationTests(CSingleFileTestCase):
    """Tests for declarations of types"""

    source = r"""
        class MyClass;
        class MyClass
        {
        };
        """

    def test_type(self):
        """Try searching for type declarations."""
        self.found_line_eq(
            'type-decl:MyClass', 'class <b>MyClass</b>;')


class FunctionDeclarationTests(CSingleFileTestCase):
    """Tests for declarations of functions"""

    source = r"""
        void foo();
        void foo()
        {
        };
        """

    def test_function(self):
        """Try searching for function declarations."""
        self.found_line_eq(
            'function-decl:foo', 'void <b>foo</b>();')


class VariableDeclarationTests(CSingleFileTestCase):
    """Tests for declarations of variables"""

    source = r"""
        extern int x;
        int x = 0;
        void foo()
        {
            extern int x;
        }
        """

    def test_variable(self):
        """Try searching for variable declarations."""
        self.found_lines_eq('var-decl:x', [
            ('extern int <b>x</b>;', 2),
            ('extern int <b>x</b>;', 6)])
