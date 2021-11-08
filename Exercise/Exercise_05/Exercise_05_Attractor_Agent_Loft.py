import rhinoscriptsyntax as rs
import math
import scriptcontext as sc
import random as rnd


class agents(object):
    
    def __init__(self,POINTID, POS, VEC):
        
        self.pointID = POINTID
        self.pos = POS
        self.vec = VEC
        self.posList = []
        self.posList.append(self.pos)
        
        self.trail = 'I am the initial guy, who has only one point for now'
        
    def allSystemGo(self,AttractorPopulation):
        
        self.sendToAttractors(AttractorPopulation)
        self.move()
        self.makeTrail()
    
    def sendToAttractors(self,AttractorPopulation):
        
        for attractorToBeSent in AttractorPopulation:
            attractedVec = attractorToBeSent.attraction(self)
            self.vec = rs.VectorAdd(self.vec, attractedVec)
    

    def move(self):
        
        self.pos = rs.PointAdd(self.pos, self.vec)
        #print self.vec
        self.posList.append(self.pos)
    
    
    def makeTrail(self):
        
        
        if self.trail != 'I am the initial guy, who has only one point for now':
            
            rs.DeleteObject(self.trail)
        #if len(self.posList) >= 2:
        self.trail = rs.AddCurve(self.posList,2)
    
    def returnTrail(self):
        return self.trail
        
        
        
        
class attractors(object):
    
    def __init__(self, AttractionPt,AttractorPos):
        self.attractors = AttractionPt 
        self.pos = AttractorPos
        self.run = [-15,-15,-15]
    
    def attraction(self,agent):
        
        self.run[0] = -5
        
        if self.pos[2] > 250 or self.pos[2] < -250:
            self.run[2] = -self.run[2] 
        
        if self.pos[1] > 250 or self.pos[1] < -250:
            self.run[1] = -self.run[1] 
        
        self.run = [self.run[0], self.run[1], self.run[2]]
        #self.run = rs.VectorScale(self.run, 2*rnd.random())
        self.pos = rs.PointAdd(self.pos, self.run)
        self.dis = rs.Distance(self.pos,agent.pos)
        #print self.dis
        #print agent.pos
        #print self.pos
        
        self.vec = rs.VectorCreate(self.pos, agent.pos)
        self.vec = rs.VectorUnitize(self.vec)
        self.vec = rs.VectorScale(self.vec, self.dis/10)
        rs.AddPoint(self.pos)
        #print self.vec
        return self.vec
        


        
        
        


def main():
    
    agentPts = rs.GetObjects('Select Agent Points, prefer a even number', rs.filter.point)
    attractorPts = rs.GetObjects('Select Attractor POints', rs.filter.point)
    
    initialVec = [5,5,5]
    
    agentPopulation = []
    attractorPopulation = []
    
    for attractorPt in attractorPts:
        
        attractorPOS = rs.PointCoordinates(attractorPt)
        attractorPopulation.append(attractors(attractorPt,attractorPOS))
    
    
    for agentPt in agentPts:
        
        agentPOS = rs.PointCoordinates(agentPt)
        agentPopulation.append(agents(agentPt, agentPOS, initialVec))
        
    #just a initial object to be deleted
    bList = []
    b = rs.AddPoint((0,0,0))
    bList.append(b)
    
    while not sc.escape_test():
        
        rs.EnableRedraw(False)
        
        rs.DeleteObjects(bList)
        trailList = []
        
        for agent in agentPopulation:
            
            agent.allSystemGo(attractorPopulation)
            trailList.append(agent.returnTrail())
        
        
        for i in range(int(len(trailList)/2+1)):
            if i >0:
                b = rs.AddLoftSrf((trailList[2*i-2],trailList[2*i-1]))
                bList.append(b)
        
        rs.EnableRedraw(True)
            
    
    
main()
    
    