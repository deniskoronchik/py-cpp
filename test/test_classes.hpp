#include <string>

using MyString = std::string;

class MyClass
{
public:
  // Comment
  void NoReturnPublicMethod();

  /* Multiline comment 
   * @param name New name value
   */
  void SetNameCRef(const MyString &name);
  void SetNamePtr(MyString *name);
  void SetName(MyString name);
  const std::string &GetName() const;

  MyString GetOtherString() const;

  void SetID(int32_t newId);
  uint32_t GetID() const;

  void SetInt(int value);

protected:
  void _internalUpdate();

private:
  int PrivateGetter() const;
};