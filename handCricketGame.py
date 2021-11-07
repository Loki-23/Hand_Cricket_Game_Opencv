#assumptions
# 1. player always chooses head
# 2. pc always chooses tail
# 3. both chooses to bat on winning the toss


import cv2
import mediapipe as mp
import time
import random
import numpy as np


players_total=0
pc_total=0
players_score=[]
pc_score=[]

turn=0
count=0

a=['head',"tail"]
toss=random.choice(a)

pTime=0
cTime=0


def hand_cricket():
    global players_score, players_total, pc_total, pc_score, turn, a, count, toss,pTime,cTime
    players_total = 0
    pc_total = 0
    players_score = []
    pc_score = []

    turn = 0
    count = 0

    a = ['head', "tail"]
    toss = random.choice(a)

    cam=cv2.VideoCapture(0)

    mphands=mp.solutions.hands
    hands= mphands.Hands()
    mpdraw = mp.solutions.drawing_utils

    pTime=0
    cTime=0


    def restart(event, x, y, flag, param):
        if (event == cv2.EVENT_RBUTTONDOWN):
            if (x > 100 and x < 240 and y > 510 and y < 580):
                cv2.destroyAllWindows()
                hand_cricket()
            elif (x > 330 and x < 470 and y > 510 and y < 580):
                print("1")
                cv2.destroyAllWindows()


    def display_score(player_run, pc_run, turn):
        img = np.zeros((600, 600, 3), np.uint8)
        cv2.namedWindow("SCOREBOARD", cv2.WINDOW_NORMAL)
        cv2.rectangle(img, (50, 100), (550, 350), (255, 0, 0), 4)
        cv2.putText(img, "SCOREBOARD", (200, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255))
        if (turn == 0):
            cv2.putText(img, "Player is playing", (50, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (225, 1, 1))
        elif (turn == 1):
            cv2.putText(img, "pc is playing", (50, 80), cv2.FONT_HERSHEY_DUPLEX, 1, (225, 1, 1))
        cv2.putText(img, "Player", (110, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 0))
        cv2.putText(img, "COMPUTER", (350, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 0))
        cv2.line(img, (300, 100), (300, 350), (0, 200, 200), 3)
        cv2.putText(img, "{}".format(player_run), (90, 280), cv2.FONT_ITALIC, 4, (200, 130, 150), 4)
        cv2.putText(img, "{}".format(pc_run), (340, 280), cv2.FONT_ITALIC, 4, (200, 130, 150), 4)
        if (count >= 2):
            if(player_run==pc_run):
                cv2.putText(img, "DRAW", (200, 450), cv2.FONT_ITALIC, 2, (100, 150, 200), 3)
            else:
                cv2.putText(img, "Winner", (200, 450), cv2.FONT_ITALIC, 2, (100, 150, 200), 3)
                if (player_run > pc_run):
                    cv2.putText(img, "PLAYER", (180, 500), cv2.FONT_ITALIC, 2, (200, 100, 170), 3)
                elif (player_run < pc_run):
                    cv2.putText(img, "COMPUTER", (130, 500), cv2.FONT_ITALIC, 2, (200, 100, 170), 3)

            cv2.rectangle(img, (100, 510), (240, 580), (0, 0, 250), -1)
            cv2.rectangle(img, (330, 510), (470, 580), (0, 0, 250), -1)
            cv2.putText(img, "NEW GAME", (110, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.putText(img, "EXIT", (370, 550), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)
            cv2.setMouseCallback("SCOREBOARD", restart)
        cv2.imshow("SCOREBOARD", img)
    def game():

        global count,turn
        global players_total,pc_total,players_score,pc_score,cTime,pTime
        flag=0

        while True:
            check = 0
            success, img = cam.read()

            imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            lmlist = []
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id,lm in enumerate(handLms.landmark):
                        # print(id,lm )
                        h,w,c = img.shape
                        cx,cy= int(lm.x*w),int(lm.y*h)
                        # print(id,cx,cy)
                        lmlist.append([id,cx,cy])

                    mpdraw.draw_landmarks(img,handLms,mphands.HAND_CONNECTIONS)

            # Deciding who bats first
            if (toss == 'head' and count == 0):
                turn = 0
                # print("players bats first")
            elif (toss == "tail" and count == 0):
                turn = 1
                # print("pc bats first")
            display_score(players_total, pc_total, turn)
            # print corresponding gestures which are in their ranges
            if cv2.waitKey(10) == ord('p'):
                players_count = 0
                pc_count = 0

                l=[]
                if(len(lmlist)!=0):
                    if(lmlist[8][2]<lmlist[6][2]):
                        l.append(1)
                    else:
                        l.append(0)
                    if lmlist[12][2]<lmlist[10][2]:
                        l.append(1)
                    else:
                        l.append(0)
                    if lmlist[16][2]<lmlist[14][2]:
                        l.append(1)
                    else:
                        l.append(0)

                    if lmlist[20][2]<lmlist[18][2]:
                        l.append(1)
                    else:
                        l.append(0)

                    if lmlist[4][1]<lmlist[2][1]:
                        l.append(1)
                    else:
                        l.append(0)




                    if (l[0] == 0 and l[1] == 0 and l[2] == 0 and l[3] == 0 and l[4] == 0):
                        players_count=0
                        cv2.putText(img, '0', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

                    elif(l[0]==1 and l[1]==0 and l[2]==0 and l[3]==0 and l[4]==0):
                        players_count = 1
                        cv2.putText(img,'1',(0,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,255),2)

                    elif (l[0] == 1 and l[1] == 1 and l[2] == 0 and l[3] == 0 and l[4] == 0):
                        players_count = 2
                        cv2.putText(img, '2', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

                    elif (l[0] == 1 and l[1] == 1 and l[2] == 1 and l[3] == 0 and l[4] == 0):
                        players_count = 3
                        cv2.putText(img, '3', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

                    elif (l[0] == 1 and l[1] == 1 and l[2] == 1 and l[3] == 1 and l[4] == 0):
                        players_count = 4
                        cv2.putText(img, '4', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

                    elif (l[0] == 1 and l[1] == 1 and l[2] == 1 and l[3] == 1 and l[4] == 1):
                        players_count = 5
                        cv2.putText(img, '5', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)

                    elif (l[0] == 1 and l[1] == 0 and l[2] == 0 and l[3] == 1 and l[4] == 0):
                        players_count = 6
                        cv2.putText(img, '6', (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 2)
                    else:
                        check=1

                if check==0:
                    if turn==0 and count<2 :
                        pc_count=random.randint(0,6)
                        print("players_count : ", players_count)
                        print("pc_count : ", pc_count)
                        if players_count != pc_count:
                            players_score.append(players_count)
                            players_total += players_count
                            print("players total score:{}".format(players_total))
                            display_score(players_total, pc_total, turn)
                        else:
                            print("player is OUT")
                            turn = 1
                            count += 1
                            if (count == 1):
                                print("pc will play next")


                    elif turn==1 and count<2:
                        pc_count = random.randint(0, 6)
                        print("players_count : ",players_count)
                        print("pc_count : ",pc_count)
                        if players_count != pc_count :
                            pc_score.append(pc_count)
                            pc_total += pc_count
                            print("pc total score:{}".format(pc_total))
                            display_score(players_total, pc_total, turn)
                        else:
                            print("pc is OUT")
                            turn = 0
                            count += 1
                            if (count == 1):
                                print("player will play next")
                else:
                    print('No valid hand gesture is shown')
            if count>=2:
                if players_total>pc_total:
                    print('* * * * * * * * * * * *')
                    print('* * * Player wins * * *')
                    print('* * * * * * * * * * * *')
                    print("PLAYERS total score", players_total)
                    print("PC total score", pc_total)
                    print("PC's score in whole match",pc_score)
                    print("Players score in whole match",players_score)
                    display_score(players_total, pc_total,turn)
                    break

                elif(pc_total>players_total):
                    print('* * * * * * * * * * * *')
                    print('* * *   PC wins  * * *')
                    print('* * * * * * * * * * * *')
                    print("PC's score in whole match", pc_score)
                    print("PC total score",pc_total)
                    print("Players score in whole match", players_score)
                    print("PLAYERS total score",players_total)
                    display_score(players_total, pc_total,turn)
                    break
                else:
                    print('* * * * * * * * * * * *')
                    print('* * *   MATCH DRAW  * * *')
                    print('* * * * * * * * * * * *')
                    print("PC's score in whole match", pc_score)
                    print("PC total score", pc_total)
                    print("Players score in whole match", players_score)
                    print("PLAYERS total score", players_total)
                    display_score(players_total, pc_total, turn)



            # print(l)
            cTime=time.time()
            fps=1/(cTime-pTime)
            pTime=cTime
            cv2.putText(img,str(int(fps)),(530,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
            cv2.imshow("Image",img)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                flag = 1
                break

        cam.release()
        cv2.destroyAllWindows()
        if flag==0:
            display_score(players_total, pc_total,turn)

    def check(event,x,y,flag,param):
         if (event == cv2.EVENT_RBUTTONDOWN):
             if (x > 100 and x < 200 and y > 300 and y < 350):
                 cv2.destroyAllWindows()
                 game()
             elif (x > 300 and x < 400 and y > 300 and y < 350):
                 print("1")
                 cv2.destroyAllWindows()


    gameScreen= np.zeros((512,512,3),np.uint8)
    cv2.putText(gameScreen,"Hand Cricket",(50,100), cv2.FONT_HERSHEY_DUPLEX, 2, (255,0,0), 3)
    cv2.putText(gameScreen,"How to play:",(50,170),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,225),3)
    cv2.putText(gameScreen, "Put the hand in the box on the screen", (50, 200), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
    cv2.putText(gameScreen, "Press P to play ur move ", (50, 220), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225), 2)
    cv2.rectangle(gameScreen,(100,300),(200,350),(0,255,0),-1)
    cv2.putText(gameScreen,"start",(105,330), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
    cv2.rectangle(gameScreen,(300,300),(400,350),(0,0,255),-1)
    cv2.putText(gameScreen,"Exit",(315,330), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)
    cv2.namedWindow("GameScreen",cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("GameScreen", check)
    cv2.imshow("GameScreen", gameScreen)
    cv2.waitKey(0)

hand_cricket()