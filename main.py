import math, random, sys
from copy import deepcopy

gv = 0
# Disabling pylint warning in static methods...
# pylint: disable=no-member
# pylint: disable=no-self-argument
class Nonogram:
  def __init__(self, fileName = None):
    self.matrix = [] # -1, 0, 1
    self.rows = []
    self.columns = []
    if fileName != None:
      self.initialize( fileName )


  def initialize(self, fileName):
    self.readFile( fileName )
    for i in range (len(self.rows)):
      fil = []
      for j in range(len(self.columns)):
        fil.append(0)
      self.matrix.append(fil)

  def readFile( self, fileName ):
    colLine = ""
    rowLine = ""
    with open(fileName, "r") as file:
      colLine = file.readline()
      rowLine = file.readline()
    cols = colLine.split(" ")
    rows = rowLine.split(" ")
    for i in range(len(cols)):
      col = cols[i].split("|")
      colDict = []
      for c in col:
        colDict.append({"num": int(c), "mark": False, "p" : 0})
      self.columns.append(colDict) 
    for i in range(len(rows)):
      row = rows[i].split("|")
      rowDict = []
      for r in row:
        rowDict.append({"num": int(r), "mark": False, "p" : 0})
      self.rows.append(rowDict) 

  def printColsRows( self ):
    maxiCol = 0
    maxiRow = 0
    for col in self.columns:
      if len(col) > maxiCol:
        maxiCol = len(col)
    for row in self.rows:
      if len(row) > maxiRow:
        maxiRow = len(row)

    #print("--Values are in Hexadecimal--")
    for i in range(maxiCol, 0, -1):
      print(" "*maxiRow, end='')
      for j in range(len(self.columns)):
        if len(self.columns[j]) >= i:
          print('{:x}'.format(int(self.columns[j][len(self.columns[j])-i]["num"])),end='')
        else:
          print(" ", end='')
      print("")
      
    for i in range(len(self.rows)):
      print(" "*(maxiRow - len(self.rows[i])), end='')
      for j in range(len(self.rows[i])):
        print('{:x}'.format(int(self.rows[i][j]["num"])), end='')
      for j in range(len(self.columns)):
        if self.matrix[i][j] == 0:
          print(".", end='')
        elif self.matrix[i][j] == 1:
          print("O", end='')
        elif self.matrix[i][j] == -1:
          print("X", end='')
      print("")
  
  def saveNonogram( self, fileName ):
    with open( fileName, "wb" ) as file:
      file.write("P5\n".encode('ascii'))
      file.write("{} {}\n255\n".format(len(self.columns), len(self.rows) ).encode('ascii') )
      for i in range(len(self.rows)):
        vals = []
        for j in range(len(self.columns)):
          if self.matrix[i][j] == 1:
            vals.append(0)
          else:
            vals.append(255)
        newFileByteArray = bytearray(vals)
        file.write(newFileByteArray)


class NonogramSolver:

  def solveNonogram( nonogram ):
    
    nono = Nonogram()
    nono.matrix = nonogram.matrix.copy()
    nono.rows = nonogram.rows.copy()
    nono.columns = nonogram.columns.copy()
    for i in range(len(nono.rows)):
      nono.rows[i].append({"num" : 0, "mark" : False, "p" : 0})
    for i in range(len(nono.columns)):
      nono.columns[i].append({"num" : 0, "mark" : False, "p" : 0})
    row_idx = [0]*(len(nono.rows))
    col_idx = [0]*(len(nono.columns))
    result =  NonogramSolver.solveNonogram_Aux( nono, 0, 0, row_idx ,col_idx )
    return(result, nono)

  def finishedNonogram( nonogram ):
    #nonogram.printColsRows()
    for row in nonogram.matrix:
      for item in row:
        if item == 0:
          return False
    for row in nonogram.rows:
      for item in row:
        if item["num"] != 0:
          return False
    for col in nonogram.columns:
      for item in col:
        if item["num"] != 0:
          return False
    return True

  def toPaintValid( nonogram, i, j, row_idx, col_idx ):
    if nonogram.rows[i][row_idx[i]]["num"] > 0 and nonogram.columns[j][col_idx[j]]["num"] > 0:
      # nonogram.matrix[i][j] = 1
      return True
    else:
      return False

  def toMarkValid(nonogram, i, j, row_idx, col_idx):
    if nonogram.rows[i][row_idx[i]]["num"] == 0 and nonogram.columns[j][col_idx[j]]["num"] == 0:
      return True
    else:
      return False
    
  def solveNonogram_Aux ( nonogram, i, j, row_idx, col_idx ):
    # print(".", end='')
    '''global gv
    nonogram.saveNonogram( "./images/out"+str(gv)+".pgm")
    gv +=1'''
    if NonogramSolver.finishedNonogram( nonogram ):
      print(i,j,"Finished nonogram")
      return True
    elif 0 <= i < len(nonogram.rows) and 0 <= j < len(nonogram.columns):
      toValidPaint = NonogramSolver.toPaintValid( nonogram, i, j, row_idx, col_idx ) 
      valid = False
      if toValidPaint:
        #print( i, j , "{", row_idx[i], col_idx[j], "}")
        #nonogram.printColsRows()
        #print("")
        # pintar
        #print(i,j,"toValidPaint = true")
        
        nonogram.matrix[i][j] = 1
        nonogram.rows[i][row_idx[i]]["num"]  -= 1
        nonogram.columns[j][col_idx[j]]["num"] -= 1
        nonogram.rows[i][row_idx[i]]["p"]  += 1
        nonogram.columns[j][col_idx[j]]["p"] += 1
        #print(i,j,"painted")
        valid = False
        n_ri = row_idx.copy()
        n_ci = col_idx.copy()
        if ( i + 1 ) >= len(nonogram.rows):
          valid = NonogramSolver.solveNonogram_Aux( nonogram, 0, j+1, n_ri, n_ci)
        else:
          valid = NonogramSolver.solveNonogram_Aux( nonogram, i+1, j, n_ri, n_ci)
        #print(i, j, "valid =", valid)
        if valid == False:
          nonogram.rows[i][row_idx[i]]["num"]  += 1
          nonogram.columns[j][col_idx[j]]["num"] += 1
          nonogram.rows[i][row_idx[i]]["p"]  -= 1
          nonogram.columns[j][col_idx[j]]["p"] -= 1          

      if not valid or not toValidPaint:
        #print( i, j , "{", row_idx[i], col_idx[j], "}")
        #nonogram.printColsRows()
        #print("")
        #print(i,j,"going to check if Mark")
        
        if not valid or NonogramSolver.toMarkValid( nonogram, i, j, row_idx, col_idx ):
          #print(i,j, "{", row_idx[i], col_idx[j], "} going to check advance in idx ")
          if nonogram.rows[i][row_idx[i]]["num"] == 0:
            ##print(i,j,"idx by rows")
            if row_idx[i] < len(nonogram.rows[i]) - 1:
              row_idx[i] += 1
          
          if nonogram.columns[j][col_idx[j]]["num"] != 0 and \
              nonogram.columns[j][col_idx[j]]["p"] > 0 and \
            col_idx[j] < len(nonogram.columns[j]) - 1:
              return False
          
          if nonogram.columns[j][col_idx[j]]["num"] == 0:
            #print(i,j,"idx by cols")
            if col_idx[j] < len(nonogram.columns[j]) - 1:
              col_idx[j] += 1
          
          if nonogram.rows[i][row_idx[i]]["num"] != 0 and \
               nonogram.rows[i][row_idx[i]]["p"] > 0 and \
            row_idx[i] < len(nonogram.rows[i]) - 1:
              return False
            
          #print(i,j,"going to mark")
          validMark = False
          nonogram.matrix[i][j] = -1
          #print(i,j,"marked")
          n_ri = row_idx.copy()
          n_ci = col_idx.copy()
          if ( i + 1 ) >= len(nonogram.rows):
            validMark = NonogramSolver.solveNonogram_Aux( nonogram, 0, j+1, n_ri, n_ci)
          else:
            validMark = NonogramSolver.solveNonogram_Aux( nonogram, i+1, j, n_ri, n_ci)
          #print(i,j,"validMark =", validMark)
          return validMark
        return False
      return valid
    else:
      return False


if len(sys.argv) != 2:
  print("Error. Usage:",sys.argv[0],"fileName")
  exit()

nono = Nonogram(sys.argv[1])
nono.printColsRows()
print("Size:",len(nono.rows),"x", len(nono.columns))
print("About to solve Nonogram")
print("Solving", end='')
print(NonogramSolver.solveNonogram( nono ))
nono.saveNonogram("out.pgm")
nono.printColsRows()