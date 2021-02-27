# TGBotCallback

The library provides the ability to correctly processing callback data for [InlineKeyboardButton](https://core.telegram.org/bots/api#inlinekeyboardbutton).

## Installation
To install the latest version of **tgbotcallback**, use:
``` bash
pip install --upgrade tgbotcallback
```
Refer to [Installing Packages](https://packaging.python.org/tutorials/installing-packages/) guide for more information.

## Problem
Usually for process callback data used this method:
``` python
>>> callback_data = f"{filter_part}_{value_part}"  # creating data string
>>> filter_part, value_part = callback_data.split("_")  # parsing parts
```
This solution is unreliable because if a separator-character is encountered in any of your parts, the data will not be correctly parsed:
``` python
>>> filter_part = "some_filter_string"
>>> value_part = "value_string"
>>> callback_data = f"{filter_part}_{value_part}"  # 'some_filter_string_value_string'
>>> filter_part, value_part = callback_data.split("_")
# ValueError: too many values to unpack (expected 2)
```

## Solution
``` python
>>> import tgbotcallback
>>>
>>> callback_data = tgbotcallback.make_data("some_filter_string", "value_string")
>>> callback_data
'["some_filter_string","value_string"]'
>>>
>>> filter_part, value_part = tgbotcallback.parse_data(callback_data)
>>> filter_part
'some_filter_string'
>>> value_part
'value_string'
```

## Tips
- Filter part can be used in your event engines to handle calls from specific buttons.
  Value part of the button can be used to store any information that is associated with the button.
- You can use strings or integers as a filter.
  As the value of the button, you can use strings, integers, float numbers, bools, as well as lists with all of the above.
