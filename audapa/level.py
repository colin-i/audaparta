
from gi.repository import Gtk

from . import sets
from . import draw
from . import points
from . import save
from . import graph
from . import point
from . import distance

dif=Gtk.EntryBuffer()

#signbutton,maxlabel
sign_positive="+"

def open(b,combo):
	box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
	#+/- button or not   entry   maxim
	global signbutton,maxlabel,calculated,middlerate,pausesbool
	b2=Gtk.Box()
	if draw.baseline!=0:
		signbutton=sets.colorButton(sign_positive,sign,"Sign")
		b2.append(signbutton)
	en=sets.colorEntry(dif)
	b2.append(en)
	b2.append(sets.colorLabel("from 0 to "))
	maxlabel=sets.colorLabel(maximum())
	b2.append(maxlabel)
	box.append(b2)
	#atstart   middle[-1,1]   - or calculated
	cdata,mdata=calculate()
	st=sets.colorLabel(cdata)
	middlerate=sets.colorLabel(mdata)
	calculated=sets.colorLabel("-")
	b3=Gtk.Box(homogeneous=True)
	b3.append(st)
	b3.append(middlerate)
	b3.append(calculated)
	box.append(b3)
	b4=Gtk.Box()
	b4.append(sets.colorLabel("Keep pauses"))
	pausesbool=Gtk.CheckButton(active=True)
	b4.append(pausesbool)
	box.append(b4)
	#Calculate
	calc=sets.colorButton("Set",calcs,"Calculate")
	box.append(calc)
	#Cancel
	exit=sets.colorButton("Cancel",abort,"Abort",combo)
	box.append(exit)
	bt=sets.colorButton("Return",click,"Finish",combo)
	box.append(bt)
	bt=sets.colorButton("Done",ready,"Set & Return",combo)
	box.append(bt)
	combo[0].set_child(box)
	#copies
	global pointsorig,samplesorig,pointsorigh #since pauses can be more points
	#.copy() => it is not deep, _height_ same
	pointsorig=points.points.copy()
	pointsorigh=[]
	for p in points.points:
		pointsorigh.append(p._height_)
	samplesorig=draw.samples.copy()

def click(b,combo):
	finish(combo)
def finish(combo):
	if distance.test_all():
		conclude(combo)
def conclude(combo):
	done(combo) #this here, else problems at get_native().get_surface()
	if sets.get_fulleffect():
		save.saved()
	else:
		abort_samples()
	graph.redraw()

def sign(b,d):
	if b.get_child().get_text()==sign_positive:
		b._set_text_("-")
	else:
		b._set_text_(sign_positive)
	maxlabel._set_text_(maximum())

def abort_samples():
	draw.samples=samplesorig
def abort(b,combo):
	restore()
	abort_samples()
	done(combo)
def restore():
	points.points.clear()
	for i in range(0,len(pointsorigh)):
		points.points.append(pointsorig[i])
		points.points[i]._height_=pointsorigh[i]

def size_sign():
	if draw.baseline!=0:
		positiv=signbutton.get_child().get_text()==sign_positive
	else:
		positiv=True
	return (get_size(),positiv)
def get_size():
	if draw.baseline!=0:
		return int(draw.sampsize*draw.baseline)
	return draw.sampsize

def maximum():
	a,positiv=size_sign()
	a-=1 #not targeting 32768, but [0,32767]
	x=0
	for p in points.points:
		if p._height_>=0:
			h=p._height_
		else:
			h=-p._height_
		if positiv:
			h=a-h
		if h>x:
			x=h
	return x.__str__()

def not_a_digit(buf):
	buf.set_text("0",-1) #isdigit failed

def calcs(b,d):
	modify()
def modify():
	c=dif.get_text()
	if c.isdigit():
		a=int(c)
		b=int(maxlabel.get_text())
		if a>b:
			dif.set_text(b.__str__(),-1)
			return
		restore() #need no more points or points tend to flat
		sz,sgn=size_sign()
		pauses=[]
		if sgn:
			rng=len(points.points)
			for i in range(0,rng):
				if pause(i,pauses):
					p=points.points[i]
					if p._height_>=0:
						p._height_+=a
						if p._height_>=sz:
							p._height_=sz-1
					else:
						p._height_-=a
						if p._height_<-sz:
							p._height_=-sz
		else:
			rng=len(points.points)
			for i in range(0,rng):
				p=points.points[i]
				if p._height_>=0:
					if a>=p._height_:
						p._height_=0
					else:
						p._height_-=a
				else:
					if a>=-p._height_:
						p._height_=0
					else:
						p._height_+=a
		resolve(pauses)
		maxlabel._set_text_(maximum())
		save.apply()
		cdata,mdata=calculate()
		calculated._set_text_(cdata)
		middlerate._set_text_(mdata)
		return
	not_a_digit(dif)

def done(combo):
	combo[0].set_child(combo[1])

def ready(b,combo):
	modify()
	finish(combo)

def calculate():
	s=len(points.points)
	if s>=2:
		n=0
		start=points.points[0]._offset_
		stop=points.points[s-1]._offset_
		for i in range(start,stop):
			n+=abs(draw.samples[i])
		med=n/(stop-start)
		#
		a=get_size()/2
		b=med-a
		mid=b/a
		#
		return (med.__str__(),mid.__str__())
	return ("-","-")

def pause(i,lst):
	if pausesbool.get_active():
		a=points.points[i]
		if a._height_==0:
			j=i+1
			if j!=len(points.points):
				b=points.points[j]
				if b._height_==0:
					#here is a sound pause
					first=len(lst)==0
					if first or lst[len(lst)-1]!=i:
						#is new
						lst.append(i)
						lst.append(j)
						if first:
							#the interval start if it is at the start it will not be adjusted
							return False
					else:
						#extend only
						lst[len(lst)-1]=j
						return False
			elif lst[len(lst)-1]==i:
				#last needs false
				return False
	return True

def resolve(pauses):
	sz=len(pauses)
	of=0
	i=0
	while i<sz: #for-loop will not care about i modification inside
		a=pauses[i]
		if a>0:
			insert(a+of,1)
			of+=1
		i+=1
		a=pauses[i]
		if a+1<len(points.points):
			insert(a+of,0)
			of+=1
		i+=1

def insert(ix,more):
	p=points.points[ix]
	points.add(p._offset_,0,False,point.default_convex,ix+more)
