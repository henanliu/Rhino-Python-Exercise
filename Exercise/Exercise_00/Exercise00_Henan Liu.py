import rhinoscriptsyntax as rs
import random as rnd

pipelist = []
crvlist = []
ptcube = {}
x = rs.GetInteger('Set imax Value', 5)
y = rs.GetInteger('Set jmax Value', 5)
z = rs.GetInteger('Set kmax Value', 5)
u = 0
v = 1

def MidPtLoaded(pt01,pt02,pt03,pt04,load01,load02,load03,load04):
     
     MidPtLoaded = None
     MidPtLoaded = [(load01*pt01[0]+load02*pt02[0]+load03*pt03[0]+load04*pt04[0])/(load01+load02+load03+load04),
     (load01*pt01[1]+load02*pt02[1]+load03*pt03[1]+load04*pt04[1])/(load01+load02+load03+load04),
     (load01*pt01[2]+load02*pt02[2]+load03*pt03[2]+load04*pt04[2])/(load01+load02+load03+load04)]
     return MidPtLoaded
    

def RWR(Min,Max):
    RWR = Min + (Max-Min)*rnd.random()
    return RWR
    
def Main():
    for i in range(x):
        for j in range(y):
            for k in range(z):
                
                ptv_1 = i * 5 + 2*RWR(u,v)
                ptv_2 = j * 5 + 2*RWR(u,v)
                ptv_3 = k * 5 + 2*RWR(u,v)
                
                ptcube[(i,j,k)] = [ptv_1,ptv_2,ptv_3]
                
                
    for i in range(x):
        for j in range(y):
            for k in range(z):
                if i > 0 and j > 0 and k > 0:
                    Structure = crvlist.append(rs.AddCurve((ptcube[(i-1,j-1,k)], ptcube[(i-1,j,k)], ptcube[(i,j,k)], ptcube[(i, j-1,k)],ptcube[(i-1,j-1,k)]),1))    
                    HorizontalConnection = crvlist.append(rs.AddLine((MidPtLoaded(ptcube[(i-1,j-1,k-1)], ptcube[(i-1,j,k-1)], ptcube[(i,j,k-1)], ptcube[(i, j-1,k-1)],1,1,1,1)),ptcube[(i-1,j-1,k)]))
                if i >0 and j >0 and k > 0 and k < z-1 :
                    Point01 = MidPtLoaded(ptcube[(i-1,j-1,k-1)], ptcube[(i-1,j,k-1)], ptcube[(i,j,k-1)], ptcube[(i, j-1,k-1)],1,1,1,1)
                    Point02 = MidPtLoaded(ptcube[(i-1,j-1,k)], ptcube[(i-1,j,k)], ptcube[(i,j,k)], ptcube[(i,j-1,k)],1,1,1,1)
                    VerticalConnection = crvlist.append(rs.AddLine(Point01, Point02))
                

#for o in range(len(crvlist)):
    
    #PipeR = RandomWithinRange(v,u)
    #pipelist.append(rs.AddPipe(crvlist[o], 0, PipeR))
    
Main()
#a = crvlist
#b = pipelist