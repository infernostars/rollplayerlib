from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List
from .enums import OperationEnum

ABCBonusTypeVar = TypeVar('ABCBonusTypeVar', bound='ABCBonus')


class ABCBonus(ABC, Generic[ABCBonusTypeVar]):
    @abstractmethod
    def apply_bonus(self, rolled_dice: list[int]) -> list[int]: ...

    @classmethod
    @abstractmethod
    def parse(cls, input_string: str) -> ABCBonusTypeVar: ...


class Bonus(ABCBonus):
    def __init__(self, operation, value):
        self.operation = operation
        self.value = value

    def __repr__(self):
        return f"Bonus(operation={self.operation}, value={self.value})"

    def apply_bonus(self, rolled_dice: list[int]) -> list[int]:
        new_dice = []
        for i in rolled_dice:
            if self.operation == "+":
                new_dice.append(i + self.value)
            if self.operation == "-":
                new_dice.append(i - self.value)
            if self.operation == "/":
                new_dice.append(i / self.value)
            if self.operation == "*":
                new_dice.append(i * self.value)
            if self.operation == "**":
                new_dice.append(i ** self.value)
        return new_dice

    @classmethod
    def parse(cls, input_string) -> List['Bonus']:
        bonuses = []
        current_num = ''
        current_op = None

        for char in input_string:
            if char in [op.value for op in OperationEnum]:  # Check if char is an operation
                if current_num:  # If there's a number buffered, create a Bonus
                    bonuses.append(Bonus(current_op, float(current_num)))
                    current_num = ''  # Reset current number
                current_op = OperationEnum(char)  # Set current operation
            else:
                current_num += char  # Buffer the number

        # Handle the last buffered number
        if current_num and current_op:
            bonuses.append(Bonus(current_op, float(current_num)))

        return bonuses


class TargetedBonus(ABCBonus):
    def __init__(self, rolls, ops):
        self.rolls = rolls
        self.operations = ops

    def __repr__(self):
        return f"TargetedBonus(numbers={self.rolls}, operations={self.operations})"

    def apply_bonus(self, rolled_dice: list[int]) -> list[int]:
        new_dice = rolled_dice[:]

        # Apply each operation in sequence
        for operation in self.operations:
            temp_dice = new_dice[:]  # Copy the current state of new_dice for modification
            for i, dice_val in enumerate(new_dice):
                # Check if the dice index + 1 is in the targeted rolls
                if i + 1 in self.rolls:
                    # Apply the operation based on the operation type
                    if operation[0] == "+":
                        temp_dice[i] = dice_val + operation[1]
                    elif operation[0] == "-":
                        temp_dice[i] = dice_val - operation[1]
                    elif operation[0] == "/":
                        temp_dice[i] = dice_val / operation[1]
                    elif operation[0] == "*":
                        temp_dice[i] = dice_val * operation[1]
                    elif operation[0] == "**":
                        temp_dice[i] = dice_val ** operation[1]
            # Update new_dice with the results of the current operation
            new_dice = temp_dice[:]

        # Return the final modified dice
        return new_dice

    @classmethod
    def parse_string(cls, input_string):
        # Split the input string into two parts: the numbers and the operations
        parts = input_string.split(':')
        numbers_str = parts[0][1:]  # Remove the leading 'i' from the numbers part
        ops_str = parts[1]  # Get the operations string

        # Convert the numbers part into a list of integers
        numbers = [int(num) for num in numbers_str.split(',')]

        # Convert the operations string into a list of tuples (OperationEnum, value)
        ops = []
        current_op = ''
        for char in ops_str:
            if char == 'i':
                if current_op:
                    op_enum, value = OperationEnum(current_op[0]), float(current_op[1:])
                    ops.append((op_enum, value))
                    current_op = ''
                break
            elif char in [op.value for op in OperationEnum]:
                if current_op:
                    op_enum, value = OperationEnum(current_op[0]), float(current_op[1:])
                    ops.append((op_enum, value))
                    current_op = char
                else:
                    current_op = char
            else:
                current_op += char

        if current_op:
            op_enum, value = OperationEnum(current_op[0]), float(current_op[1:])
            ops.append((op_enum, value))

        return TargetedBonus(numbers, ops)

    @classmethod
    def parse(cls, input_string) -> list['TargetedBonus']:
        parsed_data_list = []
        # Find the position of the last semicolon
        last_semicolon_idx = input_string.rfind(';')
        # If there's no semicolon, use the entire text; otherwise, use text up to the last semicolon
        text_to_parse = input_string if last_semicolon_idx == -1 else input_string[:last_semicolon_idx]

        segment_starts = [i for i, char in enumerate(text_to_parse) if char == 'i']  # Find all 'i' positions

        for i, start_idx in enumerate(segment_starts):
            # Determine the end of the current segment
            if i < len(segment_starts) - 1:
                next_start = segment_starts[i + 1]
                end_idx = text_to_parse.rfind(';', start_idx, next_start)
                if end_idx == -1:  # If no semicolon is found before the next 'i', use the next 'i' as the end
                    end_idx = next_start
            else:
                # For the last segment, the end is the position of the last semicolon or the end of the text
                end_idx = len(text_to_parse)

            # Parse the segment into a TargetedBonus object
            segment = text_to_parse[start_idx:end_idx]
            parsed_data = cls.parse_string(segment)
            parsed_data_list.append(parsed_data)

        return parsed_data_list
