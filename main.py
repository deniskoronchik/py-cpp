from clang_tool import clang_init
from parser import Parser

import sys


if __name__ == '__main__':

  if len(sys.argv) != 2:
    print('Usage: python3 main.py <header file>')
    sys.exit(0)

  clang_init()
  p = Parser(sys.argv[1])
  p.parse(flags=[
          '-I/usr/local/Cellar/llvm/8.0.0_1/include/c++/v1/',
          '-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include'])  # test on OSX

  p.printParsed()
