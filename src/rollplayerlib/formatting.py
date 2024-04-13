import re

from enums import ThresholdType, FormatType, FormatEnum
from exceptions import RollException


class Threshold:
    def __init__(self, limit: int, threshold_type: ThresholdType):
        self.limit = limit
        self.threshold_type = threshold_type

    def passing(self, numbers: list[int]) -> list[bool]:
        if self.threshold_type == ThresholdType.GREATER:
            return [num >= self.limit for num in numbers]
        elif self.threshold_type == ThresholdType.LESS:
            return [num <= self.limit for num in numbers]
        elif self.threshold_type == ThresholdType.MAX:
            max_value = max(numbers)
            return [num == max_value for num in numbers]
        elif self.threshold_type == ThresholdType.MIN:
            min_value = min(numbers)
            return [num == min_value for num in numbers]
        else:
            raise RollException("Invalid threshold type (how did you get here?)")


class Format:
    def __init__(self, format_type: FormatType, format_args=None, threshold: Threshold = None):
        self.format_type = format_type
        self.format_args = format_args
        self.threshold = threshold

    @classmethod
    def parse(cls, expression):
        formatting = Format(FormatType.FORMAT_DEFAULT, 20, None)
        format_regex = r'(' + '|'.join(re.escape(op.value) for op in FormatEnum) + r')'
        strip, *formats = re.split(format_regex, expression)
        idx = 0
        while idx < len(formats):
            format_char = formats[idx]
            if idx == len(formats) - 1:
                arg = False
            else:
                arg = formats[idx + 1]
                if re.match(format_regex, arg):
                    arg = False
            if arg == "":
                arg = False
            match format_char:
                case FormatEnum.LIST:
                    if arg:
                        formatting.format_type = FormatType.FORMAT_LIST_SPLIT
                        try:
                            formatting.format_args = int(arg)
                        except ValueError:
                            raise RollException("Attempted to split with non-integer")
                    else:
                        formatting.format_type = FormatType.FORMAT_LIST
                case FormatEnum.SUM:
                    formatting.format_type = FormatType.FORMAT_SUM
                case FormatEnum.GREATER:
                    if arg:
                        try:
                            formatting.threshold = Threshold(int(arg), ThresholdType.GREATER)
                        except ValueError:
                            raise RollException("Attempted to use > with non-integer")
                    else:
                        formatting.threshold = Threshold(int(arg), ThresholdType.MAX)
                case FormatEnum.LESS:
                    if arg:
                        try:
                            formatting.threshold = Threshold(int(arg), ThresholdType.LESS)
                        except ValueError:
                            raise RollException("Attempted to use < with non-integer")
                    else:
                        formatting.threshold = Threshold(int(arg), ThresholdType.MIN)
            idx += 2 if arg else 1
        return strip, formatting  # temporary!!!!!!!!!
