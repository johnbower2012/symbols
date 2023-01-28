import sys
from symbols10 import Compute  

def main():
    fname = 'equation.txt' #input('equation file name: ')
    try:
        with open(fname, 'r') as file:
            equation = file.read()
    except:
        sys.exit(f'Unable to load file: {fname}')
    solver = Compute(equation)
    print('equation start:', solver.equation)
    solver.compute_result(printing=True)
    print('result:', solver.result)

if __name__ == "__main__":
    main()