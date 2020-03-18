#include <string>

enum class NewStyleEnum : int
{
  Value_1 = 100, // Comment after

  /* Comment before */
  Value_2
};

enum OldStyleEnum
{
  MyValue = -1, /* MyValue */
  MyValue2 = 7, // MyValue2
};