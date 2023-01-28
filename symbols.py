import re
import sys
import math


class Compute:
    def __init__(self, equation=''):
        self.equation = equation
        self.result = ''

    def fetch_equation():
        self.equation = input("Enter equation: ")

    def fetch_variables():
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
        return re.match(r'^[+-]{0,1}((\d*\.)|\d*)\d+$', equation)

    def compute(self, equation):
        equation = re.sub(' ', '', equation)
        print('computing: ', equation)
        left = re.findall('\(', equation)
        right = re.findall('\)', equation)
        if len(left) != len(right):
            print('Mismatched parentheses. Unable to resolve:', equation)
            return equation
        done = False
        while True:
            if self.numeric(equation):
                # print('done')
                break
            elif self.parentheses(equation):
                for term in self.parentheses(equation):
                    # print('resolving parentheses:', term)
                    term2 = f'\\{term[:-1]}\\{term[-1]}'
                    term2 = re.sub('\^', '\^', term2)
                    term2 = re.sub('\*', '\*', term2)
                    term2 = re.sub('\+', '\+', term2)
                    equation = re.sub(term2, self.compute(term[1:-1]), equation)
            elif self.factorial(equation):
                for term in self.factorial(equation):
                    # print('resolving factorial:', term, 'as', str(math.factorial(float(term[0]))))
                    term2 = str(term[0]) + '\\' + str(term[1])
                    equation = re.sub(term2, str(math.factorial(float(term[0]))), equation)
            elif self.power(equation):
                for term in self.power(equation):
                    # print('resolving power:', term, 'as', str(float(term[0]) ** float(term[2])))
                    term2 = str(term[0]) + '\\' + ''.join(term[1:])
                    equation = re.sub(term2, str(float(term[0]) ** float(term[2])), equation)
            elif self.multdiv(equation):
                for term in self.multdiv(equation):
                    if term[1] == '*':
                        # print('resolving multiplication:', term, 'as', str(float(term[0]) * float(term[2])))
                        term2 = re.sub('\*', '\*', ''.join(term))
                        equation = re.sub(term2, str(float(term[0]) * float(term[2])), equation)
                    elif float(term[2]) != 0 and term[1] == '/':
                        # print('resolving division:', term, 'as', str(float(term[0]) / float(term[2])))
                        equation = re.sub(''.join(term), str(float(term[0]) / float(term[2])), equation)
                    else:
                        print('Division by zero occurred:', term)
                        done = True
                        break
            elif self.addsub(equation):
                for term in self.addsub(equation):
                    if term[1] == '+':
                        # print('resolving addition:', term, 'as', str(float(term[0]) + float(term[2])))
                        term2 = re.sub('\+', '\+', ''.join(term))
                        equation = re.sub(term2, str(float(term[0]) + float(term[2])), equation)
                    elif term[1] == '-':
                        # print('resolving subtraction:', term, 'as', str(float(term[0]) - float(term[2])))
                        equation = re.sub(''.join(term), str(float(term[0]) - float(term[2])), equation)
            else:
                print('unable to resolve equation:', equation)
                break
            if done:
                break
            # print('looping')
        return equation  
        
def main():
    equation = '3!*2* ((3!+4 *5 ^2     /6)    *(7))'
    #equation = input("enter equation to resolve: ")
    computation = Compute(equation)
    computation.result = computation.compute(equation)
    print('equation start:', computation.equation)
    print('result:', computation.result)

if __name__ == "__main__":
    main()