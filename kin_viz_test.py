import kinematics_visualizer as kv
import numpy as np



def main():
    for i in range(2):
        x = i%3
        y = (i+1)%3
        print(str(x) + " " + str(y))

if __name__ == "__main__":
    main()