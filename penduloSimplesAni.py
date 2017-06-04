#_*_ coding: utf-8 _*_
#!/usr/bin/env python

import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import animation


#variables
dt = 0.1
g = 9.8 
y = 0.5
A = 1.25
wf = 2./3.
t=0
#end

class Pendulo(object):
	def __init__(self,massa,l,theta,v):
		self.m = massa
		self.l = l 
		self.x = theta
		self.v = v
		self.w2 = g/l 
		self.T = 2.*math.pi*math.sqrt(l/g)
		self.k = massa*self.w2
		self.e = 0.5*massa*(l*v)**2+massa*g*l*(1.-math.cos(theta))
		
	def a(self,x,v,t):
		return -self.w2*math.sin(x) #- y*v + A*math.sin(wf*t)
				
	def move(self,t):
		at = self.a(self.x,self.v,t)
		self.x += self.v*dt + at*dt*dt/2.
		a_tmp = self.a(self.x,self.v,t)
		v_tmp = self.v+(at+a_tmp)*dt/2. 
		a_tmp = self.a(self.x,v_tmp,t)
		self.v += (a_tmp+at)*dt/2.
		self.e = 0.5*self.m*(self.l*self.v)**2 + (self.m*g*self.l*(1.-math.cos(self.x)))
#end

def grafico(visivel):
	axes = plt.gca()
	axes.axes.get_xaxis().set_visible(visivel)
	axes.spines['top'].set_color('none')
	axes.spines['right'].set_color('none')
	axes.yaxis.set_ticks_position('left')
	axes.xaxis.set_ticks_position('bottom')
	axes.spines['bottom'].set_position(('data',0))
	axes.spines['left'].set_position(('data',0))
#end 

#begin

p1 = Pendulo(1.,10.,math.pi/6,0)

tmax=20*p1.T
t=np.arange(0,tmax,dt)
x=np.zeros(t.size)
v=np.zeros(t.size)
e=np.zeros(t.size)
x[0],v[0],e[0]=p1.x,p1.v,p1.e


for i in range(t.size):
	p1.move(t[i])
	p1.x=(p1.x+math.pi)%(2*math.pi)-math.pi
	x[i],v[i],e[i]=p1.x,p1.v,p1.e
	

fig = plt.figure(facecolor='white')

XxT = fig.add_subplot(321,xlim=(0,tmax),ylim=(-2,2))
plt.setp(XxT.get_xticklabels(),visible = False)
grafico(False)
line1,=XxT.plot([],[],'k-',lw=2)

VxT = fig.add_subplot(323,xlim=(0,tmax),ylim=(-2,2))
plt.setp(VxT.get_xticklabels(),visible = False)
grafico(False)
line2,=VxT.plot([],[],'m-',lw=2)

XxV = fig.add_subplot(122,xlim=(-np.pi,np.pi),ylim=(-2,2))
grafico(False)
line3,=XxV.plot([],[],'g.',lw=2)

ExT = fig.add_subplot(325,xlim=(min(t),max(t)),ylim=(min(e)-0.01,max(e)+0.01))
grafico(True)
line4,=ExT.plot([],[],'r-',lw=2)


#frame base
def init():
	line1.set_data([],[])
	line2.set_data([],[])
	line3.set_data([],[])
	line4.set_data([],[])
	return line1,line2,line3,

#funcao animacao
def animate(i):
	a = t[:i]#np.linspace(0,2,1000)
	b = x[:i]#np.sin(2 * np.pi * (x - 0.01*i))
	c = v[:i]
	d = e[:i]

	
	line1.set_data(a,b)
	line2.set_data(a,c)
	line3.set_data(b,c)
	line4.set_data(a,d)
	return line1,line2,line3,
	
#cria animacao
anim = animation.FuncAnimation(fig,animate,init_func = init, frames=t.size,interval=0,blit=True)

plt.show()

print 'concluido'
#end
