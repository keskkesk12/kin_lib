import math
import numpy as np
import cv2


class Robot:
    def __init__(self):
        self.link_list = list()
        self.transformation_list = list()
        self.concatenated_transformation_list = list()
        self.frame_position_list = list()
        self.tool_frame = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
        self.base_frame = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])

    def setTool(self, _frame):
        self.tool_frame = _frame

    def setBase(self, _frame):
        self.base_frame = _frame

    def appendLink(self, _link):
        self.link_list.append(_link)

    def updateLinkVariables(self):
        n = 1
        for link in self.link_list:
            link.setVariable(cv2.getTrackbarPos(str(n), 'Robot'))
            n += 1

    def generateTransformationList(self):
        self.transformation_list = list()
        self.transformation_list.append(self.base_frame)
        for link in self.link_list:
            self.transformation_list.append(link.generateTransformation())
        self.transformation_list.append(self.tool_frame)

    def printTransformationList(self):
        print("transformation_list")
        for transformation in self.transformation_list:
            print(transformation)

    def printConcatenatedTransformations(self):
        for transformation in self.concatenated_transformation_list:
            print(transformation)

    def generateConcatenatedTransformations(self):
        self.concatenated_transformation_list = list()
        temp_transformation = np.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
        for transformation in self.transformation_list:
            temp_transformation = np.matmul(temp_transformation, transformation)
            self.concatenated_transformation_list.append(temp_transformation)

    def initDisplay(self):
        cv2.namedWindow('Robot')
        cv2.resizeWindow('Robot', 400, 400)
        n = 1
        for link in self.link_list:
            cv2.createTrackbar(str(n), 'Robot', int(link.max/2), int(link.max), nothing)
            n += 1

    def generateFramePositions(self):
        self.frame_position_list = list()
        self.frame_position_list.append(FramePosition())

        for transformation in self.concatenated_transformation_list:
            temp_pos = FramePosition()
            temp_pos.world_origin = np.matmul(transformation, temp_pos.world_origin)
            temp_pos.world_x = np.matmul(transformation, temp_pos.world_x)
            temp_pos.world_y = np.matmul(transformation, temp_pos.world_y)
            temp_pos.world_z = np.matmul(transformation, temp_pos.world_z)
            self.frame_position_list.append(temp_pos)

    def printFrameOrigins(self):
        n = 0
        for origin in self.frame_position_list:
            print(n)
            n+=1
            print(origin.world_origin)

    def display(self):
        xz_image = self.__drawImage((0, 1), True)
        yz_image = self.__drawImage((2, 1), False)
        image = np.hstack((xz_image, yz_image))
        cv2.imshow('Robot', image)

    def __drawCoordinateSystem(self, _image, _FramePosition):
        origin_x = _FramePosition.world_origin[0]
        origin_y = _FramePosition.world_origin[1]
        origin_z = _FramePosition.world_origin[2]
        frame_thickness = 3
        #Draw x
        temp_image = cv2.line(_image, drawTransformation((origin_x, origin_y)), drawTransformation((_FramePosition.world_x[0], _FramePosition.world_x[1])), (0, 0, 255), thickness=frame_thickness)
        #Draw y
        temp_image = cv2.line(_image, drawTransformation((origin_x, origin_y)), drawTransformation((_FramePosition.world_y[0], _FramePosition.world_y[1])), (0, 255, 0), thickness=frame_thickness)
        #Draw z
        temp_image = cv2.line(_image, drawTransformation((origin_x, origin_y)), drawTransformation((_FramePosition.world_z[0], _FramePosition.world_z[1])), (255, 0, 0), thickness=frame_thickness)
        return temp_image

    def __drawImage(self, selection, drawBool):
        temp_image = np.zeros(shape=[window_dimensions[0], window_dimensions[1], 3], dtype=np.uint8)
        for i in range(len(self.frame_position_list)):
            if i < len(self.frame_position_list)-1:
                this_x = self.frame_position_list[i].world_origin[selection[0]]
                this_y = self.frame_position_list[i].world_origin[selection[1]]
                next_x = self.frame_position_list[i+1].world_origin[selection[0]]
                next_y = self.frame_position_list[i+1].world_origin[selection[1]]
                #temp_image = cv2.line(temp_image, drawTransformation((this_x, this_y)), drawTransformation((next_x, next_y)), ((50+30*i)%255, (50+50*i)%255, 0), thickness=3)
                temp_image = cv2.line(temp_image, drawTransformation((this_x, this_y)), drawTransformation((next_x, next_y)), (255, 255, 255), thickness=2)
                if drawBool:
                    temp_image = self.__drawCoordinateSystem(temp_image, self.frame_position_list[i])
        return temp_image

class Link:
    def generateTransformation(self):
        screw_x = np.array([[1, 0, 0, self.a],
                            [0, math.cos(self.alpha), -math.sin(self.alpha), 0],
                            [0, math.sin(self.alpha), math.cos(self.alpha), 0],
                            [0, 0, 0, 1]])
        
        screw_z = np.array([[math.cos(self.theta), -math.sin(self.theta), 0, 0],
                            [math.sin(self.theta), math.cos(self.theta), 0, 0],
                            [0, 0, 1, self.d],
                            [0, 0, 0, 1]])
        return np.matmul(screw_x, screw_z)

class Prismatic(Link):
    def __init__(self, _alpha, _a, _theta, _min = 0, _max = 200, _default = 100):
        self.alpha = _alpha
        self.a = _a
        self.d = _default
        self.theta = _theta
        self.min = _min
        self.max = _max

    def getVariable(self):
        return self.d

    def setVariable(self, _d):
        self.d = _d

class Revolute(Link):
    def __init__(self, _alpha, _a, _d, _min = 0, _max = 360, _default = 0):
        self.alpha = _alpha
        self.a = _a
        self.d = _d
        self.theta = _default
        self.min = _min
        self.max = _max

    def getVariable(self):
        return self.theta

    def setVariable(self, _theta):
        self.theta = math.radians(_theta - self.max/2)

class FramePosition:
    def __init__(self):
        self.world_origin = np.array([[0],
                                      [0],
                                      [0],
                                      [1]])
        self.world_x = np.array([[30],
                                 [0],
                                 [0],
                                 [1]])
        self.world_y = np.array([[0],
                                 [30],
                                 [0],
                                 [1]])
        self.world_z = np.array([[0],
                                 [0],
                                 [30],
                                 [1]])

def nothing(x):
    pass

def drawTransformation(coordinate):
    y = int(window_dimensions[0] - coordinate[1])
    x = int(window_dimensions[1]/2 + coordinate[0])
    return (x, y)

def main():
    my_robot = Robot()

    my_robot.appendLink(Revolute(math.radians(-90), 0, 0))
    my_robot.appendLink(Revolute(math.radians(90), 0, 0))
    my_robot.appendLink(Revolute(math.radians(-90), 200, 0))
    my_robot.appendLink(Revolute(math.radians(90), 200, 0))
    my_robot.appendLink(Revolute(math.radians(-90), 200, 0))
    my_robot.appendLink(Revolute(math.radians(90), 100, 0))
    
    base_frame = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 100],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

    tool_frame = np.array([[1, 0, 0, 100],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])

    my_robot.setBase(base_frame)
    my_robot.setTool(tool_frame)

    my_robot.initDisplay()

    global window_dimensions
    window_dimensions = (900, 1000)#(y, x)

    while(1):
        my_robot.updateLinkVariables()
        my_robot.generateTransformationList()
        my_robot.generateConcatenatedTransformations()
        my_robot.generateFramePositions()
        my_robot.display()

        key = cv2.waitKey(25)
        if key == 27:
            # ESC will terminate the program 
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()