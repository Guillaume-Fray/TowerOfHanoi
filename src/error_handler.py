#!/usr/bin/env python

import rospy
import message_filters
from artiesans.msg import gamePositions, correctMove
from std_msgs.msg import Bool

reset = False
def setReset(data):
    reset = not data.data
    

def copy(l):
    ans = []
    for n in l:
        sub = []
        for i in n:
            sub.append(i)
        ans.append(sub)
    return ans

def callback(data):
    global positions

    if(reset):
        positions = []
        positions.append([4, 3, 2, 1])
        positions.append([])
        positions.append([])
    else:
        newPositions = [data.first, data.second, data.third]
        newPositions = copy(newPositions)
    
        ans = correctMove()

        ans.moreThanOne = False
        ans.biggerOnTop = False
        ans.oneLess = False

        publisher = rospy.Publisher('errors', correctMove)

        if(positions != newPositions):

            ans.oneLess = len(positions[0]) + len(positions[1]) + len(positions[2]) - len(newPositions[0]) - len(newPositions[1]) - len(newPositions[2]) == 1

            ans.moreThanOne = not ans.oneLess
            ans.biggerOnTop = False

            for n in range(len(positions)):
                if(len(positions[n]) > 0):
                    for i in range(1, 3):
                        buffer = copy(positions)
                        buffer[(n + i) % 3].append(buffer[n].pop())
                        #print(buffer, newPositions)
                        if(newPositions == buffer):
                            ans.moreThanOne = False
                            if(len(buffer[(n + i) % 3]) > 1 and buffer[(n + i) % 3][len(buffer[(n + i) % 3]) - 1] > buffer[(n + i) % 3][len(buffer[(n + i) % 3]) - 2]):
                                ans.biggerOnTop = True
    
            if(not(ans.moreThanOne or ans.biggerOnTop or ans.oneLess)): positions = newPositions
    
    
        print(ans)
        print(positions)
        publisher.publish(ans)
    
    
sub1 = rospy.Subscriber('board',gamePositions,callback)
sub2 = rospy.Subscriber('/artiesans/facedetection',Bool,setReset)

positions = []
positions.append([3, 2, 1])
positions.append([])
positions.append([])

if __name__ == '__main__':
    rospy.init_node('game_algorithm', anonymous=True)
    rospy.spin()
