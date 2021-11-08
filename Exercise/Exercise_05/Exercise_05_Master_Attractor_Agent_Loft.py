import rhinoscriptsyntax as rs
import math
import scriptcontext as sc



class agents(object):
    
    def __init__(self,POINTID, POS, VEC):
        
        self.pointID = POINTID
        self.pos = POS
        self.vec = VEC
        self.posList = []
        self.posList.append(self.pos)
        
        self.trail = 'I am the initial guy, whose destiny is to be deleted'
        
    def allSystemGo(self,AttractorPopulation,MasterPt):
        
        self.sendToAttractors(AttractorPopulation, MasterPt)
        self.move()
        self.makeTrail()
    
    def sendToAttractors(self,AttractorPopulation, MasterPt):
        
        for attractorToBeSent in AttractorPopulation:
            attractedVec = attractorToBeSent.sendToMaster(self, MasterPt)
            self.vec = rs.VectorAdd(self.vec, attractedVec)
    
    def sendToGravity(self,AttractorPopulation):
        pass
        
        
        
        
    def Tube(self):
        pass
        
    def move(self):
        
        self.pos = rs.PointAdd(self.pos, self.vec)
        #print self.vec
        self.posList.append(self.pos)
    
    
    def makeTrail(self):
        
        
        if self.trail != 'I am the initial guy, whose destiny is to be deleted':
            
            rs.DeleteObject(self.trail)
        #if len(self.posList) >= 2:
        self.trail = rs.AddCurve(self.posList,2)
    
    def returnTrail(self):
        return self.trail
        
        
        
        
class attractors(object):
    
    def __init__(self, AttractionPt,AttractorPos):
        self.attractors = AttractionPt 
        self.pos = AttractorPos
        self.run = [3,0,0]
    
    def sendToMaster(self,agent, MasterPt):
        self.pos = rs.PointAdd(self.pos, self.run)
        
        self.vec = MasterPt.attractionMaster(self, agent)
        rs.AddPoint(self.pos)
        return self.vec




class Master():
    
    def __init__(self, MasterID):
        self.ID = MasterID
        self.pos = rs.PointCoordinates(MasterID)
        self.run = [0,3,0]
        self.trail = "I am another initial guy, who is meant to be deleted"
        
        self.posList = []
        self.posList.append(self.pos)
        
    def attractionMaster(self, attractor, agent):
        self.disATT = rs.Distance(self.pos, attractor.pos)
        self.disAGT = rs.Distance(self.pos, agent.pos)
        
        self.run = rs.VectorScale(self.run, 1) + rs.VectorScale(rs.VectorUnitize(rs.VectorCreate( attractor.pos,self.pos)),self.disATT/5)
        
        self.pos = rs.PointAdd(self.pos, self.run)
        #print self.pos
        #print self.disATT
        #print self.disAGT
        self.vecATT = rs.VectorUnitize(rs.VectorCreate(self.pos, attractor.pos))
        self.vecAGT = rs.VectorUnitize(rs.VectorCreate(self.pos, agent.pos))
        self.vec = rs.PointAdd(self.vecATT, self.vecAGT)
        self.vec = rs.VectorScale(self.vec, 5)
        self.drawTube()
        return self.vec
        
    def drawTube(self):
        self.posList.append(self.pos)
        if self.trail != "I am another initial guy, who is meant to be deleted":
            rs.DeleteObject(self.trail)
            
            
        self.trail = rs.AddCurve(self.posList, 2)



def main():
    
    agentPts = rs.GetObjects('Select Agent Points, prefer a even number', rs.filter.point)
    attractorPts = rs.GetObjects('Select Attractor POints', rs.filter.point)
    masterPt = rs.GetObject('Select a Master Point', rs.filter.point)
    
    masterPt = Master(masterPt)
    
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
            
            agent.allSystemGo(attractorPopulation, masterPt)
            trailList.append(agent.returnTrail())
        
        
        for i in range(int(len(trailList)/2+1)):
            if i >0:
                b = rs.AddLoftSrf((trailList[2*i-2],trailList[2*i-1]))
                bList.append(b)
        
        rs.EnableRedraw(True)
            
    
    
main()
    
    