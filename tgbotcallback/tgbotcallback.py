import json as jsonlib
from typing import Union, Tuple

from . import exceptions


FilterType = Union[str, int]
ValueType = Union[str, int, float, bool, list, None]

DATA_LENGTH_LIMIT = 64  # taken from https://core.telegram.org/bots/api#inlinekeyboardbutton


def make_data(filter_: FilterType, value: ValueType = None) -> str:
    """
    Make a string for callback_data field in InlineKeyboardButton.

    :param filter_: value to filter the callback.
    :param value: value for inline button.
    :raises CallbackDataIsTooLargeError: if the data has exceeded the allowed size limit.
    :return: callback_data string.
    """

    data = [filter_, value] if value is not None else filter_
    data = jsonlib.dumps(data, separators=(",", ":"))

    data_length = len(data.encode())
    if data_length > DATA_LENGTH_LIMIT:
        raise exceptions.CallbackDataIsTooLargeError(data, data_length, DATA_LENGTH_LIMIT)

    return data


def parse_data(data: str) -> Tuple[FilterType, ValueType]:
    """
    Parse data to get filter value and button value.

    :param data: callback_data string.
    :return: value to filter the callback and inline button value.
    """

    data = jsonlib.loads(data)

    if isinstance(data, list):
        filter_, value = data
    else:
        filter_, value = data, None

    return filter_, value
