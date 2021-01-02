from matplotlib import pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3
from matplotlib import animation

fig = plt.figure()
ax = p3.Axes3D(fig)

def genxy(n,fx,fy,fxc=0,fyc=0):
    phi = 0
    sk = 0
    while phi < 360:
        yield np.array([fx*np.cos(phi)+fxc, fy*np.sin(phi)+fyc,phi])
        phi += 36*5/n

def update(num, data, line):
    line.set_data(data[:2,num-200 :num]) #描画区間を制限する
    line.set_3d_properties(data[2,num-200 :num])

N = 960
datay = np.array(list(genxy(N,fx=0,fy=1,fxc=-2,fyc=0))).T
liney, = ax.plot(datay[0, 0:1], datay[1, 0:1], datay[2, 0:1])
datax = np.array(list(genxy(N,fx=1,fy=0,fxc=0,fyc=2))).T
linex, = ax.plot(datax[0, 0:1], datax[1, 0:1], datax[2, 0:1])
dataz = np.array(list(genxy(N,fx=1,fy=1,fxc=0,fyc=0))).T
linez, = ax.plot(dataz[0, 0:1], dataz[1, 0:1], dataz[2, 0:1])

# Setting the axes properties
ax.set_xlim3d([-2.0,2.0])
ax.set_xlabel('X')

ax.set_ylim3d([-2.0, 2.0])
ax.set_ylabel('Y')

ax.set_zlim3d([36.0, 80.])
ax.set_zlabel('Z')

frames =36
s=180
for n in range(frames):
    s+=1
    num = s%800+200
    update(num,datax,linex)
    update(num,datay,liney)
    update(num,dataz,linez)
    plt.pause(0.001)

from PIL import Image,ImageFilter
images = []
for n in range(frames):
    exec('a'+str(n)+'=Image.open("./'+str(n)+'.png")')
    images.append(eval('a'+str(n)))
images[0].save('./sin_wave_el{}_az{}.gif'.format(0, 0),
               save_all=True,
               append_images=images[1:],
               duration=100,
               loop=0)    
