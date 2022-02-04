import readline
import sys
from run import run

VERSION = "0.0.3"

args = sys.argv
args.pop(0)

try:
    from_file = False
    
    if len(args) > 0:
        fn = args[0]
        f = open(fn, "r")
        file = f.read()
        from_file = True
    else:
        fn = "<stdin>"
        print(f"CorLang v{VERSION}")
    
    while True:
        if from_file:
            text = file
        else:
            text = input("> ")

        if text.strip() == "":
            continue
            
        result, error = run(fn, text)
    
        if error:
            print(error.to_string())
            if from_file:
                break
        elif result and not from_file:
            if len(result.values) == 1:
                print(repr(result.values[0]))
            else:
                print(repr(result))

        if from_file:
            break
except (EOFError, KeyboardInterrupt):
    pass
except FileNotFoundError:
    print(f"Can't find file '{args[0]}'")