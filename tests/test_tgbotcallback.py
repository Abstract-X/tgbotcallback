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

    @pytest.mark.parametrize(
        ("filter_",),
        (
            ("a" * (DATA_LENGTH_LIMIT + 1),),
        )
    )
    def test_when_resulted_callback_data_is_too_large(self, filter_):

        with pytest.raises(tgbotcallback.exceptions.CallbackDataIsTooLargeError):
            tgbotcallback.make_data(filter_)


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
