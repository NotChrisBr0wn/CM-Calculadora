from dataclasses import field
import re
import flet as ft
from sympy import N, SympifyError, sympify

@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)


@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK


@ft.control
class ScientificButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_500
    color: ft.Colors = ft.Colors.WHITE


@ft.control
class CalculatorApp(ft.Container):
    def init(self):
        self.width = 350
        self.bgcolor = ft.Colors.BLACK
        self.border_radius = ft.BorderRadius.all(20)
        self.padding = 20
        self.expression = ft.Text(value="", color=ft.Colors.WHITE_54, size=16)
        self.result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)

        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[self.expression],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[self.result],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="CE", on_click=self.button_clicked),
                        ExtraActionButton(content="⌫", on_click=self.button_clicked),
                        ExtraActionButton(content="(", on_click=self.button_clicked),
                        ExtraActionButton(content=")", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ExtraActionButton(content="AC", on_click=self.button_clicked),
                        ExtraActionButton(content="+/-", on_click=self.button_clicked),
                        ExtraActionButton(content="%", on_click=self.button_clicked),
                        ActionButton(content="/", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="7", on_click=self.button_clicked),
                        DigitButton(content="8", on_click=self.button_clicked),
                        DigitButton(content="9", on_click=self.button_clicked),
                        ActionButton(content="*", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="4", on_click=self.button_clicked),
                        DigitButton(content="5", on_click=self.button_clicked),
                        DigitButton(content="6", on_click=self.button_clicked),
                        ActionButton(content="-", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(content="1", on_click=self.button_clicked),
                        DigitButton(content="2", on_click=self.button_clicked),
                        DigitButton(content="3", on_click=self.button_clicked),
                        ActionButton(content="+", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            content="0", expand=2, on_click=self.button_clicked
                        ),
                        DigitButton(content=".", on_click=self.button_clicked),
                        ActionButton(content="=", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ScientificButton(content="√", on_click=self.button_clicked),
                        ScientificButton(content="1/x", on_click=self.button_clicked),
                        ScientificButton(content="x²", on_click=self.button_clicked),
                        ScientificButton(content="log", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ScientificButton(content="e^x", on_click=self.button_clicked),
                        ScientificButton(content="!", on_click=self.button_clicked),
                        ScientificButton(content="sin", on_click=self.button_clicked),
                        ScientificButton(content="cos", on_click=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        ScientificButton(content="tan", on_click=self.button_clicked),
                        ScientificButton(content="|x|", on_click=self.button_clicked),
                        ScientificButton(content="rand", on_click=self.button_clicked),
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")

        # Validacao e processamento das entradas
        if data == "AC":
            self.expression.value = ""
            self.result.value = "0"
        elif data == "CE":
            self.result.value = "0"
            self.expression.value = ""
        elif data == "⌫":
            self.result.value = self.apagar(self.result.value)
            self.expression.value = self.result.value
        elif data == "=":
            evaluated = self.evaluate_expression(self.result.value)
            self.expression.value = self.result.value
            self.result.value = evaluated
        elif data == "+/-":
            self.result.value = self.last_number(self.result.value)
            self.expression.value = self.result.value
        elif data == "%":
            self.result.value = self.percent(self.result.value)
            self.expression.value = self.result.value
        elif data in ("+", "-", "*", "/"):
            self.result.value = self.add_operator(self.result.value, data)
            self.expression.value = self.result.value
        elif data in ("(", ")"):
            self.result.value = self.add_parenthesis(self.result.value, data)
            self.expression.value = self.result.value
        elif data == "√":
            self.result.value = self.apply_function(self.result.value, "sqrt")
            self.expression.value = self.result.value
        elif data == "1/x":
            self.result.value = self.apply_function(self.result.value, "inverse")
            self.expression.value = self.result.value
        elif data == "x²":
            self.result.value = self.apply_function(self.result.value, "square")
            self.expression.value = self.result.value
        elif data == "log":
            self.result.value = self.apply_function(self.result.value, "log")
            self.expression.value = self.result.value
        elif data == "e^x":
            self.result.value = self.apply_function(self.result.value, "exp")
            self.expression.value = self.result.value
        elif data == "!":
            self.result.value = self.apply_function(self.result.value, "factorial")
            self.expression.value = self.result.value
        elif data == "sin":
            self.result.value = self.apply_function(self.result.value, "sin")
            self.expression.value = self.result.value
        elif data == "cos":
            self.result.value = self.apply_function(self.result.value, "cos")
            self.expression.value = self.result.value
        elif data == "tan":
            self.result.value = self.apply_function(self.result.value, "tan")
            self.expression.value = self.result.value
        elif data == "|x|":
            self.result.value = self.apply_function(self.result.value, "abs")
            self.expression.value = self.result.value
        elif data == "rand":
            self.result.value = self.apply_function(self.result.value, "random")
            self.expression.value = self.result.value
        elif data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            self.result.value = self.add_digit(self.result.value, data)
            self.expression.value = self.result.value

        self.update()

    def add_digit(self, expression, digit):
        if expression in ("Error", "zoo", "nan"):
            expression = "0"

        if digit == ".":
            current = self.get_current_number(expression)
            if "." in current:
                return expression
            if not current:
                return expression + "0."
            return expression + "."

        if expression == "0":
            return digit

        if expression.endswith(tuple("+-*/")) and digit == "0":
            return expression + "0"

        return expression + digit

    def add_operator(self, expression, operator):
        if expression in ("Error", "zoo", "nan"):
            expression = "0"

        if expression.endswith(tuple("+-*/")):
            return expression[:-1] + operator

        return expression + operator

    def add_parenthesis(self, expression, paren):
        if expression in ("Error", "zoo", "nan"):
            expression = "0"
        # botao (
        if paren == "(":
            if expression == "0":
                return "("
            if expression.endswith(tuple("+-*/(")):
                return expression + "("
            return expression + "*("
        else:  # ")"
            if expression == "0":
                return "0"
            return expression + ")"

    def apagar(self, expression):
        if expression in ("Error", "zoo", "nan", "0", ""):
            return "0"
        
        result = expression[:-1]
        return result if result else "0"

    def apply_function(self, expression, func_name):
        if expression in ("Error", "zoo", "nan", ""):
            return "Error"

        try:
            value = float(self.get_current_number(expression))
        except (ValueError, ZeroDivisionError):
            return "Error"

        prefix = expression[:len(expression) - len(self.get_current_number(expression))]

        if func_name == "sqrt":
            return prefix + f"sqrt({value})"
        elif func_name == "inverse":
            if value == 0:
                return "Error"
            return prefix + f"(1/{value})"
        elif func_name == "square":
            return prefix + f"({value}**2)"
        elif func_name == "log":
            if value <= 0:
                return "Error"
            return prefix + f"log({value})"
        elif func_name == "exp":
            return prefix + f"exp({value})"
        elif func_name == "factorial":
            return prefix + f"factorial({value})"
        elif func_name == "sin":
            return prefix + f"sin({value})"
        elif func_name == "cos":
            return prefix + f"cos({value})"
        elif func_name == "tan":
            return prefix + f"tan({value})"
        elif func_name == "abs":
            return prefix + f"abs({value})"
        elif func_name == "random":
            import random
            rand_val = random.random()
            return prefix + str(round(rand_val, 6))
        
        return "Error"

    def get_current_number(self, expression):
        for index in range(len(expression) - 1, -1, -1):
            if expression[index] in "+-*/":
                return expression[index + 1 :]
        return expression

    def last_number(self, expression):
        if expression in ("0", "Error", "zoo", "nan"):
            return "0"

        match = re.search(r"(\d*\.?\d+)$", expression)
        if not match:
            return expression

        start, end = match.span()
        number = expression[start:end]

        if start > 0 and expression[start - 1] == "-":
            if start == 1 or expression[start - 2] in "+-*/":
                return expression[: start - 1] + number

        return expression[:start] + "-" + number

    def percent(self, expression):
        if expression in ("Error", "zoo", "nan"):
            return "0"

        match = re.search(r"(\d*\.?\d+)$", expression)
        if not match:
            return expression

        start, end = match.span()
        number = expression[start:end]
        return expression[:start] + f"({number}/100)"

    def evaluate_expression(self, expression):
        try:
            value = N(sympify(expression), 12)
            if value in ("zoo", "nan"):
                return "Error"
            return self.format_number(value)
        except (SympifyError, ZeroDivisionError, TypeError, ValueError):
            return "Error"

    def format_number(self, value):
        text = str(value)
        if text.endswith(".0"):
            return text[:-2]
        if "." in text:
            return text.rstrip("0").rstrip(".")
        return text
    def format_with_thousands(self, text):
        """Format number display with space as thousands separator"""
        if not text or text in ("0", "Error", "zoo", "nan"):
            return text
        
        # salta se conter funcoes
        if not all(c in "0123456789.-" for c in text):
            return text
        
        # Lida com numeros negativos
        is_negative = text.startswith("-")
        if is_negative:
            text = text[1:]
        
        # Separa parte inteira da decimal
        if "." in text:
            integer_part, decimal_part = text.split(".")
        else:
            integer_part = text
            decimal_part = None
        
        # Aplica formatação de milhares à parte inteira
        formatted_int = ""
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                formatted_int = " " + formatted_int
            formatted_int = digit + formatted_int
        
        result = formatted_int
        if decimal_part:
            result += "." + decimal_part
        
        if is_negative:
            result = "-" + result
        
        return result
def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()

    page.add(calc)


ft.run(main)