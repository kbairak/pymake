import tempfile

from pipepy import PipePy, cd, export

from pymake import pymake

from .utils import strip_leading_spaces

pymake_cmd = PipePy('python', m="pymake")


def test_pymake_simple():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    def hello():
                        print("hello")
                """))
            assert str(pymake_cmd.hello) == "hello\n"
            pymake('hello')  # Run it again, for coverage


def test_dependency():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    def func1():
                        print("func1")


                    def func2(func1):
                        print("func2")
                """))
            assert str(pymake_cmd.func2) == "func1\nfunc2\n"
            pymake('func2')  # Run it again, for coverage


def test_dependency_only_called_once():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    def func1():
                        print("func1")

                    def func2(func1):
                        print("func2")

                    def func3(func1, func2):
                        print("func3")
                """))
            assert str(pymake_cmd.func3) == "func1\nfunc2\nfunc3\n"
            pymake('func3')  # Run it again, for coverage


def test_kwarg_from_command_line():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    def hello(msg="world"):
                        print(f"hello {msg}")
                """))

            assert str(pymake_cmd.hello) == "hello world\n"
            pymake('hello')  # Run it again, for coverage

            assert str(pymake_cmd.hello("msg=Bill")) == "hello Bill\n"
            pymake('hello', "msg=Bill")  # Run it again, for coverage


def test_Makefile_attr_from_command_line():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    msg = "world"

                    def hello():
                        print(f"hello {msg}")
                """))

            assert str(pymake_cmd.hello) == "hello world\n"
            pymake('hello')  # Run it again, for coverage

            assert str(pymake_cmd.hello("msg=Bill")) == "hello Bill\n"
            pymake('hello', "msg=Bill")  # Run it again, for coverage


def test_var_from_environment():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    msg = "world"

                    def hello(msg="world"):
                        print(f"hello {msg}")
                """))

            assert str(pymake_cmd('-e').hello) == "hello world\n"
            pymake('-e', 'hello')  # Run it again, for coverage

            with export(msg="Bill"):
                assert str(pymake_cmd.hello) == "hello world\n"
                pymake('hello')  # Run it again, for coverage

                assert str(pymake_cmd('-e').hello) == "hello Bill\n"
                pymake('-e', 'hello')  # Run it again, for coverage

            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    msg = "world"

                    def hello():
                        print(f"hello {msg}")
                """))

            assert str(pymake_cmd('-e').hello) == "hello world\n"
            pymake('-e', 'hello')  # Run it again, for coverage

            with export(msg="Bill"):
                assert str(pymake_cmd.hello) == "hello world\n"
                pymake('hello')  # Run it again, for coverage

                assert str(pymake_cmd('-e').hello) == "hello Bill\n"
                pymake('-e', 'hello')  # Run it again, for coverage


def test_custom_makefile():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('custom_makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    def hello():
                        print("Hello world")
                """))
            assert (str(pymake_cmd("custom_makefile.py", "hello")) ==
                    "Hello world\n")
            pymake("custom_makefile.py", "hello")  # Run it again, for coverage


def test_default_pymake_target():
    with tempfile.TemporaryDirectory() as tmpdir:
        with cd(tmpdir):
            with open('Makefile.py', 'w') as f:
                f.write(strip_leading_spaces("""
                    DEFAULT_PYMAKE_TARGET = "hello"

                    def hello():
                        print("Hello world")
                """))
            assert str(pymake_cmd) == "Hello world\n"
            pymake()  # Run it again, for coverage
