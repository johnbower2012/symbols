import re
import math

class Compute:
    def __init__(self, equation=''):
        self.equation = equation
        self.variables = []
        self.result = ''

    def equation(self):
        self.equation = input("Enter equation: ")

    def variables(self):
        self.variables = re.findall('(\S+)',input("Variables: "))

    def parentheses(self, equation):
        return re.findall('(\([^(]*?\))', equation)

    def factorial(self, equation):
        return re.findall(r'(\d*\.?\d+)(\!)', equation)

    def power(self, equation):
        return re.findall(r'(\d*\.?\d+)(\^)(\d*\.?\d+)', equation)

    def multdiv(self, equation):
        return re.findall(r'(\d*\.?\d+)([*/])(\d*\.?\d+)', equation)

    def addsub(self, equation):
        return re.findall(r'(\d*\.?\d+)([+-])(\d*\.?\d+)', equation)

    def numeric(self, equation):
        return re.match(r'\d*\.?\d+$', equation)

    def compute(self, equation, printing=False):
        equation = re.sub('[\s]', '', equation)
        if printing:
            print('computing: ', equation)
        left = re.findall('\(', equation)
        right = re.findall('\)', equation)
        if len(left) != len(right):
            print('Mismatched parentheses. Unable to resolve:', equation)
            return equation
        while True:
            if printing:
                print('current iteration:', equation)
            progress = False
            if self.numeric(equation):
                if printing:
                    print('done')
                progress = True
                break
            while terms := self.parentheses(equation):
                term = terms[0]
                if printing:
                    print('resolving parentheses:', term)
                term2 = f'\\{term[:-1]}\\{term[-1]}'
                term2 = re.sub('\^', '\^', term2)
                term2 = re.sub('\*', '\*', term2)
                term2 = re.sub('\+', '\+', term2)
                equation = re.sub(term2, self.compute(term[1:-1], printing), equation)
                progress = True
            while terms := self.factorial(equation):
                term = terms[0]
                if printing:
                    print('resolving factorial:', term, 'as', x := str(math.factorial(float(term[0]))))
                else:
                    x = str(math.factorial(float(term[0])))
                term2 = str(term[0]) + '\\' + str(term[1])
                equation = re.sub(term2, x, equation)
                progress = True
            while terms := self.power(equation):
                term = terms[0]
                if printing:
                    print('resolving power:', term, 'as', x := str(float(term[0]) ** float(term[2])))
                else:
                    x = str(float(term[0]) ** float(term[2]))
                term2 = str(term[0]) + '\\' + ''.join(term[1:])
                equation = re.sub(term2, x, equation)
                progress = True
            while terms := self.multdiv(equation):
                term = terms[0]
                if term[1] == '*':
                    if printing:
                        print('resolving multiplication:', term, 'as', x := str(float(term[0]) * float(term[2])))
                    else:
                        x = str(float(term[0]) * float(term[2]))
                    term2 = re.sub('\*', '\*', ''.join(term))
                    equation = re.sub(term2, x, equation)
                elif float(term[2]) != 0 and term[1] == '/':
                    if printing:
                        print('resolving division:', term, 'as', x := str(float(term[0]) / float(term[2])))
                    else:
                        x = str(float(term[0]) / float(term[2]))
                    equation = re.sub(''.join(term), x, equation)
                else:
                    print('Division by zero occurred:', term)
                    break
                progress = True
            while terms := self.addsub(equation):
                term = terms[0]
                if term[1] == '+':
                    if printing:
                        print('resolving addition:', term, 'as', x := str(float(term[0]) + float(term[2])))
                    else:
                        x = str(float(term[0]) + float(term[2]))
                    term2 = re.sub('\+', '\+', ''.join(term))
                    equation = re.sub(term2, x, equation)
                elif term[1] == '-':
                    if printing:
                        print('resolving subtraction:', term, 'as', x := str(float(term[0]) - float(term[2])))
                    else:
                        x = str(float(term[0]) - float(term[2]))
                    equation = re.sub(''.join(term), x, equation)
                progress = True
            if not progress:
                print('unable to resolve equation:', equation)
                break
            if printing:
                print('looping')
        return equation
    
    def compute_result(self, printing=False):
        self.result = self.compute(self.equation, printing)
