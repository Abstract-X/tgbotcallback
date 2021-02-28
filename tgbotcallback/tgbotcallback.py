import json as jsonlib
from typing import Union, Tuple, Callable, List

from . import exceptions


FilterType = Union[str, int]
ValueType = Union[str, int, float, bool, list, None]
NonSerializedDataType = Union[FilterType, List[Union[FilterType, ValueType]]]

DATA_LENGTH_LIMIT = 64  # taken from https://core.telegram.org/bots/api#inlinekeyboardbutton


def _serialize_data(data: NonSerializedDataType) -> str:
    """
    Serialize data to string.

    Provides compactness of the string due to the absence of spaces.

    :param data: callback data parts.
    :return: serialized data string.
    """

    return jsonlib.dumps(data, separators=(",", ":"))


def _deserialize_data(data: str) -> NonSerializedDataType:
    """
    Deserialize string to data.

    :param data: serialized data string.
    :return: callback data parts.
    """

    return jsonlib.loads(data)


def make_data(filter_: FilterType, value: ValueType = None, *,
              json_serializer: Callable[[NonSerializedDataType], str] = _serialize_data) -> str:
    """
    Make a string for callback_data field in InlineKeyboardButton.

    :param filter_: value to filter the callback.
    :param value: value for inline button.
    :param json_serializer: function for JSON serialization.
    :raises CallbackDataIsTooLargeError: if the data has exceeded the allowed size limit.
    :return: callback_data string.
    """

    data = json_serializer([filter_, value] if value is not None else filter_)

    data_length = len(data.encode())
    if data_length > DATA_LENGTH_LIMIT:
        raise exceptions.CallbackDataIsTooLargeError(data, data_length, DATA_LENGTH_LIMIT)

    return data


def parse_data(data: str, *,
               json_deserializer: Callable[[str], NonSerializedDataType] =
               _deserialize_data) -> Tuple[FilterType, ValueType]:
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
