#!/usr/bin/env python

import rospy
import message_filters
from artiesans.msg import gamePositions, uint8Array
from std_msgs.msg import String

amountOfRings = 3

def place(positions, ringSize, pole):
    n = 0
    ans = 0
    while(n < len(positions[pole]) and positions[pole][n] > ringSize): n += 1
    if(n != len(positions[pole])): ans = positions[pole][n]

    return ans

def nextMove(positions, ringSize = amountOfRings, targetPole = 2):
    ans = [3, 3]
    for pole in range(len(positions)):
        finished = True
        for ring in range(len(positions[pole])):
            if(positions[pole][ring] == ringSize):
                if(pole != targetPole):
                    if(targetPole == (pole + 1) % len(positions)): other = (pole + 2) % len(positions)
                    else: other = (pole + 1) % len(positions)

                    p = place(positions, ringSize, targetPole)
                    if(p != 0 and(ring == len(positions[pole]) - 1 or positions[pole][ring + 1] < p)):
                        ans = nextMove(positions, ringSize = p, targetPole = other)

                    elif(ring < len(positions[pole]) - 1):
                        ans = nextMove(positions, ringSize = positions[pole][ring + 1], targetPole = other)
                    elif(ring == len(positions[pole]) - 1):
                        ans = [pole, targetPole]

                elif(ringSize > 1): ans = nextMove(positions, ringSize = ringSize - 1, targetPole = targetPole)



                break
        else: finished = False

        if(finished): break
    print(ans)
    return ans


def callback(data):
    publisher = rospy.Publisher('move', uint8Array)

    board = []
    board.append(data.first)
    board.append(data.second)
    board.append(data.third)

    ans = nextMove(board)

    publisher.publish(ans)


sub = rospy.Subscriber('board',gamePositions,callback)

if __name__ == '__main__':
    rospy.init_node('game_algorithm', anonymous=True)
    rospy.spin()
