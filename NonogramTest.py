import time
from NonogramSolver import Nonogram, NonogramSolver

entries = [
    "input_3x3.txt", "input_0.txt", "input.txt", 
    "input_01.txt", "input_1.txt", "input_8x8.txt",
    "input_11.txt", "input_3.txt", "input_2.txt",
    "input_9.txt", "input_8.txt", "input_S.txt",
    "input_12.txt", "input_13.txt", "input_J.txt",
    "input_7.txt", "input_15x25.txt", "input_15x30.txt",
    "input_00.txt",   
    #, "input_4.txt", "input_5.txt","input_6.txt","input_10.txt", 
]
#print(entries)
for i in range(len(entries)):
    nono = Nonogram( "nonograms/"+entries[i] )
    print(entries[i], len(nono.columns)*len(nono.rows), end=' ')
    tS = time.process_time()
    result = NonogramSolver.solveNonogram( nono )
    tE = time.process_time()
    if result[1]:
        print(nono.getDensity(), tE-tS)