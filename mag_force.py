from visual import*
from random import random
from visual.graph import*
 
magnet_pos_list=[]
dipole_magnet_fixed=300.
dipole_magnet_pendulum=300.
length_of_pendulum = 1.
direction_of_pendulum = vector(1,1,1)  ## = "pendulum.axis"
 
## first part: magnetic field
 
 
m0 = vector(0,1,0)*dipole_magnet_fixed     ## fixed
m = vector(0,1,0)*dipole_magnet_pendulum     ## pendulum

c0=1.0/10000000
 
def B_field_single(r0,r):
    r_rel=r-r0
    ans = c0*(3*r_rel*dot(m0,r_rel)/(abs(r_rel) ** 5) - m0/(abs(r_rel) ** 3))
    return ans
 
def B(r):
    B_total = vector(0,0,0)
    for i in magnet_pos_list:
        B_total += B_field_single(i,r)
    return B_total
 
def mag_potential(tmpp, r):
    m = (-1)* tmpp.norm() * dipole_magnet_fixed
    return dot(m,B(r))
 
def mag_force(tmp, r):
    rx = r.x
    ry = r.y
    rz = r.z
    dr = length_of_pendulum/500
    fx = (mag_potential(tmp, vector(rx+dr,ry,rz))-mag_potential(tmp, vector(rx-dr,ry,rz)))/(2*dr) * 3/4
    fx += (mag_potential(tmp, vector(rx+2*dr,ry,rz))-mag_potential(tmp, vector(rx-2*dr,ry,rz)))/(4*dr) * 1/4
    fy = (mag_potential(tmp, vector(rx,ry+dr,rz))-mag_potential(tmp, vector(rx,ry-dr,rz)))/(2*dr) * 3/4
    fy += (mag_potential(tmp, vector(rx,ry+2*dr,rz))-mag_potential(tmp, vector(rx,ry-2*dr,rz)))/(4*dr) * 1/4
    fz = (mag_potential(tmp, vector(rx,ry,rz+dr))-mag_potential(tmp, vector(rx,ry,rz-dr)))/(2*dr) * 3/4
    fz += (mag_potential(tmp, vector(rx,ry,rz+2*dr))-mag_potential(tmp, vector(rx,ry,rz-2*dr)))/(4*dr) * 1/4
    return vector(fx,fy,fz)
