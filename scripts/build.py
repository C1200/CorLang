import PyInstaller.__main__ as PyInstaller
import sys

PyInstaller.run([
    "lib/cli.py",
    "-F",
    f"-n=corlang-{sys.platform}",
    "--add-data=lib/std:std"
])