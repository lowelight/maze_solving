# COMP9021 21T3 - Rachid Hamadi
# Assignment 2 *** Due Monday Week 11 @ 10.00am

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# IMPORT ANY REQUIRED MODULE
from os import write
import numpy
import copy





class MazeError(Exception):
    def __init__(self, message):
        self.message = message


class Maze:
    countUEEP=0
    countCDS=0
    countacA=0
    countInner=0
    countWall=0
    count=0
    UUP=[]
    points=[]
    grid = []
    mazeG = []
    dimMX = 0
    dimMY = 0
    dimY = 0
    dimX = 0
    filename =''
    def __init__(self, filename):
        self.grid = self.makeGrid(filename)
        self.filename = filename
        dimY = len(self.grid)
        dimX = len(self.grid[0])
        dimMY = 2*dimY-1
        dimMX = 2*dimX-1
        self.dimMX =dimMX
        self.dimMY =dimMY
        self.mazeG = self.makeMaze(self.grid)
        self.count = self.findGate(self.mazeG, dimMY, dimMX)
        self.countWall = self.wallSets(self.mazeG, dimMY, dimMX)
        self.countInner = self.innerP(self.mazeG, dimMY, dimMX)
        self.countacA = self.AcArea(self.mazeG, dimMY, dimMX)
        self.countCDS = self.forward(self.mazeG, dimMY, dimMX)
        self.countUEEP = self.findUEEP(self.mazeG, dimMY, dimMX)
        # REPLACE PASS ABOVE WITH YOUR CODE
    
    # POSSIBLY DEFINE OTHER METHODS
        
    def makeGrid(self,filename):
        grid=[]
        cList=[]
        with open(filename) as f:
            while True:
                c = f.read(1)
                if not c:
                    grid.append(cList)
                    break
                elif c != '\n':
                    cList.append(c)
                else :
                    grid.append(cList)
                    cList=[]
        grid2=[]
        for x in grid:
            wList=[]
            for y in x:
                if y != ' ':
                    wList.append(int(y))
            grid2.append(wList)
        grid3=[]
        for x in grid2:
            if x != []:
                grid3.append(x)
        
        for y in grid3:
            if len(grid3[0])!=len(y):
                raise MazeError('Incorrect input.')
        for x in grid3:
            for y in x:
                if y not in (0,1,2,3):
                    raise MazeError('Incorrect input.')
        if len(grid3) <= 1:
            raise MazeError('Incorrect input.')
        for m in grid3:
            if m[-1]==1 or m[-1]==3:
                raise MazeError('Input does not represent a maze.')
        for g in grid3[-1]:
            if g == 2 or g == 3:
                raise MazeError('Input does not represent a maze.')
        return grid3

    def makeMaze(self,grid):
        dimY = len(grid)
        dimX = len(grid[0])
        self.dimX = dimX
        self.dimY = dimY
        dimMY = 2*dimY-1
        dimMX = 2*dimX-1
        mazeG = numpy.zeros([dimMY, dimMX], dtype= int)
        gY = 0
        mY = 0
        while gY < dimY:
            gX = 0
            mX = 0
            while gX < dimX:
                if grid[gY][gX] == 1:
                    mazeG[mY][mX], mazeG[mY][mX+1], mazeG[mY][mX+2] = 1,1,1
                    if mY+1 < dimMY :
                        mazeG[mY+1][mX] = 2
                elif grid[gY][gX] == 2:
                    mazeG[mY][mX], mazeG[mY+1][mX], mazeG[mY+2][mX] = 1,1,1
                    if mX+1 < dimMX :
                        mazeG[mY][mX+1] = 2
                elif grid[gY][gX] == 3:
                    mazeG[mY][mX], mazeG[mY][mX+1], mazeG[mY][mX+2] = 1,1,1
                    mazeG[mY][mX], mazeG[mY+1][mX], mazeG[mY+2][mX] = 1,1,1
                elif grid[gY][gX] == 0:
                    if mX+1 >= dimMX and mY+1 >= dimMY:
                        pass
                    elif mX+1 >= dimMX:
                        mazeG[mY+1][mX] = 2
                    elif mY+1 >= dimMY:
                        mazeG[mY][mX+1] = 2
                    else :    
                        mazeG[mY][mX+1], mazeG[mY+1][mX] = 2 , 2
                gX += 1
                mX += 2
            gY += 1
            mY += 2
        # make pillar
        mY = 0
        while mY < dimMY:
            if mY % 2 == 0:
                mX = 0 
                while mX < dimMX:
                    count = 0
                    if mazeG[mY][mX] == 0:
                        if mY - 1 < 0 or mazeG[mY-1][mX] == 2:
                            count += 1
                        if mY + 1 >= dimMY or mazeG[mY+1][mX] == 2:
                            count += 1    
                        if mX - 1 < 0 or mazeG[mY][mX-1] == 2:
                            count += 1
                        if mX + 1 >= dimMX or mazeG[mY][mX+1] == 2:
                            count += 1
                        if count == 4:
                            mazeG[mY][mX] = 3
                    mX += 1
            mY += 1
        return mazeG
    
    def findGate(self, mazeG, dimMY, dimMX):
        count = 0
        for x in mazeG[0]:
            if x == 2:
                count += 1
        for x in mazeG[dimMY-1]:
            if x == 2:
                count += 1
        yY = 0
        while yY < dimMY:
            if mazeG[yY][0] == 2:
                count += 1
            yY += 1
        yY = 0    
        while yY < dimMY:
            if mazeG[yY][dimMX-1] == 2:
                count += 1
            yY += 1
        return count

    def wallSets(self, mazeG, dimMY, dimMX):
        bList=[]
        cList=[]
        dList=[]
        def findWalls(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 1:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        findWalls(x-1,y)
                        findWalls(x+1,y)
                        findWalls(x,y-1)
                        findWalls(x,y+1)
        y=0
        while y < dimMY:
            x = 0
            while x < dimMX:
                if [x,y] not in dList and mazeG[y][x] == 1:
                    findWalls(x,y)
                    for i in cList:
                        dList.append(i)
                    bList.append(cList)
                cList=[]
                x += 1
            y += 1
        return(len(bList))

    def innerP(self, mazeG, dimMY, dimMX):
        bList=[]
        cList=[]
        dList=[]
        count = [0]
        def findPoints(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        findPoints(x-1,y)
                        findPoints(x+1,y)
                        findPoints(x,y-1)
                        findPoints(x,y+1)
                elif mazeG[y][x] == 2:
                    findPoints(x-1,y)
                    findPoints(x+1,y)
                    findPoints(x,y-1)
                    findPoints(x,y+1)
            else:
                count[0] += 1
        y=0
        while y < dimMY:
            x = 0
            while x < dimMX:
                if [x,y] not in dList and mazeG[y][x] == 0:
                    findPoints(x,y)
                    if count[0] == 0:
                        for i in cList:
                            dList.append(i)
                        bList.append(cList)
                    else:
                        for i in cList:
                            dList.append(i)
                count[0] = 0
                cList=[]
                x += 1
            y += 1
        for x in bList:
            for i in x:
                self.mazeG[i[1],i[0]] = 4
        count1= 0 
        for x in bList:
            count1 += len(x)
        return count1

    def AcArea(self, mazeG, dimMY, dimMX):
        bList=[]
        cList=[]
        dList=[]
        def findAcArea(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        findAcArea(x-1,y)
                        findAcArea(x+1,y)
                        findAcArea(x,y-1)
                        findAcArea(x,y+1)
        x = 0                
        while x < dimMX:
            if [x,0] not in dList and mazeG[0][x] == 2:
                findAcArea(x,0)
                for i in cList:
                    dList.append(i)
                bList.append(cList)
            cList=[]
            x += 1
        x = 0
        while x < dimMX:
            if [x,dimMY-1] not in dList and mazeG[dimMY-1][x] == 2:
                findAcArea(x,dimMY-1)
                for i in cList:
                    dList.append(i)
                bList.append(cList)
            cList=[]
            x += 1
        y = 0    
        while y < dimMY:
            if [0,y] not in dList and mazeG[y][0] == 2:
                findAcArea(0,y)
                for i in cList:
                    dList.append(i)
                bList.append(cList)
            cList=[]
            y += 1
        y = 0    
        while y < dimMY:
            if [dimMX-1,y] not in dList and mazeG[y][dimMX-1] == 2:
                findAcArea(dimMX-1,y)
                for i in cList:
                    dList.append(i)
                bList.append(cList)
            cList=[]
            y += 1
        return(len(bList))

    def checkCDS(self,x, y,x1,y1):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        if (x < 0 or x >= dimMX or y < 0 or y >= dimMY) or mazeG[y][x] != 0:
            return False
        count1 = [0]
        cList=[[x1,y1]]
        def checking(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        checking(x-1,y)
                        checking(x+1,y)
                        checking(x,y-1)
                        checking(x,y+1)
            else:
                count1[0] += 1
        checking(x,y)
        if count1[0] == 0:
            return True
        else:
            return False

    def deepCheck(self,x,y,x1,y1):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        cList=[[x1,y1]]
        count = [0]
        def check(x,y,x1,y1):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 or mazeG[y][x] == 2:
                    cList.append([x,y])
                    if (x+1!=x1 or y!=y1) and (x+1 >= 0 and x+1 <dimMX and y >= 0 and y < dimMY) and (mazeG[y][x+1]==2 or mazeG[y][x+1]== 0):
                        if [x+1,y] not in cList:
                            check(x+1,y,x,y)
                        else:
                            count[0]+=1
                    if (x-1!=x1 or y!=y1) and (x-1 >= 0 and x-1 <dimMX and y >= 0 and y < dimMY) and (mazeG[y][x-1]==2 or mazeG[y][x-1]== 0):
                        if [x-1,y] not in cList:    
                            check(x-1,y,x,y)
                        else:
                            count[0]+=1
                    if (x!=x1 or y+1!=y1) and (x >= 0 and x <dimMX and y+1 >= 0 and y+1 < dimMY) and (mazeG[y+1][x]== 2 or mazeG[y+1][x]== 0):
                        if [x,y+1] not in cList:    
                            check(x,y+1,x,y)
                        else:
                            count[0]+=1
                    if (x!=x1 or y-1!=y1) and (x >= 0 and x <dimMX and y-1 >= 0 and y-1 < dimMY) and (mazeG[y-1][x]== 2 or mazeG[y-1][x]== 0):
                        if [x,y-1] not in cList:    
                            check(x,y-1,x,y)
                        else:
                            count[0]+=1
                    
        if (x+1!=x1 or y!=y1) and mazeG[y][x+1]==2:
            check(x+1,y,x,y)
        if (x-1!=x1 or y!=y1) and mazeG[y][x-1]==2:
            check(x-1,y,x,y)
        if (x!=x1 or y+1!=y1) and mazeG[y+1][x]==2:
            check(x,y+1,x,y)
        if (x!=x1 or y-1!=y1) and mazeG[y-1][x]==2:
            check(x,y-1,x,y)
        if count[0] > 0:
            return False
        else:
            return True


    def bigCheck(self,x,y):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        lList=[]
        if (x+1 >= 0 and x+1 <dimMX and y >= 0 and y < dimMY) and mazeG[y][x+1]==0:
            lList.append([x+1,y])
        if (x-1 >= 0 and x-1 <dimMX and y >= 0 and y < dimMY) and mazeG[y][x-1]==0:
            lList.append([x-1,y])
        if (x >= 0 and x <dimMX and y+1 >= 0 and y+1 < dimMY) and mazeG[y+1][x]==0:
            lList.append([x,y+1])
        if (x >= 0 and x <dimMX and y-1 >= 0 and y-1 < dimMY) and mazeG[y-1][x]==0:
            lList.append([x,y-1])

        tof = False
        for l in lList:
           if self.checkCDS(l[0],l[1],x,y) and self.deepCheck(l[0],l[1],x,y):
               tof = True
        return tof

    def CDSset(self,mazeG1):
        bList=[]
        cList=[]
        dList=[]
        dimMX = self.dimMX
        dimMY = self.dimMY
        def find(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG1[y][x] == 0 or mazeG1[y][x]== 2:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        find(x-1,y)
                        find(x+1,y)
                        find(x,y-1)
                        find(x,y+1)

        y=0
        while y < dimMY:
            x = 0
            while x < dimMX:
                if [x,y] not in dList and mazeG1[y][x] == 0:
                    find(x,y)
                    for i in cList:
                        dList.append(i)
                    bList.append(cList)
                cList=[]
                x += 1
            y += 1
        return bList

    def forward(self, mazeG, dimMY, dimMX):
        mazeG1 = copy.deepcopy(mazeG)
        cList=[]
        def change(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 :
                    if [x,y] not in cList:
                        cList.append([x,y])
                        mazeG1[y][x]=1
                        change(x-1,y)
                        change(x+1,y)
                        change(x,y-1)
                        change(x,y+1)
                elif mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        if not self.bigCheck(x,y):
                            cList.append([x,y])
                            mazeG1[y][x]=1
                            change(x-1,y)
                            change(x+1,y)
                            change(x,y-1)
                            change(x,y+1)

        aList=[]
        x = 0                
        while x < dimMX:
            if mazeG[0][x] == 2:
                aList.append([x,0])
            x += 1
        x = 0
        while x < dimMX:
            if mazeG[dimMY-1][x] == 2:
                aList.append([x,dimMY-1])
            x += 1
        y = 0    
        while y < dimMY:
            if mazeG[y][0] == 2:
                aList.append([0,y])
            y += 1
        y = 0    
        while y < dimMY:
            if mazeG[y][dimMX-1] == 2:
                aList.append([dimMX-1,y])
            y += 1

        for a in aList:
            change(a[0],a[1])
        countl = self.CDSset(mazeG1)
        for c1 in countl:
            for c2 in c1:
                if self.mazeG[c2[1]][c2[0]]==0:
                    self.mazeG[c2[1]][c2[0]]=6
        self.points=copy.deepcopy(countl)
        return (len(countl))

    def checkUE(self,x,y):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        count = [0]
        cList=[]
        def checking(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        checking(x-1,y)
                        checking(x+1,y)
                        checking(x,y-1)
                        checking(x,y+1)
            else:
                count[0] += 1
        checking(x,y)
        if count[0] == 2:
            return True
        else:
            return False

    def findUUP(self,x,y):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        bList=[]
        cList=[]
        def record(x,y):
            if x >= 0 and x <dimMX and y >= 0 and y < dimMY:
                if mazeG[y][x] == 0 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        if mazeG[y][x] == 0:
                            bList.append([x,y])
                        cList.append([x,y])
                        record(x-1,y)
                        record(x+1,y)
                        record(x,y-1)
                        record(x,y+1)
        record(x,y)
        return bList

    def checkUUP(self,x,y):
        mazeG = self.mazeG
        dimMX = self.dimMX
        dimMY = self.dimMY
        def check(x,y):
            if (x < 0 or x >=dimMX or y < 0 or y >= dimMY) or mazeG[y][x]==0:
                return True
            else:
                return False
        count = 0
        if mazeG[y+1][x] == 2:
            if check(x,y+2):
                count += 1
        if mazeG[y-1][x] == 2:
            if check(x,y-2):
                count += 1
        if mazeG[y][x+1] == 2:
            if check(x+2,y):
                count += 1
        if mazeG[y][x-1] == 2:
            if check(x-2,y):
                count += 1
        
        if count == 2:
            return True
        else:
            return False

    def findUEEP(self, mazeG, dimMY, dimMX):
        aList=[]
        x = 0                
        while x < dimMX:
            if mazeG[0][x] == 2:
                aList.append([x,0])
            x += 1
        x = 0
        while x < dimMX:
            if mazeG[dimMY-1][x] == 2:
                aList.append([x,dimMY-1])
            x += 1
        y = 0    
        while y < dimMY:
            if mazeG[y][0] == 2:
                aList.append([0,y])
            y += 1
        y = 0    
        while y < dimMY:
            if mazeG[y][dimMX-1] == 2:
                aList.append([dimMX-1,y])
            y += 1
        
        
        bList= []
        for x in aList :
            if self.checkUE(x[0],x[1]):
                cList = self.findUUP(x[0],x[1])
                ToF = True
                for y in cList:
                    if not self.checkUUP(y[0],y[1]):
                        ToF = False
                if ToF:
                    bList.append(cList)
                    
        fList = []
        for x in bList:
            for y in bList:
                if sorted(x) not in fList and sorted(x)==sorted(y):
                    fList.append(sorted(x))
        for m in fList:
            for n in m:
                self.mazeG[n[1]][n[0]] = 8
        self.UUP=copy.deepcopy(fList)
        return len(fList)




    def analyse(self):
        count = self.count
        if count ==  0:
            print('The maze has no gate.')
        elif count == 1:
            print('The maze has a single gate.')
        else:
            print(f'The maze has {count} gates.')

        countWall = self.countWall
        if countWall ==  0:
            print('The maze has no wall.')
        elif countWall == 1:
            print('The maze has walls that are all connected.')
        else:
            print(f'The maze has {countWall} sets of walls that are all connected.')

        countInner = self.countInner
        if countInner ==  0:
            print('The maze has no inaccessible inner point.')
        elif countInner == 1:
            print('The maze has a unique inaccessible inner point.')
        else:
            print(f'The maze has {countInner} inaccessible inner points.')

        countacA = self.countacA
        if countacA ==  0:
            print('The maze has no accessible area.')
        elif countacA == 1:
            print('The maze has a unique accessible area.')
        else:
            print(f'The maze has {countacA} accessible areas.')

        countCDS = self.countCDS
        if countCDS ==  0:
            print('The maze has no accessible cul-de-sac.')
        elif countCDS == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {countCDS} sets of accessible cul-de-sacs that are all connected.')
        
       
        countUEEP = self.countUEEP
        if countUEEP ==  0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif countUEEP == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {countUEEP} entry-exit paths with no intersections not to cul-de-sacs.')
        
        


    def findWline(self):
        dimMX = self.dimMX 
        dimMY = self.dimMY 
        mazeG = self.mazeG
        bList=[]
        cList=[]
        dList=[]
        def find(x,y):
            if x >= 0 and x <dimMX :
                if mazeG[y][x] == 1:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        find(x+1,y)
        bList1= []
        y=0
        while y < dimMY:
            x = 0
            while x < dimMX:
                if [x,y] not in dList and mazeG[y][x] == 1:
                    find(x,y)
                    for i in cList:
                        dList.append(i)
                    bList.append(cList)
                cList=[]
                x += 1
            line = []
            for a in bList:
                if len(a)>1:
                    l1 = copy.deepcopy(a[0])
                    l2 = copy.deepcopy(a[-1])
                    l1[0],l1[1] = int(l1[0]/2),int(l1[1]/2)
                    l2[0],l2[1] = int(l2[0]/2),int(l2[1]/2)
                    line.append([l1,l2])
            if line !=[]:
                bList1.append(line)
            y+=2
            bList=[]
        return bList1

    def findWcol(self):
        dimMX = self.dimMX 
        dimMY = self.dimMY 
        mazeG = self.mazeG
        bList=[]
        cList=[]
        dList=[]
        def find(x,y):
            if y >= 0 and y <dimMY :
                if mazeG[y][x] == 1:
                    if [x,y] not in cList:
                        cList.append([x,y])
                        find(x,y+1)
        bList1= []
        x=0
        while x < dimMX:
            y = 0
            while y < dimMY:
                if [x,y] not in dList and mazeG[y][x] == 1:
                    find(x,y)
                    for i in cList:
                        dList.append(i)
                    bList.append(cList)
                cList=[]
                y += 1
            line = []
            for a in bList:
                if len(a)>1:
                    l1 = copy.deepcopy(a[0])
                    l2 = copy.deepcopy(a[-1])
                    l1[0],l1[1] = int(l1[0]/2),int(l1[1]/2)
                    l2[0],l2[1] = int(l2[0]/2),int(l2[1]/2)
                    line.append([l1,l2])
            if line !=[]:        
                bList1.append(line)
            x+=2
            bList=[]
        return bList1

    def findPillar(self):
        dimMY = self.dimMY
        dimMX = self.dimMX
        mazeG = self.mazeG
        bList=[]
        y=0
        while y < dimMY:
            x = 0
            while x < dimMX:
                if mazeG[y][x] == 3:
                    bList.append([x,y])
                x += 1
            y+=2
        bList1 =[]
        for x in bList:
            a1 = int(x[0]/2)
            a2 = int(x[1]/2)
            bList1.append([a1,a2])
        bList1=sorted(bList1,key=(lambda x: [x[1],x[0]]))
        return bList1

    def findCDSS(self):
        wList=[]
        for p in self.points:
            for x in p:
                if self.mazeG[x[1]][x[0]] == 6:
                    wList.append([x[0],x[1]])
        fList=[]
        for p in wList:
            l1 = p[0]/2
            l2 = p[1]/2
            fList.append([l1,l2])
        fList=sorted(fList,key=(lambda x: [x[1],x[0]]))
        return fList

    def changeUUP(self):
        dimMX = self.dimMX 
        dimMY = self.dimMY 
        mazeG = self.mazeG
        bList=[]
        cList=[]
        dList=[]
        aList=[]
        def find(x,y):
            if x >= 0 and x <dimMX :
                if mazeG[y][x] == 8 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        if mazeG[y][x] == 8:
                            aList.append([x,y])
                        cList.append([x,y])
                        find(x-1,y)
                        find(x+1,y)
            else:
                aList.append([x,y])
        y=1
        while y < dimMY:
            x = 1
            while x < dimMX:
                if [x,y] not in dList and mazeG[y][x] == 8:
                    find(x,y)
                    for i in aList:
                        dList.append(i)
                    bList.append(aList)
                cList=[]
                aList=[]
                x += 2
            y += 2
        bList1= []
        for b in bList:
            bList1.append(sorted(b))
        bList2= []
        for b in bList1:
            if len(b)>=3:
                bList2.append([b[0],b[-1]])
            elif len(b)==2:
                bList2.append([b[0],b[1]])
        fList = []
        for x in bList2:
            line=[]
            for y in x:
                l1 = y[0]/2
                l2 = y[1]/2
                line.append([l1,l2])
            fList.append(line)
        return(fList)

    def rowUUP(self):
        dimMX = self.dimMX 
        dimMY = self.dimMY 
        mazeG = self.mazeG
        bList=[]
        cList=[]
        dList=[]
        aList=[]
        def find(x,y):
            if y >= 0 and y <dimMY :
                if mazeG[y][x] == 8 or mazeG[y][x] == 2:
                    if [x,y] not in cList:
                        if mazeG[y][x] == 8:
                            aList.append([x,y])
                        cList.append([x,y])
                        find(x,y-1)
                        find(x,y+1)
            else:
                aList.append([x,y])
        x=1
        while x < dimMX:
            y = 1
            while y < dimMY:
                if [x,y] not in dList and mazeG[y][x] == 8:
                    find(x,y)
                    for i in aList:
                        dList.append(i)
                    bList.append(aList)
                cList=[]
                aList=[]
                y += 2
            x += 2
        bList1= []
        for b in bList:
            bList1.append(sorted(b))
        bList2= []
        for b in bList1:
            if len(b)>=3:
                bList2.append([b[0],b[-1]])
            elif len(b)==2:
                bList2.append([b[0],b[1]])
        fList = []
        for x in bList2:
            line=[]
            for y in x:
                l1 = y[0]/2
                l2 = y[1]/2
                line.append([l1,l2])
            fList.append(line)
        return(fList)
        
    def combineUUP(self,list1,list2):
        for x in list2:
            list1.append(x)
        return list1

    def display(self):
        f1=self.filename.split('.')
        with open(f1[0]+'.tex','w',newline='') as f:
            f.writelines('\\documentclass[10pt]{article}\n')
            f.writelines('\\usepackage{tikz}\n')
            f.writelines('\\usetikzlibrary{shapes.misc}\n')
            f.writelines('\\usepackage[margin=0cm]{geometry}\n')
            f.writelines('\\pagestyle{empty}\n')
            f.writelines('\\tikzstyle{every node}=[cross out, draw, red]\n')
            f.writelines('\n')
            f.writelines('\\begin{document}\n')
            f.writelines('\n')
            f.writelines('\\vspace*{\\fill}\n')
            f.writelines('\\begin{center}\n')
            f.writelines('\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n')
            wallline=self.findWline()
            wallcol=self.findWcol()
            f.writelines('% Walls\n')
            if len(wallline)!=0:
                for x in wallline:
                    for y in x:
                        f.writelines(f'    \\draw ({y[0][0]},{y[0][1]}) -- ({y[1][0]},{y[1][1]});\n')
            if len(wallcol)!=0:
                for x in wallcol:
                    for y in x:
                        f.writelines(f'    \\draw ({y[0][0]},{y[0][1]}) -- ({y[1][0]},{y[1][1]});\n')

            pillar=self.findPillar()
            f.writelines('% Pillars\n')
            for x in pillar:
                f.writelines(f'    \\fill[green] ({x[0]},{x[1]}) circle(0.2);\n')
            f.writelines('% Inner points in accessible cul-de-sacs\n')
            CDS  = self.findCDSS()
            if len(CDS) !=0:
                for c in CDS:
                    f.writelines(f'    \\node at ({c[0]},{c[1]}) {{}};\n')
            f.writelines('% Entry-exit paths without intersections\n')
            UUP=self.combineUUP(self.changeUUP(),self.rowUUP())
            for u in UUP:
                f.writelines(f'    \\draw[dashed, yellow] ({u[0][0]},{u[0][1]}) -- ({u[1][0]},{u[1][1]});\n')
            f.writelines('\\end{tikzpicture}\n')
            f.writelines('\\end{center}\n')
            f.writelines('\\vspace*{\\fill}\n')
            f.writelines('\n')
            f.writelines('\\end{document}\n')
        # REPLACE PASS ABOVE WITH YOUR CODE

try:
    maze = Maze('maze_13.txt')
    maze.analyse()
    maze.display()
except MazeError as e:
    print(e) 
