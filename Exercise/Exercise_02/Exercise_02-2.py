import rhinoscriptsyntax as rs
import math 
import random

area = {}
uvpointo = {}
uvpoint = {}
ring = {}
ring2 = {}
ringA = {}
ringA2 = {}
dis = {}
uvnormal = {}
closept = {}
codis = {}
n = 1





def PleaseRunPlease(srf, obj, intU, intV):
     
    Udomain = rs.SurfaceDomain(srf, 0)
    Vdomain = rs.SurfaceDomain(srf, 1)
    
    Ustep = (Udomain[1] - Udomain[0])/intU
    Vstep = (Vdomain[1] - Vdomain[0])/intV
    
    cdis = (Vdomain[1] + Vdomain[0])/2
    #print Vdomain[0], Vdomain[1]
    
    for i in range (intU + 1):
        for j in range(intV + 1):
            
            u = Udomain[0] + Ustep * i
            v = Vdomain[0] + Vstep * j
            
            uvpointo[(i,j)] = rs.EvaluateSurface(srf, u, v)
            #rs.AddPoint(uvpointo[(i,j)])
            
            
            dis[(i,j)] = rs.Distance(uvpointo[i,j], (0,0,0))
            
    cdis = (uvpointo[(1, intV)][1] + uvpointo[(1, 0)][1])/2
    print cdis
    
    for i in range(intU + 1):
        for j in range(intV + 1):
            
            u = Udomain[0] + Ustep * i
            
    #        if math.sin(uvpointo[(i,j)][1]*math.pi/(cdis/4)) >= 0:
    #            v = Vdomain[0] + Vstep * j + 15*((math.sin(uvpointo[(i,j)][1]*math.pi/(cdis/4)))**(1/3))
    #        else :
    #            v = Vdomain[0] + Vstep * j - 15*(abs(math.sin(uvpointo[(i,j)][1]*math.pi/(cdis/4))))**(1/3)
            v = Vdomain[0] + Vstep * j + 5*(math.sin(uvpointo[(i,j)][1]*math.pi/(cdis/4)))
            #print v - Vdomain[0] - Vstep* j 
            uvpoint[(i,j)] = rs.EvaluateSurface(srf, u , v)
            
            uvnormal[(i,j)] = rs.SurfaceNormal(srf, (u,v))
            
            closept[(i,j)] = rs.PointClosestObject((uvpoint[(i,j)]),obj)
    
    for i in range(intU + 1):
        for j in range(intV +1):
             if i>0 and j>0:
                 ring[(i,j)] = rs.AddCurve((uvpoint[(i-1,j-1)], uvpoint[(i-1,j)],
                 uvpoint[(i,j)],uvpoint[(i,j-1)],uvpoint[(i-1,j-1)]),3)
                 ringA[(i,j)] = rs.AddCurve((uvpoint[(i-1,j-1)], uvpoint[(i-1,j)],
                 uvpoint[(i,j)],uvpoint[(i,j-1)],uvpoint[(i-1,j-1)]),2)
                 rs.AddPlanarSrf((ring[(i,j)], ringA[(i,j)]))
                 area[(i,j)] = rs.Area(ring[(i,j)])
                 
    for i in range(intU + 1):
        for j in range(intV + 1):
            
            
            codis[(i,j)] = n*rs.Distance(uvpoint[(i,j)], closept[(i,j)][1])
            
    for i in range(intU ):
        for j in range(intV ):
            uvnormal[(i,j)] = rs.VectorScale(uvnormal[i,j], area[(i+1,j+1)]**(1.2)/10 )
            
    for i in range(intU + 1):
        for j in range(intV + 1):
            uvnormal[(i,j)] = rs.PointAdd((uvpoint[i,j]),uvnormal[(i,j)])
            
    for i in range(intU + 1):
        for j in range(intV +1):
             if i>0 and j>0:
                 ring2[(i,j)] = rs.AddCurve((uvnormal[(i-1,j-1)], uvnormal[(i-1,j)],
                 uvnormal[(i,j)],uvnormal[(i,j-1)],uvnormal[(i-1,j-1)]),3)
                 ringA2[(i,j)] = rs.AddCurve((uvnormal[(i-1,j-1)], uvnormal[(i-1,j)],
                 uvnormal[(i,j)],uvnormal[(i,j-1)],uvnormal[(i-1,j-1)]),2)
                 rs.AddLoftSrf((ring2[(i,j)],ringA2[(i,j)]),loft_type=3)
                 
                 
    for i in range(intU + 1):
        for j in range(intV +1):
             if i>0 and j>0:
                 tubes = rs.AddLoftSrf((ring[(i,j)], ring2[(i,j)]))
                 tube2 = rs.AddLoftSrf((ringA[(i,j)],ringA2[(i,j)]))

def main():
    srf = rs.GetObject('Select a Surface Please', rs.filter.surface)
    obj = rs.GetObject('Select an Inteference Object Please')
    intU = rs.GetInteger('How many do you want for U?', 4)
    intV = rs.GetInteger('How mandy do you want for V?', 48)
    rs.HideObject((srf,obj))
    
    rs.EnableRedraw(False)
    PleaseRunPlease(srf,obj,intU,intV)
    rs.EnableRedraw(True)
    
main()