import typing
import enum


class Base:

  def __init__(self, name: str, decl_file: str):
    self.name = name
    self.decl_file = decl_file


class Enum(Base):

  class Field:

    def __init__(self, name: str, value, comment: str):
      self.name = name
      self.value = value
      self.comment = comment

    def __str__(self):
      return '{}: {} // {}'.format(self.name, self.value, self.comment)

  def __init__(self, items: [Field], **kwargs):
    Base.__init__(self, **kwargs)
    self.items = items

  def __str__(self):
    result = 'enum {} {{'.format(self.name)
    for i in self.items:
      result += '\n  {}'.format(str(i))
    result += '\n}'

    return result


class AccessSpecifier(enum.Enum):
  PUBLIC = 1
  PROTECTED = 2
  PRIVATE = 3


class ClassMethod(Base):

  class Parameter:

    def __init__(self, name: str, _type: str):
      self.name = name
      self.type = _type

    def __str__(self):
      return '{} {}'.format(self.type, self.name)

  def __init__(self, params: [Parameter], ret: str, amodif: AccessSpecifier, comment: str, ** kwargs):
    Base.__init__(self, **kwargs)

    self.params = params
    self.ret = ret
    self.amodif = amodif
    self.comment = comment

  def __str__(self):
    params = ''
    index = 0
    for p in self.params:
      if index > 0:
        params += ','
      params += str(p)
      index += 1

    modif = 'public'
    if self.amodif == AccessSpecifier.PROTECTED:
      modif = 'protected'
    elif self.amodif == AccessSpecifier.PRIVATE:
      modif = 'private'

    doc = ''
    if self.comment:
      doc = '/* {} */\n'.format(self.comment if self.comment else '')

    return '\n{}{} {}({}) --- {}'.format(
        doc,
        self.ret,
        self.name,
        params,
        modif)


class Klass(Base):

  def __init__(self, methods: [ClassMethod], **kwargs):
    Base.__init__(self, **kwargs)

    self.methods = methods

  def __str__(self):
    methods = ''
    for f in self.methods:
      methods += '\n  {}'.format(str(f))

    return '{} {{ {} \n}}'.format(self.name, methods)
