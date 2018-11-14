from enum import Enum, EnumMeta, _EnumDict, IntEnum


class UniqueEnum(Enum):
    def __init__(self):
        super(UniqueEnum, self).__init__()
        cls = self.__class__
        if any(self.value == dup.value for dup in cls):
            dup = cls(self.value)
            raise ValueError('No duplicate values allowed in %s: %r and %r' % (self.__class__.__name__, self, dup))


class AutoNumberEnumMeta(EnumMeta):
    _i = 0

    def __new__(metacls, cls, bases, classdict):
        if type(classdict) is dict:
            original_dict = classdict
            classdict = _EnumDict()
            for k, v in original_dict.items():
                classdict[k] = v
        temp = _EnumDict()
        for k, v in classdict.items():
            if k in classdict._member_names:
                if v == ():
                    v = metacls._i
                else:
                    metacls._i = v
                metacls._i += 1
                temp[k] = v
            else:
                temp[k] = classdict[k]
        return EnumMeta.__new__(metacls, cls, bases, temp)


class AutoNumberEnum(IntEnum, UniqueEnum, metaclass=AutoNumberEnumMeta):
    __metaclass__ = AutoNumberEnumMeta


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class SortedEnumMeta(EnumMeta):
    def __iter__(cls):
        it = EnumMeta.__iter__(cls)
        return iter(sorted(it))


class SortedEnum(OrderedEnum, metaclass=SortedEnumMeta):
    __metaclass__ = SortedEnumMeta


def typed(_type):
    def wrapper(enumeration):
        if any(not isinstance(member.value, _type) for member in enumeration):
            raise TypeError('All enum values must be of type %r' % _type)
        return enumeration

    return wrapper
