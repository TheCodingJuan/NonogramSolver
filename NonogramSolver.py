'''
NonogramSolver.py
By: Juan Jose Camacho Cala
    Sergio Andres Mejia Tovar
    Julian David Parada Galvis
Analisis de Algortimos 2020-30
Proyecto final
'''

import math, random, sys
from copy import deepcopy
# Disabling pylint warning in static methods...
# pylint: disable=no-member
# pylint: disable=no-self-argument

# --------------------------------------
# --------------------------------------
# CLASS NONOGRAM
#  Class that represents a Nonogram
#  attr:
#   matrix[][]: Saves the cell table, saving 0 when no action has been done
#                                            1 when it has been painted
#                                           -1 when it has been marked
#   rows[][]: Saves the row numbers. In each row it's saved its list of numbers.
#             Each number saves the group size (the number itself), 
#             if it has been marked and the painted amount of the group. 
#   columns[][]: Saves the column numbers. In each column it's saved its list of numbers.
#             Each number saves the group size (the number itself), 
#             if it has been marked and the painted amount of the group. 
# --------------------------------------
# --------------------------------------
class Nonogram:

  # --------------------------------------
  # Nonogram class constructor, may receive a file to read the rows and cols from it
  # --------------------------------------
  def __init__(self, fileName = None):
    self.matrix = [] # -1, 0, 1
    self.rows = []
    self.columns = []
    if fileName != None:
      self.initialize( fileName )
    # end if
  # end def
  
  # --------------------------------------
  # initialize: Function that initializes rows, columns and matrix
  #   params: 
  #    fileName: Name of file to read the rows and cols numbers
  # --------------------------------------
  def initialize(self, fileName):
    self.readFile( fileName )
    self.matrix = [ [ 0 for _ in range(len(self.columns)) ] for _ in range(len(self.rows)) ]
  # end def

  # --------------------------------------
  # readFile: Function that reads a file containing the rows and cols numbers
  #   params:
  #    fileName: Name of file to read the rows and cols numbers. This file consists
  #              on two lines, the first are col numbers and the second are row numbers.
  #              Each col or row is separated by a space and numbers in the same col or row
  #              are separated by a |
  # --------------------------------------
  def readFile( self, fileName ):
    colLine = ""
    rowLine = ""
    with open(fileName, "r") as file:
      colLine = file.readline()
      rowLine = file.readline()
    # end with
    cols = colLine.split(" ")
    rows = rowLine.split(" ")
    for i in range(len(cols)):
      col = cols[i].split("|")
      colDict = []
      for c in col:
        colDict.append({"num": int(c), "mark": False, "painted" : 0})
      # end for
      self.columns.append(colDict) 
    # end for
    for i in range(len(rows)):
      row = rows[i].split("|")
      rowDict = []
      for r in row:
        rowDict.append({"num": int(r), "mark": False, "painted" : 0})
      # end for
      self.rows.append(rowDict) 
    # end for
  # end def

  # --------------------------------------
  # printColsRows: Prints the Nonogram in the console in a kinda friendly way
  # --------------------------------------
  def printColsRows( self ):
    maxiCol = 0
    maxiRow = 0
    for col in self.columns:
      if len(col) > maxiCol:
        maxiCol = len(col)
      # end if
    # end for
    for row in self.rows:
      if len(row) > maxiRow:
        maxiRow = len(row)
      # end if
    #end for
    print("--Values are in Hexadecimal--")
    for i in range(maxiCol, 0, -1):
      print(" "*maxiRow, end='')
      for j in range(len(self.columns)):
        if len(self.columns[j]) >= i:
          print('{:x}'.format(int(self.columns[j][len(self.columns[j])-i]["num"])),end='')
        else:
          print(" ", end='')
        # end if
      # end for
      print("")
    # end for
      
    for i in range(len(self.rows)):
      print(" "*(maxiRow - len(self.rows[i])), end='')
      for j in range(len(self.rows[i])):
        print('{:x}'.format(int(self.rows[i][j]["num"])), end='')
      # end for
      for j in range(len(self.columns)):
        if self.matrix[i][j] == 0:
          print(".", end='')
        elif self.matrix[i][j] == 1:
          try:
            print("█", end='')
          except:
            print("O", end='')
          # end try
        elif self.matrix[i][j] == -1:
          print("-", end='')
        # end if
      # end for
      print("")
    # end for
  # end def

  # --------------------------------------
  # saveNonogram: Saves the nonogram in a binary P5 pgm image
  #   params:
  #    fileName: Name of the file where is to save the image
  # -------------------------------------- 
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
          # end if
        # end for
        newFileByteArray = bytearray(vals)
        file.write(newFileByteArray)
      # end for
    # end with
  # end def
# end class

# --------------------------------------
# --------------------------------------
# CLASS: NONOGRAM SOLVER
#  Class with static methods that solve a given Nonogram
# --------------------------------------
# -------------------------------------- 
class NonogramSolver:
  
  # -------------------------------------- 
  # solveNonogram: Facade method to solve a nonogram
  #   params:
  #    nonogram: Object of type Nonogram containing the nonogram info
  #   return:
  #    ( result, nono ): Pair containing the final state of the nonogram and 
  #                      whether it has been solved or not  
  # -------------------------------------- 
  def solveNonogram( nonogram ):    
    nono = Nonogram()
    nono.matrix = nonogram.matrix.copy()
    nono.rows = nonogram.rows.copy()
    nono.columns = nonogram.columns.copy()
    for i in range(len(nono.rows)):
      nono.rows[i].append({"num" : 0, "mark" : False, "painted" : 0})
    # end for
    for i in range(len(nono.columns)):
      nono.columns[i].append({"num" : 0, "mark" : False, "painted" : 0})
    # end for
    row_idx = [0]*(len(nono.rows))
    col_idx = [0]*(len(nono.columns))
    result =  NonogramSolver.solveNonogram_Aux( nono, 0, 0, row_idx ,col_idx )
    return(nono, result)
  # end def

  # -------------------------------------- 
  # finishedNonogram: Validates whether a nonogram has been solved or not.
  #                   Checks if all cells have been painted or marked and if
  #                   all row and col numbers are 0
  #   params:
  #    nonogram: Nonogram to evaluate
  #   return: 
  #    boolean indicating if the nonogram is finished (True) or not (False).
  # -------------------------------------- 
  def finishedNonogram( nonogram ):
    for row in nonogram.matrix:
      for item in row:
        if item == 0:
          return False
        # end if
      # end for
    # end for
    for row in nonogram.rows:
      for item in row:
        if item["num"] != 0:
          return False
        # end if
      # end for
    # end for
    for col in nonogram.columns:
      for item in col:
        if item["num"] != 0:
          return False
        # end if
      # end for
    # end for
    return True
  # end def

  # -------------------------------------- 
  # toPaintValid: Method that validates if it's valid to paint the (i,j) cell given
  #               the current state of the game.
  #   params:
  #    nonogram: Nonogram to validate
  #    i, j: Coordinates of the to-paint cell
  #    row_idx: List containing the index of the current analyzed number in the rows.
  #    col_idx: List containing the index of the current analyzed number in the columns.
  #   return:
  #    boolean indicating if it's valid to paint that cell (True) or not (False).
  # --------------------------------------  
  def toPaintValid( nonogram, i, j, row_idx, col_idx ):
    if nonogram.rows[i][row_idx[i]]["num"] > 0 and nonogram.columns[j][col_idx[j]]["num"] > 0:
      return True
    else:
      return False
    # end if
  # end def

  # -------------------------------------- 
  # toMarkValid: Method that validates if it's valid to mark the (i,j) cell given
  #              the current state of the game.
  #   params:
  #    nonogram: Nonogram to validate
  #    i, j: Coordinates of the to-mark cell
  #    row_idx: List containing the index of the current analyzed number in the rows.
  #    col_idx: List containing the index of the current analyzed number in the columns.
  #   return:
  #    boolean indicating if it's valid to mark that cell (True) or not (False).
  # --------------------------------------  
  def toMarkValid(nonogram, i, j, row_idx, col_idx):
    if nonogram.rows[i][row_idx[i]]["num"] == 0 or nonogram.columns[j][col_idx[j]]["num"] == 0:
      return True
    else:
      return False
    # end if
  # end def
    
  # -------------------------------------- 
  # solveNonogram_Aux: Recursive method that tries to solve the nonogram. It first validates
  #                    if the game has been solved. If not it tries either to paint it or to
  #                    mark it, checking invalidation of the matrix at several moments.
  #   params:
  #    nonogram: Nonogram to validate
  #    i, j: Coordinates of the analyzed cell
  #    row_idx: List containing the index of the current analyzed number in the rows.
  #    col_idx: List containing the index of the current analyzed number in the columns.
  #   return:
  #    boolean indicating if the nonogram has been solved given the current state.
  # --------------------------------------  
  def solveNonogram_Aux ( nonogram, i, j, row_idx, col_idx ):
    if NonogramSolver.finishedNonogram( nonogram ):
      print("Finished nonogram")
      return True
    elif 0 <= i < len(nonogram.rows) and 0 <= j < len(nonogram.columns):
      toValidPaint = NonogramSolver.toPaintValid( nonogram, i, j, row_idx, col_idx ) 
      valid = False
      if toValidPaint:
        nonogram.matrix[i][j] = 1
        nonogram.rows[i][row_idx[i]]["num"]  -= 1
        nonogram.columns[j][col_idx[j]]["num"] -= 1
        nonogram.rows[i][row_idx[i]]["painted"]  += 1
        nonogram.columns[j][col_idx[j]]["painted"] += 1
        valid = False
        n_ri = row_idx.copy()
        n_ci = col_idx.copy()
        if ( i + 1 ) >= len(nonogram.rows):
          valid = NonogramSolver.solveNonogram_Aux( nonogram, 0, j+1, n_ri, n_ci)
        else:
          valid = NonogramSolver.solveNonogram_Aux( nonogram, i+1, j, n_ri, n_ci)
        #end if

        if valid == False:
          nonogram.rows[i][row_idx[i]]["num"]  += 1
          nonogram.columns[j][col_idx[j]]["num"] += 1
          nonogram.rows[i][row_idx[i]]["painted"]  -= 1
          nonogram.columns[j][col_idx[j]]["painted"] -= 1          
        # end if
      # end if
      if not valid or not toValidPaint:        
        if not valid or NonogramSolver.toMarkValid( nonogram, i, j, row_idx, col_idx ):
          if (nonogram.rows[i][row_idx[i]]["num"] == 0) and \
            row_idx[i] < len(nonogram.rows[i]) - 1:
              row_idx[i] += 1
          # end if
          if nonogram.columns[j][col_idx[j]]["num"] == 0 and \
            col_idx[j] < len(nonogram.columns[j]) - 1:
              col_idx[j] += 1
          # end if
          if nonogram.rows[i][row_idx[i]]["num"] != 0 and \
               nonogram.rows[i][row_idx[i]]["painted"] > 0 and \
                row_idx[i] < len(nonogram.rows[i]) - 1:
              return False
          # end if
          if nonogram.columns[j][col_idx[j]]["num"] != 0 and \
              nonogram.columns[j][col_idx[j]]["painted"] > 0 and \
                col_idx[j] < len(nonogram.columns[j]) - 1:
              return False
          # end if
          validMark = False
          nonogram.matrix[i][j] = -1
          n_ri = row_idx.copy()
          n_ci = col_idx.copy()
          if ( i + 1 ) >= len(nonogram.rows):
            validMark = NonogramSolver.solveNonogram_Aux( nonogram, 0, j+1, n_ri, n_ci)
          else:
            validMark = NonogramSolver.solveNonogram_Aux( nonogram, i+1, j, n_ri, n_ci)
          # end if
          return validMark
        # end if
        return False
      # end if
      return valid
    else:
      return False
    # end if
  # end def
# end class

# -------------------------------------- 
# -- TEST --
# -------------------------------------- 
if len(sys.argv) != 3:
  print("Error. Usage:",sys.argv[0],"inFile outFile")
  exit()
# end if

nono = Nonogram(sys.argv[1])
nono.printColsRows()
print("Size:",len(nono.rows),"x", len(nono.columns))
print("Solving")
result = NonogramSolver.solveNonogram( nono )
if result[1]:
  print("Solved!")
  nono.saveNonogram(sys.argv[2])
  nono.printColsRows()
  print("Image saved to:", sys.argv[2])
else:
  print("Unsolvable! Check entries.")
# end if

# eof - NonogramSolver.py
