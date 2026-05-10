# -*- coding: utf-8 -*-
"""
@Project: LinalgDat2022
@File: GaussExtensions.py

@Description: Project B Gauss extensions

"""

import math

from sys import path
path.append('../Core')
from Vector import Vector
from Matrix import Matrix

def AugmentRight(A: Matrix, v: Vector) -> Matrix:
    """
    Create an augmented matrix from a matrix and a vector.

    This function creates a new matrix by concatenating matrix A
    and vector v. See page 12 in "Linear Algebra for Engineers and
    Scientists", K. Hardy.

    Parameters:
         A: M-by-N Matrix
         v: M-size Vector
    Returns:
        the M-by-(N+1) matrix (A|v)
    """
    M = A.M_Rows
    N = A.N_Cols
    if v.size() != M:
        raise ValueError("number of rows of A and length of v differ.")

    B = Matrix(M, N + 1)
    for i in range(M):
        for j in range(N):
            B[i, j] = A[i, j]
        B[i, N] = v[i]
    return B


def ElementaryRowReplacement(A: Matrix, i: int, m: float, j: int) -> Matrix:
    """
    Replace row i of A by row i of A + m times row j of A.

    Parameters:
        A: M-by-N Matrix
        i: int, index of the row to be replaced
        m: float, the multiple of row j to be added to row i
        j: int, index or replacing row.
    Returns:
        A modified in-place after row replacement.
    """
    N = A.N_Cols
    for n in range(N):
        A[i,n] = A[i,n] + m * A[j,n]
    return A

def ElementaryRowInterchange(A: Matrix, i: int, j : int) -> Matrix:
    """
    Interchange row i and row j of A.

    Parameters:
        A: M-by-N Matrix
        i: int, index of the first row to be interchanged
        j: int, index the second row to be interchanged.

    Returns:
        A modified in-place after row interchange
    """
    N = A.N_Cols
    for n in range(N):
        A[i,n], A[j,n] = A[j,n], A[i,n]
    return A


def ElementaryRowScaling(A: Matrix, i: int, c: float) -> Matrix:
    """
    Replace row i of A c * row i of A.

    Parameters:
        A: M-by-N Matrix
        i: int, index of the row to be replaced
        c: float, the scaling factor

    Returns:
        A modified in-place after row scaling.
    """
    N = A.N_Cols
    for n in range(N):
        A[i,n] = c * A[i,n]
    return A


def ForwardReduction(A: Matrix) -> Matrix:
    """
    Forward reduction of matrix A.

    This function performs the forward reduction of A provided in the
    assignment text to achieve row echelon form of a given (augmented)
    matrix.

    Parameters:
        A:  M-by-N augmented matrix
    returns
        M-by-N matrix which is the row-echelon form of A (performed in-place,
        i.e., A is modified directly).
    """
    N = A.N_Cols
    M = A.M_Rows

    for nuRække in range(M):
        j = None # j er pivot kolonnen
        pivotRække = None

        for n in range(N):
            for m in range(nuRække, M):
                if A[m,n] != 0.0:
                    j = n
                    pivotRække = m
                    break # ud af nuRække til M loopet
            if j != None:
                break # ud af 0 til N loopet 
        
        # Sand hvis der kun er nul-kolonner tilbage.
        if j == None: 
            break

        # Byt pivoten op øverst i sub Matricen
        if nuRække != pivotRække:
            A = ElementaryRowInterchange(A, nuRække, pivotRække)        

        for i in range(nuRække + 1, M):
            if A[i, j] != 0.0:
                c = -A[i,j]/A[nuRække,j]
                A = ElementaryRowReplacement(A,i,c,nuRække)
    
    return A
        
def BackwardReduction(A: Matrix) -> Matrix:
    """
    Backward reduction of matrix A.

    This function performs the forward reduction of A provided in the
    assignment text given a matrix A in row echelon form.

    Parameters:
        A:  M-by-N augmented matrix in row-echelon form
    returns
        M-by-N matrix which is the reduced form of A (performed in-place,
        i.e., A is modified directly).
    """
    N = A.N_Cols
    M = A.M_Rows

    for i in range(M -1, -1, -1):
        pivotCol = None
        
        for j in range(N):
            if A[i,j] != 0.0:
                pivotCol = j
                break

        if pivotCol == None:
            continue

        if A[i,pivotCol] != 1:
            ElementaryRowScaling(A, i, 1/A[i,pivotCol])

        for n in range(i-1,-1,-1):
            if A[n,pivotCol] != 0.0:
                c = -A[n, pivotCol]

                A = ElementaryRowReplacement(A,n,c,i)

    return A


def GaussElimination(A: Matrix, v: Vector) -> Vector:
    """
    Perform Gauss elimination to solve for Ax = v.

    This function performs Gauss elimination on a linear system given
    in matrix form by a coefficient matrix and a right-hand-side vector.
    It is assumed that the corresponding linear system is consistent and
    has exactly one solution.

    Hint: combine AugmentRight, ForwardReduction and BackwardReduction!

    Parameters:
         A: M-by_N coefficient matrix of the system
         v: N-size vector v, right-hand-side of the system.
    Return:
         M-size solution vector of the system.
    """
    totalMatrice = AugmentRight(A, v)
    
    rækkeEchelonForm = ForwardReduction(totalMatrice)
    
    reduceretRækkeEchelonForm = BackwardReduction(rækkeEchelonForm)
    
    M = reduceretRækkeEchelonForm.M_Rows
    solution = Vector(M)
    for i in range(M):
        solution[i] = reduceretRækkeEchelonForm[i, reduceretRækkeEchelonForm.N_Cols - 1]
    
    return solution
