from unittest.mock import MagicMock as Mock

import pytest

import tgbotcallback
from tgbotcallback.tgbotcallback import DATA_LENGTH_LIMIT


class TestMakeData:

    @pytest.mark.parametrize(
        ("filter_", "expected_result"),
        (
            ("filter", '"filter"'),
            (12345, '12345')
        )
    )
    def test(self, filter_, expected_result):

        assert tgbotcallback.make_data(filter_) == expected_result

    @pytest.mark.parametrize(
        ("filter_", "value", "expected_result"),
        (
            ("filter", "value", '["filter","value"]'),
            ("filter", 12345, '["filter",12345]'),
            ("filter", 123.45, '["filter",123.45]'),
            ("filter", True, '["filter",true]'),
            ("filter", [1, 2, 3], '["filter",[1,2,3]]'),
            (12345, "value", '[12345,"value"]'),
            (12345, 12345, '[12345,12345]'),
            (12345, 123.45, '[12345,123.45]'),
            (12345, True, '[12345,true]'),
            (12345, [1, 2, 3], '[12345,[1,2,3]]')
        )
    )
    def test_with_value(self, filter_, value, expected_result):

        assert tgbotcallback.make_data(filter_, value) == expected_result

    def test_when_resulted_callback_data_is_too_large(self):

        filter_ = "a" * (DATA_LENGTH_LIMIT + 1)
        with pytest.raises(tgbotcallback.exceptions.CallbackDataIsTooLargeError):
            tgbotcallback.make_data(filter_)

    @pytest.mark.parametrize(
        ("parts_args", "expected_args"),
        (
            (("filter",), ("filter",)),
            (("filter", "value"), (["filter", "value"],))
        )
    )
    def test_when_a_third_party_json_serializer_is_used(self, parts_args, expected_args):

        json_serializer_mock = Mock()
        tgbotcallback.make_data(*parts_args, json_serializer=json_serializer_mock)  # noqa

        json_serializer_mock.assert_called_once_with(*expected_args)


class TestParseData:

    @pytest.mark.parametrize(
        ("data", "expected_result"),
        (
            ('"filter"', ("filter", None)),
            ('12345', (12345, None)),
            ('["filter","value"]', ("filter", "value")),
            ('["filter",12345]', ("filter", 12345)),
            ('["filter",123.45]', ("filter", 123.45)),
            ('["filter",true]', ("filter", True)),
            ('["filter",[1,2,3]]', ("filter", [1, 2, 3])),
            ('[12345,"value"]', (12345, "value")),
            ('[12345,12345]', (12345, 12345)),
            ('[12345,123.45]', (12345, 123.45)),
            ('[12345,true]', (12345, True)),
            ('[12345,[1,2,3]]', (12345, [1, 2, 3]))
        )
    )
    def test(self, data, expected_result):

        assert tgbotcallback.parse_data(data) == expected_result

    def test_when_a_third_party_json_deserializer_is_used(self):

        data = "12345"
        json_deserializer_mock = Mock()
        tgbotcallback.parse_data(data, json_deserializer=json_deserializer_mock)  # noqa

        json_deserializer_mock.assert_called_once_with(data)
