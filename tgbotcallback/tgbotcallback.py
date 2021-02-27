import json as jsonlib
from typing import Union, Tuple, Callable

from . import exceptions


FilterType = Union[str, int]
ValueType = Union[str, int, float, bool, list, None]

DATA_LENGTH_LIMIT = 64  # taken from https://core.telegram.org/bots/api#inlinekeyboardbutton


def make_data(filter_: FilterType, value: ValueType = None, *,
              json_serializer: Callable = jsonlib.dumps) -> str:
    """
    Make a string for callback_data field in InlineKeyboardButton.

    :param filter_: value to filter the callback.
    :param value: value for inline button.
    :param json_serializer: function for JSON serialization.
    :raises CallbackDataIsTooLargeError: if the data has exceeded the allowed size limit.
    :return: callback_data string.
    """

    data = [filter_, value] if value is not None else filter_
    try:
        data = json_serializer(data, separators=(",", ":"))
    except TypeError as exception:  # if there is no separators kwarg in the serializer
        if exception.args[0] == "'separators' is an invalid keyword argument for this function":
            data = json_serializer(data)
        else:
            raise

    data_length = len(data.encode())
    if data_length > DATA_LENGTH_LIMIT:
        raise exceptions.CallbackDataIsTooLargeError(data, data_length, DATA_LENGTH_LIMIT)

    return data


def parse_data(data: str, *, json_deserializer: Callable = jsonlib.loads) -> Tuple[FilterType, ValueType]:
    """
    Parse data to get filter value and button value.

    :param data: callback_data string.
    :param json_deserializer: function for JSON deserialization.
    :return: value to filter the callback and inline button value.
    """

    data = json_deserializer(data)

    if isinstance(data, list):
        filter_, value = data
    else:
        filter_, value = data, None

    return filter_, value
