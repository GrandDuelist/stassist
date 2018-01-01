class CPSSpatio():
    def __init__(self,grid_shape=None):
        self.grid_shape = (50,50)
        if grid_shape:
            self.grid_shape = grid_shape
        self.regions = {}
        self.grids = []
        self.grid_regions = {}
        self.init()

    def init(self,out_edge_regions):
        self.initSpatioRegion(out_edge_regions)
        (minx,miny,maxx,maxy) = self.getRectBoundaryFromRegions(self.regions)
        self.initSpatioRectBoundary(minx,maxx,miny,maxy)
        self.initRectToPolygonMapping()

    
    def initSpatioRegion(self,out_edge):
        for one_region in out_edge:
            geo_id = one_region['geo_id']; geo_array = one_region['geo_array']
            self.regions[geo_id] = geo_array

    def getRectBoundaryFromRegions(self,regions):
        minx,miny,maxx,maxy = float('inf'),float('inf'),0,0
        for k,region in regions:
            for point in regions:
                [x,y] = regions
                if x > maxx: maxx = x
                if x < minx: minx = x
                if y > maxy: maxy = y
                if y < miny: miny = y
        return(minx,miny,maxx,maxy)
        
    def initSpatioRectBoundary(self,minx,maxx,miny,maxy):
        self.minmax = (minx,maxx,miny,maxy)
        (xshape,yshape) = self.grid_shape
        (xstep,ystep) = ((maxx - minx)/float(xshape),(maxy-miny)/float(yshape))
        self.step = (xstep,ystep)

    def initRectToPolygonMapping(self):
        (minx,maxx,miny,maxy) = self.minmax
        (xshape,yshape) = self.grid_shape
        self.grid_regions = [[]*xshape for ii in xrange(yshape)]
        for k,v in self.regions:
            for point in v:
                (x,y) = (((point[0]-minx)/self.xstep),((point[1]-miny)/self.ystep))
                self.grid_regions[x][y].append(k)
    def pointToGridIndex(self):
        (x,y) = (((point[0]-minx)/self.xstep),((point[1]-miny)/self.ystep))
        return(x,y)
     
    def findCandidatesInGrids(self,point):
        (x,y) = self.pointToGridIndex(point)
        candidates = self.grid_regions[x][y]
        return(candidates)

    def pnpoly(self,polygon,point):
        n=len(polygon);i,j,c = 0,n-1,False;(testx,testy) = (float(point[0]),float(point[1]))
        while(i < n):
            (currentxi,currentyi) = (float(polygon[i][0]),float(polygon[i][1]))
            (currentxj,currentyj) = (float(polygon[j][0]),float(polygon[j][1]))
            if ((currentyi > testy) != (currentyj > testy)) and (testx < (currentxj - currentxi) * (testy-currentyi) / (currentyj - currentyi) + currentxi):
                c = not c
            j = i
            i += 1
        return(c)

    def findPointRegionID(self,point):
        candidates = self.findCandidatesInGrids(point)
        regionid = self.searchPointInRegions(point,candidates)
        if regionid:
            return(regionid)
        else:
            return(self.searchPointInRegions(point,self.regions.keys()))

    def searchPointInRegions(self,point,candidates):
        for onekey in candidates:
            polygon = self.regions[onekey]
            if self.pnppoly(polygon,point):
                return(onekey)
        return(None)
def minmaxGeoJson(geojson_path):
    file_path = geojson_path
    # file_path = 'shenzhen_boundary_gps.geoJson'
    data = json.load(open(file_path))
    coordinates = data['coordinates'][0]
    minx=miny=100000; maxx=maxy = 0;
    for point in coordinates:
        (x,y) = point
        minx = min(minx,x);maxx = max(maxx,x);miny=min(miny,y);maxy=max(maxy,y)
    print("minx = "+str(minx)+" maxx = " + str(maxx) + " miny = " + str(miny) + " maxy = "+str(maxy))        

class CSPCrop():
    def setRectangle(self,minx,miny,maxx,maxy):
        self.minx = minx; self.miny = miny; self.maxx = maxx; self.maxy = maxy
    def isInRectangle(self,x,y):
        isx = (x >= self.minx and x <= self.maxx)
        isy = (y >= self.miny and y <= self.maxy)
        return(isx and isy)
    def setShenzhenRectangle(self):
        self.setRectangle(113.7463515,114.6237079,22.4415225,22.8644043)
    