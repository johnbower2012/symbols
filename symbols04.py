import re
import sys
import math


def equation():
    return input("Enter equation: ")

def variables():
    return re.findall('(\S+)',input("Variables: "))

def parentheses(equation):
    return re.findall('(\([^(]*?\))', equation)

def factorial(equation):
    return re.findall(r'(\d*\.?\d+)(\!)', equation)

def power(equation):
    return re.findall(r'(\d*\.?\d+)(\^)(\d*\.?\d+)', equation)

def multdiv(equation):
    return re.findall(r'(\d*\.?\d+)([*/])(\d*\.?\d+)', equation)

def addsub(equation):
    return re.findall(r'(\d*\.?\d+)([+-])(\d*\.?\d+)', equation)

def numeric(equation):
    return re.match(r'\d*\.?\d+$', equation)

def compute(equation, printing=False):
    equation = re.sub(' ', '', equation)
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
        if numeric(equation):
            if printing:
                print('done')
            progress = True
            break
        while parentheses(equation):
            term = parentheses(equation)[0]
            if printing:
                print('resolving parentheses:', term)
            term2 = f'\\{term[:-1]}\\{term[-1]}'
            term2 = re.sub('\^', '\^', term2)
            term2 = re.sub('\*', '\*', term2)
            term2 = re.sub('\+', '\+', term2)
            equation = re.sub(term2, compute(term[1:-1], printing), equation)
            progress = True
        while factorial(equation):
            term = factorial(equation)[0]
            if printing:
                print('resolving factorial:', term, 'as', str(math.factorial(float(term[0]))))
            term2 = str(term[0]) + '\\' + str(term[1])
            equation = re.sub(term2, str(math.factorial(float(term[0]))), equation)
            progress = True
        while power(equation):
            term = power(equation)[0]
            if printing:
                print('resolving power:', term, 'as', str(float(term[0]) ** float(term[2])))
            term2 = str(term[0]) + '\\' + ''.join(term[1:])
            equation = re.sub(term2, str(float(term[0]) ** float(term[2])), equation)
            progress = True
        while multdiv(equation):
            term = multdiv(equation)[0]
            if term[1] == '*':
                if printing:
                    print('resolving multiplication:', term, 'as', str(float(term[0]) * float(term[2])))
                term2 = re.sub('\*', '\*', ''.join(term))
                equation = re.sub(term2, str(float(term[0]) * float(term[2])), equation)
            elif float(term[2]) != 0 and term[1] == '/':
                if printing:
                    print('resolving division:', term, 'as', str(float(term[0]) / float(term[2])))
                equation = re.sub(''.join(term), str(float(term[0]) / float(term[2])), equation)
            else:
                print('Division by zero occurred:', term)
                break
            progress = True
        while addsub(equation):
            term = addsub(equation)[0]
            if term[1] == '+':
                if printing:
                    print('resolving addition:', term, 'as', str(float(term[0]) + float(term[2])))
                term2 = re.sub('\+', '\+', ''.join(term))
                equation = re.sub(term2, str(float(term[0]) + float(term[2])), equation)
            elif term[1] == '-':
                if printing:
                    print('resolving subtraction:', term, 'as', str(float(term[0]) - float(term[2])))
                equation = re.sub(''.join(term), str(float(term[0]) - float(term[2])), equation)
            progress = True
        if not progress:
            print('unable to resolve equation:', equation)
            break
        if printing:
            print('looping')
    return equation  
        
def main():
    equation = '3!*2* ((3!+4 *5 ^2     /6)    *(7))'
    #equation = '((1+2) *4/(5     ^2)*2!  )^3/5'
    #equation = input("enter equation to resolve: ")
    print('equation start:', equation)
    print('result:', compute(equation, printing=True))

if __name__ == "__main__":
    main()