# Author: Github ID: q5kang
# Date created: July 19, 2019

import arcpy
import time
import numpy
startTime = time.time()
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")

#Local variables for 1b
nelu95__2_ = "C:\\Users\\q5kang"

## Insert your local GIS file here to get the highest point, at least 2 suitability layers are needed.


# Make sure to convert your data type to raster
sDevRas = arcpy.Raster("")

Dev_sliceA = arcpy.RasterToNumPyArray(sDevRas)

# Example of the other layers
suitNatA = arcpy.RasterToNumPyArray(sNatRas)
SuitSliceAgrA = arcpy.RasterToNumPyArray(sAgrRas)

nRows = SuitSliceAgrA.shape[0]
nCols = Dev_sliceA.shape[1]
nMean = SuitSliceAgrA.mean()
dMean = Dev_sliceA.mean()
nnMean = suitNatA.mean()
nStd = SuitSliceAgrA.std()

tmplist = []

for row in range(0, nRows):
    for col in range(0, nCols):
        suita = max(Dev_sliceA[row,col], suitNatA[row,col], SuitSliceAgrA[row,col])
        tmplist.append(suita)
        
newarray = numpy.asarray(tmplist)
newarray = newarray.reshape(nRows, nCols)

#convert the resulting array back to a raster
future = arcpy.NumPyArrayToRaster(newarray, arcpy.Point(sNatRas.extent.XMin, sDevRas.extent.YMin), sNatRas.meanCellWidth, sNatRas.meanCellHeight)

#set the spatial reference to match the original raster
arcpy.DefineProjection_management(future, sNatRas)

# save to your destination
future.save("C:\\Users")
        

# Process: Reclassify (5)
arcpy.gp.Reclassify_sa(nestream, "VALUE", "6 0;6 7 0;7 8 0;NODATA 1", Reclass_stream, "DATA")

# Process: Reclassify (3)
arcpy.gp.Reclassify_sa(nelu95__2_, "VALUE", "111 194 0;194 429 1;429 625 0", reclass_nelu95_avail, "DATA")

# Process: Times
arcpy.gp.Times_sa(reclass_nelu95_avail, Reclass_stream, Times_nelu95_avastream)

# Process: Reclassify
arcpy.Reclassify_3d(nelu95, "VALUE", "111 200 1;200 300 2;300 625 3", Nelu_relassified, "DATA")


# Process: Over
arcpy.gp.Over_sa(future, Nelu_relassified, Over_futureland) 

# Process: Times (2)
arcpy.gp.Times_sa(Times_nelu95_avastream, Over_futureland, Times2)

# Process: Reclassify (4)
arcpy.Reclassify_3d(Times2, "VALUE", "0 NODATA;0 1 1;1 2 2;2 3 3", Reclass_Time2, "DATA")

# Process: Slice
arcpy.Slice_3d(Reclass_Time2, Slice_futureland, "100", "EQUAL_AREA", "1")

#conflict

tmplist2 = []

for r in range(0, nRows):
    for c in range(0, nCols):
        if ((Dev_sliceA[r,c] > dMean) and (suitNatA[r,c] > nnMean)):
            tmplist2.append(1)
        elif ((Dev_sliceA[r,c] > dMean) and (SuitSliceAgrA[r,c] > nMean)):
            tmplist2.append(1)
        elif ((suitNatA[r,c] > nnMean) and (SuitSliceAgrA[r,c] > nMean)):
            tmplist2.append(1)
        else:
            tmplist2.append(0)
        
newarray2 = numpy.asarray(tmplist2)
newarray2 = newarray2.reshape(nRows, nCols)

#convert the resulting array back to a raster
conflict = arcpy.NumPyArrayToRaster(newarray2, arcpy.Point(sNatRas.extent.XMin, sDevRas.extent.YMin), sNatRas.meanCellWidth, sNatRas.meanCellHeight)

#set the spatial reference to match the original raster
arcpy.DefineProjection_management(conflict, sNatRas)

conflict.save(r"C:")
