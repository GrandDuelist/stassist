from cpsspatio import *
#p1 = (21.0122287,52.2296756)
#p2 = (16.9251681,52.406374)
#cpsdistance = CPSDistance()
#r = cpsdistance.GPSDist(p1,p2)
def testCPSCrop():
    cpscrop = CPSCrop()
    cpscrop.setShenzhenPolygonBoundary()
    b = cpscrop.isInPolygon(114.0508539, 22.5463145)

def testGeoJsonMultiplePolygon():
    cpsspatio = CPSSpatio()
    aa = simplejson.load(open('C:\Users\zhiha\Downloads\china.json'))
    cpsspatio.setGeoJsonMultiplePolygon(aa)
    cpsspatio.findPointInPolygonJson((118.4187,28.2968))

def testGridCount():
    cpsspatio = CPSSpatio()
    cpsspatio.initSpatioRectBoundary(113.7463515,114.6237079,22.4415225,22.8644043)
    result = cpsspatio.countInGrid([114.23,113.94,114.312,114.11],[22.55,22.65,22.71,22.48],[1,3,4,5])
    print(cpsspatio.grid_location)
    #print(result)

testGridCount()
