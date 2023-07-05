import enum


@enum.unique
class UserStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


USER_STATUSES = (
    (UserStatus.ACTIVE.value, "Active"),
    (UserStatus.INACTIVE.value, "Inactive"),
)


@enum.unique
class OperationType(enum.Enum):
    ADDITION = "addition"
    SUBSTRACTION = "subtraction"
    DIVISION = "division"
    SQUARE_ROOT = "square_root"
    RANDOM_STRING = "random_string"


OPERATION_TYPES = (
    (OperationType.ADDITION.value, "Addition"),
    (OperationType.SUBSTRACTION.value, "Subtraction"),
    (OperationType.DIVISION.value, "Division"),
    (OperationType.SQUARE_ROOT.value, "Square root"),
    (OperationType.RANDOM_STRING.value, "Random string"),
)

BASE_USER_BALANCE = 5
