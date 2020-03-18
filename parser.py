import typing
import parsed
import clang.cindex as ci

import re


class Parser:

  def __init__(self, file_path):
    self.file_path = file_path
    self.classes = []
    self.enums = []

  def parse(self, flags: [str] = [], is_debug: bool = True):

    args = ['-std=c++17', '-fparse-all-comments']
    args.extend(flags)
    try:
      tu = ci.TranslationUnit.from_source(
          self.file_path,
          args=args,
          options=ci.TranslationUnit.PARSE_SKIP_FUNCTION_BODIES  # |
          # 0x400  # CXTranslationUnit_SingleFileParse
          # https://clang.llvm.org/doxygen/group__CINDEX__TRANSLATION__UNIT.html#ggab1e4965c1ebe8e41d71e90203a723fe9a96401c77684f532f62e848e78c965886
      )
    except ci.TranslationUnitLoadError:
      if is_debug:
        print("Can't open source file: {}".format(self.file_path))

      return False

    print(dir(ci.CursorKind))
    print(dir(ci.Cursor))

    for cursor in tu.cursor.get_children():
      # skip everything from included files
      if str(cursor.location.file) != self.file_path:
        continue

      if cursor.kind == ci.CursorKind.CLASS_DECL:
        self.classes.append(self.parseClass(cursor))
      elif cursor.kind == ci.CursorKind.ENUM_DECL:
        self.enums.append(self.parseEnum(cursor))

    if is_debug and len(tu.diagnostics) > 0:
      print('\n', '-' * 10, '\nParse errors:')
      for msg in tu.diagnostics:
        print(msg)

    return tu is not None

  def trimComment(self, value: str):
    result = value
    # TODO: support multiline comments
    regex = re.compile(
        r"(\/\/(?P<value_s>.*)$)|(/\*(?P<value_m>[\s\S]*?)\*/\s*)")
    matches = regex.finditer(value)
    for _, match in enumerate(matches):
      s = match.group('value_s')
      m = match.group('value_m')
      result = m if m is not None else s

    return result.strip()  # .replace('*', '')

  def convertAccess(self, modif: ci.AccessSpecifier) -> parsed.AccessSpecifier:
    if modif == ci.AccessSpecifier.PUBLIC:
      return parsed.AccessSpecifier.PUBLIC
    elif modif == ci.AccessSpecifier.PROTECTED:
      return parsed.AccessSpecifier.PROTECTED

    return parsed.AccessSpecifier.PRIVATE

  def parseMethod(self, cursor: ci.Cursor) -> parsed.ClassMethod:
    params = []

    for child in cursor.get_children():
      if child.kind == ci.CursorKind.PARM_DECL:

        params.append(parsed.ClassMethod.Parameter(
            name=child.spelling,
            _type=child.type.get_canonical().spelling))

    return parsed.ClassMethod(
        name=cursor.spelling,
        decl_file=self.file_path,
        params=params,
        ret=cursor.result_type.get_canonical().spelling,
        comment=self.trimComment(
            cursor.raw_comment) if cursor.raw_comment is not None else None,
        amodif=self.convertAccess(cursor.access_specifier))

  def parseClass(self, cursor: ci.Cursor) -> parsed.Klass:
    methods = []
    for child in cursor.get_children():
      if child.kind == ci.CursorKind.CXX_METHOD:
        methods.append(self.parseMethod(child))

    return parsed.Klass(name=cursor.spelling, decl_file=self.file_path, methods=methods)

  def parseEnum(self, cursor: ci.Cursor) -> parsed.Enum:
    items = []
    for child in cursor.get_children():
      if child.kind == ci.CursorKind.ENUM_CONSTANT_DECL:
        it = parsed.Enum.Field(
            child.spelling, child.enum_value, self.trimComment(child.raw_comment))
        items.append(it)

    return parsed.Enum(name=cursor.spelling,
                       decl_file=self.file_path, items=items)

  def printParsed(self):
    print('=' * 10)
    print('Enums: ')
    for e in self.enums:
      print(str(e))

    print('-' * 10)
    print('Classes: ')
    for c in self.classes:
      print(str(c))
