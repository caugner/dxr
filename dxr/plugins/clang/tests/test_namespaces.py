"""Tests for searches about namespaces"""

from dxr.plugins.clang.tests import CSingleFileTestCase


class NamespaceDefTests(CSingleFileTestCase):
    """Tests for finding definitions of namespaces"""

    source = r"""
        namespace Outer {
        }
        namespace Outer {
            namespace Inner {
            }
        }
        """

    def test_namespace_definitions(self):
        self.found_lines_eq('+namespace:Outer', [
            ('namespace <b>Outer</b> {', 2),
            ('namespace <b>Outer</b> {', 4)])
        self.found_line_eq('+namespace:Outer::Inner', 'namespace <b>Inner</b> {')


class NamespaceExprRefTests(CSingleFileTestCase):
    """Tests for finding references to namespaces in expressions"""

    source = r"""
        namespace Outer {
            void foo() {}
            int baz = 0;
        }
        namespace Outer {
            namespace Inner {
                void bar() {}
            }
        }
        void quux() {
            Outer::foo();
            Outer::baz = 1;
            Outer::Inner::bar();
        }
        """

    def test_namespace_expression_references(self):
        self.found_lines_eq('+namespace-ref:Outer', [
            ('<b>Outer</b>::foo();', 12),
            ('<b>Outer</b>::baz = 1;', 13),
            ('<b>Outer</b>::Inner::bar();', 14)])
        self.found_line_eq('+namespace-ref:Outer::Inner', 'Outer::<b>Inner</b>::bar();')


class NamespaceDeclRefTests(CSingleFileTestCase):
    """Tests for finding references to namespaces in declarations"""

    source = r"""
        namespace Outer {
            class MyClass {};
        }
        namespace Outer {
            namespace Inner {
                class MyClass {};
            }
        }
        void quux() {
            Outer::MyClass *x;
            Outer::Inner::MyClass *y;
        }
        """

    def test_namespace_declaration_references(self):
        self.found_lines_eq('+namespace-ref:Outer', [
            ('<b>Outer</b>::MyClass *x;', 11),
            ('<b>Outer</b>::Inner::MyClass *y;', 12)])
        self.found_line_eq('+namespace-ref:Outer::Inner', 'Outer::<b>Inner</b>::MyClass *y;')


class NamespaceUsingDirectiveTests(CSingleFileTestCase):
    """Tests for the 'using' directive"""

    source = r"""
        namespace Outer {
            namespace Inner {
            }
        }
        using namespace Outer;
        using namespace Outer::Inner;
        """

    def test_namespace_using_directive_references(self):
        self.found_lines_eq('+namespace-ref:Outer', [
            ('using namespace <b>Outer</b>;', 6),
            ('using namespace <b>Outer</b>::Inner;', 7)])
        self.found_line_eq('+namespace-ref:Outer::Inner', 'using namespace Outer::<b>Inner</b>;')


class NamespaceUsingDeclarationTests(CSingleFileTestCase):
    """Tests for the 'using' declaration"""

    source = r"""
        namespace Outer {
            void foo(int) {}
            void foo(double) {}
        }
        namespace Outer {
            namespace Inner
            {
                void bar() {}
            }
        }
        void quux() {
            using Outer::foo;
            using Outer::Inner::bar;
        }
        """

    def test_namespace_using_declaration_references(self):
        self.found_lines_eq('+namespace-ref:Outer', [
            ('using <b>Outer</b>::foo;', 13),
            ('using <b>Outer</b>::Inner::bar;', 14)])
        self.found_line_eq('+namespace-ref:Outer::Inner', 'using Outer::<b>Inner</b>::bar;')


class NamespaceAliasTests(CSingleFileTestCase):
    """Tests for namespace aliases"""

    source = r"""
        namespace Outer {
            void foo() {}
        }
        void quux() {
            namespace OuterAlias = Outer;
            OuterAlias::foo();
        }
        """

    def test_namespace_alias_definitions(self):
        """Try searching for namespace alias definitions."""
        self.found_line_eq(
            '+namespace-alias:quux()::OuterAlias',
            'namespace <b>OuterAlias</b> = Outer;')

    def test_namespace_alias_references(self):
        """Try searching for namespace alias references."""
        self.found_line_eq(
            '+namespace-alias-ref:quux()::OuterAlias',
            '<b>OuterAlias</b>::foo();')
