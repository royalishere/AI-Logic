from algorithm import *

def main():
    idx = 1
    while True:
        try:
            algo = algorithms()
            input_file = "./INPUT/input_" + str(idx) + ".txt"
            output_file = "./OUTPUT/output_" + str(idx) + ".txt"
            algo.read_file(input_file)
            algo.pl_resolution()
            algo.write_file(output_file)
            
            idx = idx + 1
        except:
            break

if __name__ == '__main__':
    main()