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
            ]
        )

    def button_clicked(self, e):
        data = e.control.content
        print(f"Button clicked with data = {data}")

        # Validacao e processamento das entradas
        if data == "AC":
            self.expression.value = ""
            self.result.value = "0"
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


def main(page: ft.Page):
    page.title = "Calc App"
    calc = CalculatorApp()

    page.add(calc)


ft.run(main)