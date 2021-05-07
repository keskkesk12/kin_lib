from kin_lib import Matrix as mat
import kinematics_visualizer as kin_viz
import math
import numpy as np

def main():
    a = mat([[1, 1, 0, 1],
             [3, -1, 1, 2],
             [0, 0, 2, -3],
             [0, 0, -3, 0]])
    
    b = mat([[1],
             [4],
             [0],
             [2]])
    
    a.print()
    a.solve(b)
    b.print(8)
    
if __name__ == "__main__":
    main()