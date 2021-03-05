'''
Socket Programming Question:[Note: This program will be an extension of single client-server program which was done in lab evaluation-1, including 2 clients. Code Template in java for Multi client and a single server can be taken from the socket programming file which I have already sent.]

Develop a multi-threaded guessing game using socket programming. The  server  should  be  able  to  accept  multiple  connections(minimum of 3).  For  each  connection,  the  server generates  a  random  number  between  1  and  100.  This  number  is  not  disclosed  to  the  client. The goal of the client is to guess this random number within 6 tries. The client guesses a number. The server must respond with “The number is too high”, “The number is too low” for each try. If the client guesses the number within 6 tries, the server must return “Correct Answer” to the respective client and a score is calculated as follows. Else, it must return “Failed to guess the number. The correct number is <number>”. 
If client guesses the number correctly between

1-3 tries 🡪 score of 5 is assigned
4-6 🡪 score of 3 is assigned
>6 🡪 score of 0 is assigned

Play this game for a minimum of 6 times. After each round, the player number and the cumulative score should be displayed to each of the client by the server. At the end of the game, the final score board with player number, score and their position should be displayed at each of the client .

Final score board sample

Player 	score 	position
Player1	30	1
Player2	10	3
Player 3	20	2




For the evaluation demonstration, the minimum requirement is to show one server and two client connections. Otherwise, the code will not be evaluated.
'''

#server program ---------------------------------------------------------------------------------------------------------------------
import socket
import random

s=socket.socket()

s.bind(('localhost',10999))
s.listen(3)

count=0
countn=0
time =0 
player_id=dict()

c,address=s.accept()

ans=c.recv(1024).decode()

while(ans=="y"):
    #print("entered")
    id=c.recv(1024).decode()
    print("id of the number" ,id)
    
    n=random.randint(1,101)
    #print("random number",n)
    
    c.send(bytes("Guess the number",'utf-8'))
    num=int(c.recv(1024).decode())
    if(num==n):
        countn=1
    
    for i in range(1,6):
        if(num>n):
            c.send(bytes("Too high",'utf-8'))
            num=int(c.recv(1024).decode())
        if(num<n):
            c.send(bytes("Too low",'utf-8'))
            num=int(c.recv(1024).decode())
        if(num==n):
            c.send(bytes("You got it !!",'utf-8'))
            count=i
            break
        if(i==5 and count==0):
            c.send(bytes("You didnt get it !!",'utf-8'))
    if(countn==1):
        time=countn
    elif (count>0 and countn==0):
        time=i+1
    else:
        time=0
    if(1<=time<=3):
        if id in player_id.keys():
            player_id[id]+=5
        else:
            player_id[id]=5
    elif(4<=time<=6):
        if id in player_id.keys():
            player_id[id]+=3
        else:
            player_id[id]=3
    else:
        if id in player_id.keys():
            player_id[id]+=0
        else:
            player_id[id]=0
            
    
    ans=c.recv(1024).decode()
    #print(ans)

sort=sorted(player_id.items(),key=lambda x:x[1], reverse=True)
h=1
print("position - player_id - score")
for i in sort:
    print(h," - ",i[0]," - ",i[1])
    h+=1

c.close()



#client program --------------------------------------------------------------------------------------------------
import socket

c=socket.socket()
c.connect(('localhost',10999))

print("do you want to play (y/n)?")
ans=input()
c.send(bytes(ans,'utf-8'))
while(ans=="y"):
    print("give your player id")
    id=input()
    c.send(bytes(id,'utf-8'))
    
    str_n=c.recv(1024).decode()
    print(str_n)
    num=input()
    c.send(bytes(num,'utf-8'))
    str_n=c.recv(1024).decode()
    while(str_n!="You got it !!" and str_n!="You didnt get it !!"):
        print(str_n)
        num=input()
        c.send(bytes(num,'utf-8'))
        str_n=c.recv(1024).decode()
    print(str_n)
    
    print("do you want to continue the game ? ")
    ans=input()
    c.send(bytes(ans,'utf-8'))
