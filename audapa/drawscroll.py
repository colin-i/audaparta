from gi.repository import Gtk,Gdk

from . import draw
from . import r_offset
from . import seloff
from . import sets

#size,landscape,win

def set_landscape():
	global landscape
	landscape=win.get_width()>=win.get_height()
def calculate(n):
	w=win.get_width()
	h=win.get_height()
	d=draw.area
	f=3
	global size
	if landscape:
		#30000 maximum size of an X window
		if n>(size:=(w*f)):
			n=size
		elif n<=w:#cannot go back at overshot without this
			if draw.length>w:
				n=w+1
			else:
				n=w
		if d.get_width()!=n or d.get_height()!=h:
			d.set_size_request(n,h)
			r_offset.cnged(win.get_hadjustment(),w)
			return True
	else:
		if n>(size:=(h*f)):
			n=size
		elif n<=h:
			if draw.length>h:
				n=h+1
			else:
				n=h
		if d.get_width()!=w or d.get_height()!=n:
			d.set_size_request(w,n)
			r_offset.cnged(win.get_vadjustment(),h)
			return True
	return False

def forward(a,b):
	n=draw.offset+draw.size
	if n<draw.length:
		draw.offset+=a
		r_offset.cged(b)
		draw.redraw()
def backward(a,b):
	if draw.offset>0:
		draw.offset-=a
		r_offset.cged(b)
		draw.redraw()
def edge(wn,pos,d):
	if pos==Gtk.PositionType.RIGHT:
		forward(size,win.get_hadjustment())
	elif pos==Gtk.PositionType.BOTTOM:
		forward(size,win.get_vadjustment())
	elif pos==Gtk.PositionType.LEFT:
		backward(min(size,draw.offset),win.get_hadjustment())
	else:
		backward(min(size,draw.offset),win.get_vadjustment())

def init():
	global win
	win=Gtk.ScrolledWindow(vexpand=True)
	win.set_child(draw.init())
	win.connect('edge-overshot',edge,None)
	win.get_hadjustment().connect('value-changed',r_offset.cgd,None)
	win.get_vadjustment().connect('value-changed',r_offset.cgd,None)

def move(b,next):
	if landscape:
		a=int(win.get_width()/2)
		b=win.get_hadjustment()
	else:
		a=int(win.get_height()/2)
		b=win.get_vadjustment()
	if next:
		forward(a,b)
	else:
		backward(a,b)

def open():
	global control
	control=Gtk.EventControllerKey()
	control.connect("key-pressed",eve,None)
	win.add_controller(control)
def close():
	win.remove_controller(control)
def eve(controller,keyval,keycode,state,d):
	if keyval==Gdk.KEY_period or keyval==Gdk.KEY_greater:
		seloff.moveright.emit(sets._click_)
		return True
	elif keyval==Gdk.KEY_comma or keyval==Gdk.KEY_less:
		seloff.moveleft.emit(sets._click_)
		return True
	return False
