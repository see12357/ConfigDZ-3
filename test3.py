import unittest
from io import StringIO
import sys
from Converter import ConfigTranslator  # Предполагаем, что ваш код находится в файле `translator.py`.

class TestConfigTranslator(unittest.TestCase):
    def setUp(self):
        """Настройка для каждого теста."""
        self.translator = ConfigTranslator()
        
    def test_translate_valid_json(self):
        # Тест для строки 1-23
        input_json = '{"key": "value"}'
        expected_output = 'dict(\n  key = "value",\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)
        
    def test_translate_invalid_json(self):
        # Тест для строки 1-23
        input_json = '{"key": "value"'
        captured_output = StringIO()
        sys.stderr = captured_output
        self.assertIsNone(self.translator.translate(input_json))
        sys.stderr = sys.__stderr__
        self.assertIn("Ошибка синтаксиса JSON", captured_output.getvalue())


    def test_simple_translation(self):
        """Тест на преобразование простого словаря JSON."""
        input_json = '{"key": "value", "number": 42}'
        expected_output = 'dict(\n  key = "value",\n  number = 42,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_expression_evaluation(self):
        """Тест на вычисление выражений."""
        input_json = '{"sum_example": ".{+ 5 10}."}'
        expected_output = 'dict(\n  sum_example = 15,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_nested_dictionary(self):
        """Тест на обработку вложенных словарей."""
        input_json = '{"outer_key": {"inner_key": 10}}'
        expected_output = 'dict(\n  outer_key = dict(\n  inner_key = 10,\n),\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_mod_operation(self):
        """Тест на операцию mod."""
        input_json = '{"mod_example": ".{mod 10 3}."}'
        expected_output = 'dict(\n  mod_example = 1,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_min_operation(self):
        """Тест на операцию min."""
        input_json = '{"min_example": ".{min 3 7 1}."}'
        expected_output = 'dict(\n  min_example = 1,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)


    def test_constants(self):
        """Тест на использование объявленных констант."""
        self.translator.declare_constant("a", 10)
        input_json = '{"sum_with_constant": ".{+ a 5}."}'
        expected_output = 'dict(\n  sum_with_constant = 15,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_unsupported_value_type(self):
        """Тест на неподдерживаемый тип значения."""
        input_json = '{"unsupported_value": [1, 2, 3]}'
        with self.assertRaises(ValueError):
            self.translator.translate(input_json)

    def test_invalid_key(self):
        with self.assertRaises(ValueError):
            self.translator.process_dict({"1invalid_key": "value"})  # Некорректное имя ключа

    def test_unsupported_value_type(self):
        with self.assertRaises(ValueError):
            self.translator.process_value([1, 2, 3])

    def test_empty_data(self):
        input_json = '{}'
        expected_output = 'dict(\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

    def test_invalid_expression_syntax(self):
        with self.assertRaises(ValueError):
            self.translator.evaluate_expression(".{+ 5}")  # Некорректное выражение без второго операнда

    def test_invalid_key_format(self):
        with self.assertRaises(ValueError):
            self.translator.process_dict({"1invalid_key": "value"})  # Некорректное имя ключа
            
    def test_nested_dict(self):
        input_json = '{"outer_key": {"inner_key": 10}}'
        expected_output = 'dict(\n  outer_key = dict(\n  inner_key = 10,\n),\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)
        
    def test_valid_expression(self):
        input_json = '{"sum_example": ".{+ 5 10}.", "sum_with_constant": ".{+ 3 3}."}'
        expected_output = 'dict(\n  sum_example = 15,\n  sum_with_constant = 6,\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)
        
    def test_dict_with_mixed_types(self):
        input_json = '{"mixed": {"key": 10, "subkey": ".{+ 5 5}."}}'
        expected_output = 'dict(\n  mixed = dict(\n  key = 10,\n  subkey = 10,\n),\n)'
        self.assertEqual(self.translator.translate(input_json), expected_output)

if __name__ == "__main__":
    unittest.main()
