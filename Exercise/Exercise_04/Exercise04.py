import rhinoscriptsyntax as rs
import math

surfaces = []
#ToBeFractal = []


class fractal(object):
    
    def __init__(self, surface, AttractPt):
        
        
        self.uvpoint = {}
        
        self.area = rs.Area(surface)
        
        self.AttractPt = AttractPt
        
        if self.area>=80:
            self.surface = surface
            self.udomain = rs.SurfaceDomain(self.surface, 0)
            self.vdomain = rs.SurfaceDomain(self.surface, 1)
            self.intU = 4
            self.intV = 4
            self.stepU = (self.udomain[1] - self.udomain[0])/self.intU
            self.stepV = (self.vdomain[1] - self.vdomain[0])/self.intV
            
            self.matrix()
            self.BaseCurve()
            self.BaseSrf()
            self.UV()
            self.Norm()
            self.Vector()
            self.Loft()
            
        
        
    def matrix(self):
        for i in range(self.intU + 1):
            for j in range(self.intV + 1):
                self.u = self.udomain[0] + i*self.stepU
                self.v = self.vdomain[0] + j*self.stepV
                self.uvpoint[(i,j)] = rs.EvaluateSurface(self.surface, self.u, self.v)
                #rs.AddPoint(self.uvpoint[(i,j)])
                #rs.AddPoint(uvpoint[(i,j)])
    
    def BaseCurve(self):
        
        self.BaseCurve = rs.AddCurve((self.uvpoint[(1,1)], self.uvpoint[(self.intU-1,1)], 
        self.uvpoint[(self.intU-1,self.intV-1)], self.uvpoint[(1,self.intV-1)],self.uvpoint[(1,1)]),1)
        
    def BaseSrf(self):
        self.BaseSrf = rs.AddPlanarSrf(self.BaseCurve)
    
    def UV(self):
        self.udomain02 = rs.SurfaceDomain(self.BaseSrf, 0)
        self.vdomain02 = rs.SurfaceDomain(self.BaseSrf, 1)
        
        self.u02 = (self.udomain02[0] + self.udomain02[1])/2
        self.v02 = (self.vdomain02[0] + self.vdomain02[1])/2
    def Norm(self):
        self.Norm = rs.SurfaceNormal(self.BaseSrf, (self.u02,self.v02))
        #area = rs.Area(BaseSrf)
        self.dis = rs.Distance(self.uvpoint[(1,1)], self.uvpoint[(self.intU-1, 1)])
        self.Norm = rs.VectorScale(self.Norm, 1*self.dis)
    
    def Vector(self):
        #rs.PointCoordinates()
        self.Vector = rs.VectorCreate(self.AttractPt, self.uvpoint[(1,1)])
        self.vLength = rs.VectorLength(self.Vector)
        self.Vector = rs.VectorScale(self.Vector, 7/self.vLength)
        self.Norm = rs.VectorAdd(self.Vector, self.Norm)
        
    def Loft(self):
        self.LoftSrf = rs.CopyObject(self.BaseSrf, self.Norm)
        
        self.LoftCrv = rs.CopyObject(self.BaseCurve, self.Norm)
        
        self.loftpt01 = rs.CopyObject(self.uvpoint[(1,1)], self.Norm)
        self.loftpt02 = rs.CopyObject(self.uvpoint[(self.intU-1,1)], self.Norm)
        self.loftpt03 = rs.CopyObject(self.uvpoint[(self.intU-1, self.intV-1)], self.Norm)
        self.loftpt04 = rs.CopyObject(self.uvpoint[(1,self.intV-1)], self.Norm)
        
        #rs.AddLoftSrf((BaseCurve, LoftCrv))
        
        self.SideCrv01 = rs.AddCurve((self.uvpoint[(1,1)], self.uvpoint[(self.intU-1, 1)], self.loftpt02, self.loftpt01, self.uvpoint[(1,1)]),1)
        self.SideCrv02 = rs.AddCurve((self.uvpoint[(self.intU-1,1)], self.uvpoint[(self.intU-1, self.intV-1)], self.loftpt03, self.loftpt02,self.uvpoint[(self.intU-1,1)]),1)
        self.SideCrv03 = rs.AddCurve((self.uvpoint[(self.intU-1,self.intV-1)], self.uvpoint[(1, self.intV-1)], self.loftpt04, self.loftpt03,self.uvpoint[(self.intU-1,self.intV-1)]),1)
        self.SideCrv04 = rs.AddCurve((self.uvpoint[(1,self.intV-1)], self.uvpoint[(1, 1)], self.loftpt01, self.loftpt04,self.uvpoint[(1,self.intV-1)]),1)
        
        self.SideSrf01 = rs.AddPlanarSrf(self.SideCrv01)
        self.SideSrf02 = rs.AddPlanarSrf(self.SideCrv02)
        self.SideSrf03 = rs.AddPlanarSrf(self.SideCrv03)
        self.SideSrf04 = rs.AddPlanarSrf(self.SideCrv04)
#            
#            
        fractal(self.SideSrf01,self.AttractPt)
        fractal(self.SideSrf02,self.AttractPt)
        fractal(self.SideSrf03,self.AttractPt)
        fractal(self.SideSrf04,self.AttractPt)
        fractal(self.LoftSrf,self.AttractPt)


def main():
    
    surface = rs.GetObjects('Select Surfaces', rs.filter.surface)
    AttractPt = rs.GetObject('Select a Attractor', rs.filter.point)
    
    rs.EnableRedraw(False)
    
    for i in range(len(surface)):
        
         fractal(surface[i],AttractPt)
        
    rs.EnableRedraw(True)
    
main()