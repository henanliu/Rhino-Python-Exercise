import rhinoscriptsyntax as rs
import math

surfaces = []
ToBeFractal = []

def fractal(surface):
    
    uvpoint = {}
    
    area = rs.Area(surface)
    
    if area>=300:
        
        
        udomain = rs.SurfaceDomain(surface, 0)
        vdomain = rs.SurfaceDomain(surface, 1)
        intU = 4
        intV = 4
        stepU = (udomain[1] - udomain[0])/intU
        stepV = (vdomain[1] - vdomain[0])/intV
    
        for i in range(intU + 1):
            for j in range(intV + 1):
                u = udomain[0] + i*stepU
                v = vdomain[0] + j*stepV
                uvpoint[(i,j)] = rs.EvaluateSurface(surface, u, v)
                #rs.AddPoint(uvpoint[(i,j)])
                
        BaseCurve = rs.AddCurve((uvpoint[(1,1)], uvpoint[(intU-1,1)], 
        uvpoint[(intU-1,intV-1)], uvpoint[(1,intV-1)],uvpoint[(1,1)]),1)
        
        BaseSrf = rs.AddPlanarSrf(BaseCurve)
        udomain02 = rs.SurfaceDomain(BaseSrf, 0)
        vdomain02 = rs.SurfaceDomain(BaseSrf, 1)
        
        u02 = (udomain02[0] + udomain02[1])/2
        v02 = (vdomain02[0] + vdomain02[1])/2
        
        Norm = rs.SurfaceNormal(BaseSrf, (u02,v02))
        
        #area = rs.Area(BaseSrf)
        dis = rs.Distance(uvpoint[(1,1)], uvpoint[(intU-1, 1)])
        
        Norm = rs.VectorScale(Norm, 1*dis)
        
        LoftSrf = rs.CopyObject(BaseSrf, Norm)
        
        LoftCrv = rs.CopyObject(BaseCurve, Norm)
        
        loftpt01 = rs.CopyObject(uvpoint[(1,1)], Norm)
        loftpt02 = rs.CopyObject(uvpoint[(intU-1,1)], Norm)
        loftpt03 = rs.CopyObject(uvpoint[(intU-1, intV-1)], Norm)
        loftpt04 = rs.CopyObject(uvpoint[(1,intV-1)], Norm)
        
        #rs.AddLoftSrf((BaseCurve, LoftCrv))
        
        SideCrv01 = rs.AddCurve((uvpoint[(1,1)], uvpoint[(intU-1, 1)], loftpt02, loftpt01, uvpoint[(1,1)]),1)
        SideCrv02 = rs.AddCurve((uvpoint[(intU-1,1)], uvpoint[(intU-1, intV-1)], loftpt03, loftpt02,uvpoint[(intU-1,1)]),1)
        SideCrv03 = rs.AddCurve((uvpoint[(intU-1,intV-1)], uvpoint[(1, intV-1)], loftpt04, loftpt03,uvpoint[(intU-1,intV-1)]),1)
        SideCrv04 = rs.AddCurve((uvpoint[(1,intV-1)], uvpoint[(1, 1)], loftpt01, loftpt04,uvpoint[(1,intV-1)]),1)
        
        SideSrf01 = rs.AddPlanarSrf(SideCrv01)
        SideSrf02 = rs.AddPlanarSrf(SideCrv02)
        SideSrf03 = rs.AddPlanarSrf(SideCrv03)
        SideSrf04 = rs.AddPlanarSrf(SideCrv04)
        
        
        fractal(SideSrf01)
        fractal(SideSrf02)
        fractal(SideSrf03)
        fractal(SideSrf04)
        fractal(LoftSrf)
        #rs.ExtrudeCurve(BaseCurve, [0,0,10])


def rotatescale(surfaces):
    Origin = []
    RotatedSrf = []
    
    Origin = rs.AddPoints(rs.SurfacePoints(surfaces[0]))
    OriginB = rs.AddPoints(rs.SurfacePoints(surfaces[1]))
    
    NXvalue = rs.PointCoordinates(Origin[3])[0] - rs.PointCoordinates(OriginB[1])[0]
    NYvalue = rs.PointCoordinates(Origin[3])[1] - rs.PointCoordinates(OriginB[1])[1]
    NZvalue = rs.PointCoordinates(Origin[3])[2] - rs.PointCoordinates(OriginB[1])[2]
    
    for i in range(len(surfaces)):
        MovedSrf = rs.CopyObject((surfaces[i]),(NXvalue, NYvalue, NZvalue))
        ScaledSrf = rs.ScaleObject(MovedSrf, Origin[3], [0.95,0.95,0.95])
        #ScaledSrf.append(rs.ScaleObject(MovedSrf, Origin[3], [0.8,0.8,0.8]))
        #RotatedSrf = rs.RotateObject(ScaledSrf, Origin[3], 15)
        NewSrf = rs.RotateObject(ScaledSrf, Origin[3], 25)
        RotatedSrf.append(NewSrf)
        ToBeFractal.append(NewSrf)
        
        
    if rs.Area(ScaledSrf) > 50:
        
        rotatescale(RotatedSrf)



def main():
    
    surfaces = rs.GetObjects('Select Surfaces', rs.filter.surface)
    
    rs.EnableRedraw(False)
    
    
    rotatescale(surfaces)
    
    for i in range(len(surfaces)):
        ToBeFractal.append(surfaces[i])
    
    for i in range(len(ToBeFractal)):
        
        fractal(ToBeFractal[i])
    
    
        
    rs.EnableRedraw(True)

main()