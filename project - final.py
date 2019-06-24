from visual import*
from visual.graph import*
from random import*
from mag_force import*
 
N = 3  ##3*3 magnet
mass = 1
size = 0.1
space = 4*size
length = 1.0
m =0
k = 1E5
g = vector(0.0, -9.8, 0.0)
theta = 60
thetaa = 45
f = 0.2
pos_initial = length*vector(sin(theta*pi/180.)*sin(thetaa*pi/180.), -cos(theta*pi/180.), -sin(theta*pi/180.)*cos(thetaa*pi/180.))
mags = []
 
scene = display(width=800, height=800, center=(0, -0.5, 0), background=(0.5, 0.5, 0), forward=vector(0, -1, 0))
string = cylinder(radius=0.006)
#ceiling = box(length=3, height=0.001, width=3, color=color.blue)
ball = sphere(radius=0.5*size, color=color.red)
 
#
 
resultlist = []
results = ghistogram(bins=arange(0.5,9.5), color=color.red)
results.plot(data=resultlist)
 
 
#
cnt=[]
for i in range(10):
    cnt.append(0)
 
ball.pos = pos_initial
ball.v = vector(0, 0, 0)
ball.a = vector(0, 0, 0)
 
string.pos = vector(0, 0, 0)
string.axis = ball.pos - string.pos
 
for i in range(N):
    for j in range(N):
        mag = cylinder(radius=size, color=color.green)
        if(i==1 and j==1):mag.pos = vector((0.5*(N-1)-j)*space, -(length+size*1), (0.5*(N-1)-i)*space)
        elif((i==0 and(j==0 or j==2)) or (i==2 and(j==0 or j==2))): mag.pos=vector((0.5*(N-1)-j)*space, -(length+size*1), (0.5*(N-1)-i)*space)
        else:mag.pos = vector((0.5*(N-1)-j)*space, -(length+size), (0.5*(N-1)-i)*space)
        mag.axis = vector(0, -size, 0)
        mags.append(mag)
 
for i in range(N**2):
    magnet_pos_list.append(mags[i].pos)
 
def tforce(r):
    return -k*(r-length)*norm(string.axis)
 
def initialize():
    ball.pos = length*vector(sin(theta*pi/180.)*sin(thetaa*pi/180.), -cos(theta*pi/180.), -sin(theta*pi/180.)*cos(thetaa*pi/180.))
    ball.v = vector(0.0, 0.0, 0.0)
    ball.a = vector(0.0, 0.0, 0.0)
 
def territory(meow):
    m = 0
    n = 0
   
    if meow.z <= (-space)*0.75 :
        m = 1
    if meow.z > (-space)*0.25 and meow.z <= space*0.25:
        m = 2
    if meow.z > space*0.75:
        m = 3
 
    if meow.x <= -space*0.75 :
        n = 1
    if meow.x > -space*0.25 and meow.x <= space*0.25:
        n = 2
    if meow.x > space*0.75:
        n = 3
    if(m!=0 and n!=0) : return 3*(m-1)+n
    else : return 0
 
dt = 0.001
t = 0.0
b = 0
pt = 0
times=1
booli =1
while times<=100:
    a=0
    thetaa=45+random()-0.5
    print 'Try= ', times
    print 'initial angle= ' ,thetaa
    initialize()
    while True:
        rate(10000)
        t += dt
        a += 1
        ball.a = tforce(abs(string.axis))/mass + g - f*ball.v
        ball.a += mag_force(string.axis, ball.pos)/mass
        #print mag_force(string.axis, ball.pos)
        ball.v += ball.a*dt
        ball.pos += ball.v*dt
        string.axis = ball.pos - string.pos
        if a%100==0:
            if territory(ball.pos) == pt and pt!=0 : b += 1
            else:
                pt = territory(ball.pos)
                b = 0
        string.axis = ball.pos - string.pos
        if b == 10:
            b = 0
            print 'stable state= ', pt
            print'------------------------------'
            resultlist.append(pt)
            results.plot(data=resultlist)
            #cnt[pt]+=1
            break
        if(ball.pos.y>0):
            booli=0
            break
    if(booli==0):
        booli=1
        times-=1
    times+=1
