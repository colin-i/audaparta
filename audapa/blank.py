
from gi.repository import Gtk

from . import sets

start=Gtk.EntryBuffer(text="0")
stop=Gtk.EntryBuffer(text="0")

def open(b,combo):
	bx=Gtk.Grid(hexpand=True)
	bx.attach(sets.colorLabel("Blank samples at start"),0,0,1,1)
	bx.attach(sets.colorEntry(start),1,0,1,1)
	bx.attach(sets.colorLabel("Blank samples at end"),0,1,1,1)
	bx.attach(sets.colorEntry(stop),1,1,1,1)
	bx.attach(sets.colorButton("Cancel",cancel,"Abort",combo),0,2,2,1)
	bx.attach(sets.colorButton("Done",done,"Apply",combo),0,3,2,1)
	combo[0].set_child(bx)

def cancel(b,combo):
	combo[0].set_child(combo[1])

def done(b,combo):
	combo[0].set_child(combo[1])
	n=len(draw.samples)
	a=start.get_text()
	if a.isdigit():
		c=int(a)
		draw.samples=([0]*c)+draw.samples
	b=stop.get_text()
	if b.isdigit():
		c=int(b)
		draw.samples+=[0]*c
