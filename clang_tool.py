import os

import clang.cindex

search_directories = [
    '/usr/lib/llvm-7/lib',
    '/usr/lib/llvm-6.0/lib',
    '/usr/local/Cellar/llvm/8.0.0_1/lib',  # OSX - brew
]


def clang_find():
  clang_dir = None
  for d in search_directories:
    if os.path.isdir(d) and os.path.exists(d):
      clang_dir = d
      break

  return clang_dir


def clang_init():
  cl = clang_find()
  if cl:
    print('Found clang: {}'.format(cl))
  else:
    print("Can't find clang")

  clang.cindex.Config.set_library_path(clang_find())
