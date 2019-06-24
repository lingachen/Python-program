from visual import*
from visual.graph import*
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
thetaa = 16

f = 0
pos_initial = length*vector(sin(theta*pi/180.)*sin(thetaa*pi/180.), -cos(theta*pi/180.), -sin(theta*pi/180.)*cos(thetaa*pi/180.))
mags = []

scene = display(width=800, height=800, center=(0, -0.5, 0), background=(0.5, 0.5, 0), forward=vector(0, -1, 0))
string = cylinder(radius=0.006)
#ceiling = box(length=3, height=0.001, width=3, color=color.blue)
ball = sphere(radius=0.5*size, color=color.red)
scene1 = display()
c = sphere(radius=0.001, color=color.red, display=scene1, make_trail=True)

ball.pos = pos_initial
ball.v = vector(0, 0, 0)
ball.a = vector(0, 0, 0)

string.pos = vector(0, 0, 0)
string.axis = ball.pos - string.pos

for i in range(N):
    for j in range(N):
        mag = cylinder(radius=size, color=color.green, display=scene)
        mag.pos = vector((0.5*(N-1)-j)*space, -(length+size), (0.5*(N-1)-i)*space)
        mag.axis = vector(0, -size, 0)
        mags.append(mag)

for i in range(N**2):
    if (i+1)%2==1:mags[i].pos.y += 0.5*size
    if (i+1)%5==0:mags[i].pos.y -= size
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
    
    if meow.z <= -space/2.0:
        m = 1
    if meow.z > -space/2.0 and meow.z <= space/2.0:
        m = 2
    if meow.z > space/2.0:
        m = 3

    if meow.x <= -space/2.0:
        n = 1
    if meow.x > -space/2.0 and meow.x <= space/2.0:
        n = 2
    if meow.x > space/2.0:
        n = 3
    return 3*(m-1)+n

dt = 0.001
t = 0.0
a = 0
b = 0
pt = 0

while thetaa<360:
    print thetaa
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
        c.pos=vector(ball.v.x, ball.v.y, ball.pos.x*ball.v.y - ball.pos.y*ball.v.x)
        if a%100==0:
            if territory(ball.pos) == pt:b += 1
            else:
                pt = territory(ball.pos)
                b = 0
        string.axis = ball.pos - string.pos
        if b == 100:
            b = 0
            print pt
            break
    thetaa+=1
    
