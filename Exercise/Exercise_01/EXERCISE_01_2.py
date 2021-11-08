

import rhinoscriptsyntax as rs
import random as rnd
import math

ptcube = {}
crvlist = []
srflist = []
Ring = {}
h = 4 #height
m = 0.5 #distance 
c = 1.6 #center

def MidPtLoaded(pt01, pt02, pt03, pt04, load01, load02, load03, load04):
    MidPtLoaded = None
    MidPtLoaded = [(load01*pt01[0]+load02*pt02[0]+load03*pt03[0]+load04*pt04[0])/(load01+load02+load03+load04),
    (load01*pt01[1]+load02*pt02[1]+load03*pt03[1]+load04*pt04[1])/(load01+load02+load03+load04),
    (load01*pt01[2]+load02*pt02[2]+load03*pt03[2]+load04*pt04[2])/(load01+load02+load03+load04)]
    return MidPtLoaded
    
    
def PtCube(imax, jmax, kmax):
    
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax):
                x = (i+15)*i/(j+10) + 0.2*rnd.random()
                y = (j+15)*j/(i+10) + 0.2*rnd.random()
                z = k*h + rnd.random()
                
                ptcube[(i,j,k)] = [x, y, z]
                
                
                if i>0 and j>0 and k>0:
                    Ring[(i,j,k)] = rs.AddCurve((ptcube[(i-1,j-1,k-1)],
                    ptcube[(i-1,j,k-1)],ptcube[(i,j,k-1)],
                    ptcube[(i,j-1,k-1)],ptcube[(i-1,j-1,k-1)]),1)
                    
                    rs.HideObjects(Ring[i,j,k])
                    
                    
                    #\rs.AddPlanarSrf(Ring[(i,j,k+1)])
    for i in range(imax):
        for j in range(jmax):
            for k in range(kmax-1):
                if i >0 and j>0 and k>0:
                    MidPt = MidPtLoaded(ptcube[(i-1,j-1,k-1)], ptcube[(i-1,j,k-1)],
                    ptcube[(i,j,k-1)], ptcube[(i, j-1,k-1)],1,1,1,1)
                    
                    AxisDis =  math.sqrt((MidPt[0]-imax/c)*(MidPt[0]-imax/c)+
                    (MidPt[1]-jmax/c)*(MidPt[1]-jmax/c))
                    
                    
                    
                    
                    if i>0 and j>0 and k>0 and AxisDis> jmax*m:
                    #rs.AddPlanarSrf(Ring[(i,j,k+1)])
                    
                        BOX = rs.AddLoftSrf((Ring[(i,j,k)],Ring[(i,j,k+1)]))
                        CAP01 = rs.AddPatch(Ring[(i,j,k+1)],Ring[(i,j,k+1)])
                        CAP02 = rs.AddPatch(Ring[(i,j,k)],Ring[(i,j,k)])
                        #rs.ObjectColor(BOX,(255/imax*i,255-(255/jmax*j),255/kmax*k))
                        rs.ObjectColor(BOX, (254, 155 , (15+25*k)))
                        rs.ObjectColor(CAP01, (254,155,(15+25*k)))
                        rs.ObjectColor(CAP02, (254,155,(15+25*k)))
                    if i>0 and j>0 and k==1 and AxisDis <= jmax*m:
                        
                        VaseBase = rs.AddLoftSrf((Ring[(i,j,k)],Ring[(i,j,k+1)]))
                        VaseBottom = rs.AddPatch(Ring[(i,j,k+1)],Ring[(i,j,k+1)])
                        rs.AddPatch(Ring[(i,j,k)],Ring[(i,j,k)])
                        rs.ObjectColor(VaseBottom, (255,0,0))
                        rs.ObjectColor(VaseBase, (254,155,15 + 255/(30*k+1)))
                    
def Main():
    imax = rs.GetInteger("Enter imax value", 8)
    jmax = rs.GetInteger("Enter jmax value", 8)
    kmax = rs.GetInteger("Enter kmax value", 7)
    #m = jmax
    
    rs.EnableRedraw(False)
    PtCube(imax, jmax, kmax)
    rs.EnableRedraw(True)


Main()