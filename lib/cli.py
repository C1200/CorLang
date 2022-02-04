#!/usr/bin/env python

import readline
import sys
from run import run

VERSION = "0.0.2"

args = sys.argv
args.pop(0)

try:
    running = True
    
    if len(args) > 0:
        fn = args[0]
        f = open(fn, "r")
        file = f.readlines()
        line = 0
    else:
        fn = "<stdin>"
        print(f"CorLang v{VERSION}")
    
    while running:
        if len(args) > 0:
            text = file[line]
            line += 1
            if not (line < len(file)):
                running = False
        else:
            text = input("> ")

        if text.strip() == "":
            continue
            
        result, error = run(fn, text)
    
        if error:
            print(error.to_string())
            if len(args) > 0:
                exit(1)
        elif result and len(args) == 0:
            print(repr(result))
except (EOFError, KeyboardInterrupt):
    exit(0)
except FileNotFoundError:
    print(f"Can't find file '{args[0]}'")