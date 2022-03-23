
from gi.repository import Gtk

from . import sets
from . import seloff
from . import forms
from . import point
from . import points
from . import draw
from . import graph
from . import arcbutton
from . import step

def open(p):
	global box,info
	box=Gtk.Box()
	box.append(arcbutton.open(p))
	#box.append(sets.colorButton(chr(0x0077),manual,"Manual"))#0057
	#def manual(b,d):
	box.append(sets.colorButton(chr(0x2913),snap,"Snap to base"))
	box.append(sets.colorButton(seloff.char_delete,delete,"Delete"))
	box.append(sets.colorButton(chr(0x2B05),step.left,"Left"))
	box.append(sets.colorButton(chr(0x27A1),step.right,"Right"))
	box.append(sets.colorButton(chr(0x2B06),step.up,"Up"))
	box.append(sets.colorButton(chr(0x2B07),step.down,"Down"))
	info=sets.colorLabel(inf(p._offset_,p._height_))
	info.set_hexpand(True)
	info.set_halign(Gtk.Align.END)
	box.append(info)
	forms.box.get_parent().append(box)

def close():
	forms.box.get_parent().remove(box)

def delete(b,d):
	p=point.lastselect
	ix=points.points.index(p)
	dels,puts=p._take_(ix)
	ix=and_inter(ix,dels,puts)
	graph.lines(dels,puts,draw.wstore,draw.hstore)
	p._remove_(ix)
	if p.get_parent():
		p.get_parent().remove(p)
	close()
	point.lastselect=None
	graph.area.queue_draw()
def and_inter(ix,dels,puts):
	pnts=points.points
	sz=len(pnts)
	if ix==0:
		if sz==1:
			return ix
		if and_inter_test(1):
			dels.append([dels[0][1],pnts[1]])
	elif ix==(sz-1):
		if and_inter_test(sz-2):
			dels.append([pnts[sz-3],dels[0][0]])
			ix-=1
	elif pnts[ix-1]._inter_:
		if and_inter_test(ix+1):
			aux=pnts[ix+1]
			dels.append([dels[1][1],aux])
			puts[0][1]=aux
	return ix
def and_inter_test(test):
	p=points.points[test]
	b=p._inter_
	if b:
		p._remove_(test)
		if p.get_parent():
			p.get_parent().remove(p)
	return b

def inf(o,h):
	return str(o)+' '+str(h)

def snap(b,d):
	p=point.lastselect
	hg=p._height_
	p._height_=0
	x,y=p._coord_(draw.wstore,draw.hstore)
	p._height_=hg
	p._dend_(x,y)
	graph.area.queue_draw()
