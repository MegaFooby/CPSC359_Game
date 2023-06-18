write = open('enemy_movement3.data', 'w')

y = -50
x = 0
dx = 5
dy = 5
fire = 0
count = 0
#pattern 1 test
'''while y < 1100:
    if y <= 0:
        dx = 0
    elif y < 300:
        dx = 7
    else:
        dx = 0
    if y == 0 or y == 300:
        fire = 1
    y += dy
    string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
    write.write(string)
    fire = 0
    count += 1'''

#pattern 2
'''for i in range(40):
    y += dy
    string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
    write.write(string)
    fire = 0
    count += 1
dy = 0
for i in range(100):
    if i % 10 == 0:
        fire = 1
    string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
    write.write(string)
    fire = 0
    count += 1
dy = 5
while y < 1100:
    y += dy
    string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
    write.write(string)
    fire = 0
    count += 1'''

#pattern 3
x = -100
while y < 1100:
    dx = 7
    dy = 2
    while x <= 1000:
        x += dx
        y += dy
        if x == 96 or x == 194 or x == 292 or x == 390 or x == 488 or x == 586 or x == 684 or x == 782:
            fire = 1
        string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
        write.write(string)
        fire = 0
        count += 1
    dy = -9
    dx = 0
    for i in range(11):
        x += dx
        y += dy
        string = '0' + str(dx) + ' ' + str(dy) + ' ' + str(fire) + '\n'
        write.write(string)
        fire = 0
        count += 1
    dx = -7
    dy = 2
    while x >= -100:
        x += dx
        y += dy
        if x == 96 or x == 194 or x == 292 or x == 390 or x == 488 or x == 586 or x == 684 or x == 782:
            fire = 1
        string = str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
        write.write(string)
        fire = 0
        count += 1
    dy = -9
    dx = 0
    for i in range(11):
        x += dx
        y += dy
        string = '0' + str(dx) + ' ' + str(dy) + ' ' + str(fire) + '\n'
        write.write(string)
        fire = 0
        count += 1
'''for i in range(100):
   while( y < 1100):
       while(y <= 500):
            y += dy
            x += dx
            
            if (y == 450 or y == 300 or y ==250):
               fire =1
            string = str(dx)
            string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
            write.write(string)
            fire =0
           
       while(y >500):
            y -= dy
            x -= dx
            if (y == 550 or y == 600 or y ==750):
                fire =1
            string = str(dx)
            string = '0' + str(dx) + ' ' + '0' + str(dy) + ' ' + str(fire) + '\n'
            write.write(string)
            fire = 0 
        #if(x < 900):
            #y -= dy
            #if (y < 0):
                #x += dx'''


    
write.close()
print(count)
