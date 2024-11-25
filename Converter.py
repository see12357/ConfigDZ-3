import json
import re
import sys

class ConfigTranslator:
    def __init__(self):
        self.constants = {}  # Сохранение объявленных констант

    def translate(self, input_json):
        try:
            parsed_data = json.loads(input_json)
        except json.JSONDecodeError as e:
            print(f"Ошибка синтаксиса JSON: {e}", file=sys.stderr)
            return

        try:
            return self.process_value(parsed_data)
        except Exception as e:
            print(f"Ошибка обработки данных: {e}", file=sys.stderr)

    def process_value(self, value):
        if isinstance(value, dict):
            return self.process_dict(value)
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Проверка: строка является выражением?
            if value.startswith(".{") and value.endswith("}."):
                return str(self.evaluate_expression(value))  # Вычисление выражения
            return f'"{value}"'  # Возвращаем строку как текст (в кавычках)
        else:
            raise ValueError(f"Неподдерживаемый тип значения: {value}")

    def process_dict(self, dictionary):
        result = "dict(\n"
        for key, value in dictionary.items():
            if not re.match(r'^[_a-z]+$', key):
                raise ValueError(f"Некорректное имя ключа: {key}")
            translated_value = self.process_value(value)
            result += f"  {key} = {translated_value},\n"
        result += ")"
        return result

    def declare_constant(self, name, value):
        if not re.match(r'^[_a-z]+$', name):
            raise ValueError(f"Некорректное имя переменной: {name}")
        self.constants[name] = value

    def evaluate_expression(self, expression):
        if not expression.startswith(".{") or not expression.endswith("}."):
            raise ValueError(f"Некорректное выражение: {expression}")
        parts = expression[2:-2].split()
        if not parts:
            raise ValueError(f"Пустое выражение: {expression}")
        operator = parts[0]
        operands = [self.get_constant_or_value(p) for p in parts[1:]]

        if operator == "+":
            return sum(operands)
            return print(opernds)
        elif operator == "min":
            return min(operands)
            return print(opernds)
        elif operator == "mod":
            if len(operands) != 2:
                raise ValueError(f"Операция mod требует 2 операнда: {expression}")
            return operands[0] % operands[1]
        else:
            raise ValueError(f"Неизвестная операция: {operator}")

    def get_constant_or_value(self, token):
        if token in self.constants:
            return self.constants[token]
        try:
            return int(token)
        except ValueError:
            raise ValueError(f"Неизвестный токен: {token}")

def main():
    translator = ConfigTranslator()
    input_data = sys.stdin.read()

    # Обработка строк для поддержки комментариев
    cleaned_input = re.sub(r'//.*', '', input_data)

    # Перевод JSON в учебный конфигурационный язык
    output = translator.translate(cleaned_input)
    if output:
        print(output)

if __name__ == "__main__":
    main()
