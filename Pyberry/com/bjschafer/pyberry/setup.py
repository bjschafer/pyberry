from cx_Freeze import setup, Executable

base = None
buildOptions = dict(includes = ["bdb", "book", "lookup"])

setup(
      name = "Pyberry",
      version = "0.2",
      description = '''Pyberry is open source library management (i.e. books, etc.)
      software, written in (of course) Python 3. It is command line based with no
      GUI planned as of now and is designed to be extremely lightweight and fast.
      It uses sqlite as a database backend and supports looking up books by ISBN.
      Information can be obtained from Amazon and other sources.''',
      options = dict(build_exe = buildOptions),
      executables = [Executable("PyBerry.py", base = base)]
      )
