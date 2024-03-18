


class model1:
    __field1: int
    __field2: str
    _field3: None

    def __init__(self, field1: int, field2: str, field3: None):
      self.__field1: int = field1
      self.__field2: str = field2
      self._field3: None = field3


    @property
    def field1(self) -> int:
        return self.__field1

    @field1.setter
    def field1(self, value : int) -> None:
        self.__field1 = value

    @property
    def field2(self) -> str:
        return self.__field2