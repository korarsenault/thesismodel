import os
from numpy import *
import arcpy
from arcpy.sa import *

gdb_worksp = arcpy.GetParameterAsText(10)
arcpy.env.workspace = gdb_worksp

#defining variables
schema = arcpy.GetParameterAsText(0)
boundary = arcpy.GetParameterAsText(1)
schools = arcpy.GetParameterAsText(2)
libs = arcpy.GetParameterAsText(3)
parks = arcpy.GetParameterAsText(4)
polling = arcpy.GetParameterAsText(5)
medical = arcpy.GetParameterAsText(6)
grocery = arcpy.GetParameterAsText(7)
transit = arcpy.GetParameterAsText(8)

#making sure everything is in the right coordinate reference system
SRtxt = arcpy.GetParameterAsText(9)
SR = arcpy.SpatialReference()
SR.loadFromString(SRtxt)
arcpy.management.DefineProjection(schools, SR)
arcpy.management.DefineProjection(libs, SR)
arcpy.management.DefineProjection(parks, SR)
arcpy.management.DefineProjection(polling, SR)
arcpy.management.DefineProjection(medical, SR)
arcpy.management.DefineProjection(grocery, SR)
arcpy.management.DefineProjection(transit, SR)

#feature to point for initial schema
schemapoints = arcpy.management.FeatureToPoint(schema, 'BlockGroupsPoints')

schemapoints1 = arcpy.analysis.Near(schemapoints, schools, search_radius="",
                                    location="NO_LOCATION", angle="NO_ANGLE",
                                    method="GEODESIC", 
                                    field_names=[["NEAR_FID", "NEAR_FID_SCHOOLS"],
                                                 ["NEAR_DIST", "NEAR_DIST_SCHOOLS"]])
                                             
schemapoints2 = arcpy.analysis.Near(schemapoints1, libs, search_radius="", 
                                    location="NO_LOCATION", angle="NO_ANGLE",
                                    method="GEODESIC", 
                                    field_names=[["NEAR_FID", "NEAR_FID_LIBS"],
                                                 ["NEAR_DIST", "NEAR_DIST_LIBS"]])
   
schemapoints3 = arcpy.analysis.Near(schemapoints2, parks, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="GEODESIC", field_names=[["NEAR_FID", "NEAR_FID_PARKS"], ["NEAR_DIST", "NEAR_DIST_PARKS"]] )
schemapoints4 = arcpy.analysis.Near(schemapoints3, polling, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="GEODESIC", field_names=[["NEAR_FID", "NEAR_FID_POLLING"], ["NEAR_DIST", "NEAR_DIST_POLLING"]] )
schemapoints5 = arcpy.analysis.Near(schemapoints4, medical, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="GEODESIC", field_names=[["NEAR_FID", "NEAR_FID_MEDICAL"], ["NEAR_DIST", "NEAR_DIST_MEDICAL"]] )
schemapoints6 = arcpy.analysis.Near(schemapoints5, grocery, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="GEODESIC", field_names=[["NEAR_FID", "NEAR_FID_GROCERY"], ["NEAR_DIST", "NEAR_DIST_GROCERY"]] )
schemapoints7 = arcpy.analysis.Near(schemapoints6, transit, search_radius="", location="NO_LOCATION", angle="NO_ANGLE", method="GEODESIC", field_names=[["NEAR_FID", "NEAR_FID_TRANSIT"], ["NEAR_DIST", "NEAR_DIST_TRANSIT"]] )
arcpy.management.CopyFeatures(schemapoints7, 'schemapoints')
schemapoints="schemapoints"

milecode = """
def mile(x):
    if x > 0:
        return x / 1609 
    else:
        return '0'
"""

#calculate near distance in miles from meters

schemapointsdist = arcpy.management.CalculateFields(schemapoints, "", [["NEAR_DIST_SCHOOLS", "mile(!NEAR_DIST_SCHOOLS!)"],
                                                    ["NEAR_DIST_LIBS", "mile(!NEAR_DIST_LIBS!)"],
                                                    ["NEAR_DIST_PARKS", "mile(!NEAR_DIST_PARKS!)"],
                                                    ["NEAR_DIST_POLLING", "mile(!NEAR_DIST_POLLING!)"],
                                                    ["NEAR_DIST_MEDICAL", "mile(!NEAR_DIST_MEDICAL!)"],
                                                    ["NEAR_DIST_GROCERY", "mile(!NEAR_DIST_GROCERY!)"],
                                                    ["NEAR_DIST_TRANSIT", "mile(!NEAR_DIST_TRANSIT!)"]], milecode,
                                                    enforce_domains="NO_ENFORCE_DOMAINS")

arcpy.management.CopyFeatures(schemapointsdist, 'schemapointsmile', "", "", "", "")
schemapointsmile="schemapointsmile"

#add fields of bike, ped, scooter category

#Set fieldname variables

field_name1 = "SCHOOL_DIST_CAT_PED"
field_name2 = "LIB_DIST_CAT_PED"
field_name3 = "PARK_DIST_CAT_PED"
field_name4 = "POLL_DIST_CAT_PED"
field_name5 = "MED_DIST_CAT_PED"
field_name6 = "GROCERY_DIST_CAT_PED"
field_name7 = "TRANSIT_DIST_CAT_PED"
field_name8 = "SCHOOL_DIST_CAT_BIKE"
field_name9 = "LIB_DIST_CAT_BIKE"
field_name10 = "PARK_DIST_CAT_BIKE"
field_name11 = "POLL_DIST_CAT_BIKE"
field_name12 = "MED_DIST_CAT_BIKE"
field_name13 = "GROCERY_DIST_CAT_BIKE"
field_name14 = "TRANSIT_DIST_CAT_BIKE"
field_name15 = "SCHOOL_DIST_CAT_ESCOOTER"
field_name16 = "LIB_DIST_CAT_ESCOOTER"
field_name17 = "PARK_DIST_CAT_ESCOOTER"
field_name18 = "POLL_DIST_CAT_ESCOOTER"
field_name19 = "MED_DIST_CAT_ESCOOTER"
field_name20 = "GROCERY_DIST_CAT_ESCOOTER"
field_name21 = "TRANSIT_DIST_CAT_ESCOOTER"


#Add the fields one at a time 
pointsaddfield = arcpy.AddField_management(schemapointsmile,field_name1,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield1 = arcpy.AddField_management(pointsaddfield,field_name2,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield2 = arcpy.AddField_management(pointsaddfield1,field_name3,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield3 = arcpy.AddField_management(pointsaddfield2,field_name4,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield4 = arcpy.AddField_management(pointsaddfield3,field_name5,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield5 = arcpy.AddField_management(pointsaddfield4,field_name6,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield6 = arcpy.AddField_management(pointsaddfield5,field_name7,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield7 = arcpy.AddField_management(pointsaddfield6,field_name8,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield8 = arcpy.AddField_management(pointsaddfield7,field_name9,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield9 = arcpy.AddField_management(pointsaddfield8,field_name10,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield10 = arcpy.AddField_management(pointsaddfield9,field_name11,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield11 = arcpy.AddField_management(pointsaddfield10,field_name12,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield12 = arcpy.AddField_management(pointsaddfield11,field_name13,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield13 = arcpy.AddField_management(pointsaddfield12,field_name14,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield14 = arcpy.AddField_management(pointsaddfield13,field_name15,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield15 = arcpy.AddField_management(pointsaddfield14,field_name16,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield16 = arcpy.AddField_management(pointsaddfield15,field_name17,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield17 = arcpy.AddField_management(pointsaddfield16,field_name18,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield18 = arcpy.AddField_management(pointsaddfield17,field_name19,"FLOAT", "", "", "", "", "", "", "")
pointsaddfield19 = arcpy.AddField_management(pointsaddfield18,field_name20,"FLOAT", "", "", "", "", "", "", "")
schemapointsaddcat = arcpy.AddField_management(pointsaddfield19,field_name21,"FLOAT", "", "", "", "", "", "", "")
arcpy.management.CopyFeatures(schemapointsaddcat, 'schema_addcat', "", "", "", "")


schema_addcat="schema_addcat"

ped="""
def ped(x):
     if x < 1.0:
         return '1'
     else:
         return '0'
"""

escoot="""
def escoot(x):
     if x < 3.75:
         return '1'
     else:
         return '0'
"""

bike="""
def bike(x):
    if x < 2.5:
         return '1'
    else:
         return '0'"""

#calculate binary distance for each category
schemapointsaddcat2 = arcpy.management.CalculateFields(schema_addcat, "", [["SCHOOL_DIST_CAT_PED", "ped(!NEAR_DIST_SCHOOLS!)"],
                                                                          ["LIB_DIST_CAT_PED", "ped(!NEAR_DIST_LIBS!)"],
                                                                          ["PARK_DIST_CAT_PED", "ped(!NEAR_DIST_PARKS!)"], 
                                                                          ["POLL_DIST_CAT_PED", "ped(!NEAR_DIST_POLLING!)" ],
                                                                          ["MED_DIST_CAT_PED", "ped(!NEAR_DIST_MEDICAL!)"], 
                                                                          ["GROCERY_DIST_CAT_PED", "ped(!NEAR_DIST_GROCERY!)"], 
                                                                          ["TRANSIT_DIST_CAT_PED", "ped(!NEAR_DIST_TRANSIT!)"]],
                                                                          ped, enforce_domains="NO_ENFORCE_DOMAINS")

schemapointsaddcat3 = arcpy.management.CalculateFields(schemapointsaddcat2, "", [["SCHOOL_DIST_CAT_BIKE", "bike(!NEAR_DIST_SCHOOLS!)"],
                                                                                 ["LIB_DIST_CAT_BIKE", "bike(!NEAR_DIST_LIBS!)"],
                                                                                 ["PARK_DIST_CAT_BIKE", "bike(!NEAR_DIST_PARKS!)"], 
                                                                                 ["POLL_DIST_CAT_BIKE", "bike(!NEAR_DIST_POLLING!)" ],
                                                                                 ["MED_DIST_CAT_BIKE", "bike(!NEAR_DIST_MEDICAL!)"], 
                                                                                 ["GROCERY_DIST_CAT_BIKE", "bike(!NEAR_DIST_GROCERY!)"], 
                                                                                 ["TRANSIT_DIST_CAT_BIKE", "bike(!NEAR_DIST_TRANSIT!)"]],
                                                                                bike, enforce_domains="NO_ENFORCE_DOMAINS")


bgpoints = arcpy.management.CalculateFields(schemapointsaddcat3, "", [["SCHOOL_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_SCHOOLS!)"], 
                                                                     ["LIB_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_LIBS!)"], 
                                                                     ["PARK_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_PARKS!)"], 
                                                                     ["POLL_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_POLLING!)"], 
                                                                     ["MED_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_MEDICAL!)"], 
                                                                     ["GROCERY_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_GROCERY!)"], 
                                                                     ["TRANSIT_DIST_CAT_ESCOOTER", "escoot(!NEAR_DIST_TRANSIT!)"]],
                                                                     escoot, enforce_domains="NO_ENFORCE_DOMAINS")

arcpy.management.CopyFeatures(bgpoints, 'bgpoints', "", "", "", "")


#features to raster
arcpy.conversion.FeatureToRaster(bgpoints, "SCHOOL_DIST_CAT_PED", "SCHOOL_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "LIB_DIST_CAT_PED", "LIB_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "PARK_DIST_CAT_PED", "PARK_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "POLL_DIST_CAT_PED", "POLL_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "MED_DIST_CAT_PED", "MED_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "GROCERY_DIST_CAT_PED", "GROCERY_DIST_CAT_PED_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "TRANSIT_DIST_CAT_PED", "TRANSIT_DIST_CAT_PED_RASTER")

arcpy.conversion.FeatureToRaster(bgpoints, "SCHOOL_DIST_CAT_BIKE", "SCHOOL_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "LIB_DIST_CAT_BIKE", "LIB_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "PARK_DIST_CAT_BIKE", "PARK_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "POLL_DIST_CAT_BIKE", "POLL_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "MED_DIST_CAT_BIKE", "MED_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "GROCERY_DIST_CAT_BIKE", "GROCERY_DIST_CAT_BIKE_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "TRANSIT_DIST_CAT_BIKE", "TRANSIT_DIST_CAT_BIKE_RASTER")

arcpy.conversion.FeatureToRaster(bgpoints, "SCHOOL_DIST_CAT_ESCOOTER", "SCHOOL_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "LIB_DIST_CAT_ESCOOTER", "LIB_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "PARK_DIST_CAT_ESCOOTER", "PARK_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "POLL_DIST_CAT_ESCOOTER", "POLL_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "MED_DIST_CAT_ESCOOTER", "MED_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "GROCERY_DIST_CAT_ESCOOTER", "GROCERY_DIST_CAT_ESCOOTER_RASTER")
arcpy.conversion.FeatureToRaster(bgpoints, "TRANSIT_DIST_CAT_ESCOOTER", "TRANSIT_DIST_CAT_ESCOOTER_RASTER")

val1 = arcpy.GetParameterAsText(11)
val2 = arcpy.GetParameterAsText(12)
val3 = arcpy.GetParameterAsText(13)
val4 = arcpy.GetParameterAsText(14)
val5 = arcpy.GetParameterAsText(15)
val6 = arcpy.GetParameterAsText(16)
val7 = arcpy.GetParameterAsText(17)


#ped weighted sum
wsumobj1 = WSTable([["SCHOOL_DIST_CAT_PED_RASTER", "VALUE", val1],
                                      ["PARK_DIST_CAT_PED_RASTER", "VALUE", val2],
                                      ["POLL_DIST_CAT_PED_RASTER", "VALUE", val4],
                                      ["MED_DIST_CAT_PED_RASTER", "VALUE",val5],
                                      ["GROCERY_DIST_CAT_PED_RASTER", "VALUE", val6],
                                      ["TRANSIT_DIST_CAT_PED_RASTER", "VALUE", val7],
                                      ["LIB_DIST_CAT_PED_RASTER", "VALUE", val3]])

outWeightedSum1 = WeightedSum(wsumobj1)

ped = outWeightedSum1.save(gdb_worksp + '\\' + "Weighted_Ped_Raster_Tool")

#bike weighted sum
wsumobj2 = WSTable([["SCHOOL_DIST_CAT_BIKE_RASTER", "VALUE", val1],
                                      ["LIB_DIST_CAT_BIKE_RASTER", "VALUE", val3],
                                      ["PARK_DIST_CAT_BIKE_RASTER", "VALUE", val2],
                                      ["POLL_DIST_CAT_BIKE_RASTER", "VALUE", val4],
                                      ["MED_DIST_CAT_BIKE_RASTER", "VALUE", val5],
                                      ["GROCERY_DIST_CAT_BIKE_RASTER", "VALUE", val6],
                                      ["TRANSIT_DIST_CAT_BIKE_RASTER", "VALUE", val7]])

outWeightedsum2 = WeightedSum(wsumobj2)

bike = outWeightedSum2.save(gdb_worksp + '\\' + "Weighted_Bike_Raster_Tool")



#escoot weighted sum
wsumobj3 = WSTable([["SCHOOL_DIST_CAT_ESCOOTER_RASTER", "VALUE", val1],
                                      ["LIB_DIST_CAT_ESCOOTER_RASTER", "VALUE", val3],
                                      ["PARK_DIST_CrAT_ESCOOTER_RASTER", "VALUE", val2],
                                      ["POLL_DIST_CAT_ESCOOTER_RASTER", "VALUE", val4],
                                      ["MED_DIST_CAT_ESCOOTER_RASTER", "VALUE", val5],
                                      ["GROCERY_DIST_CAT_ESCOOTER_RASTER", "VALUE", val6],
                                      ["TRANSIT_DIST_CAT_ESCOOTER_RASTER", "VALUE", val7]])

outWeightedsum3 = WeightedSum(wsumobj3)

escoot = outWeightedSum3.save(gdb_worksp + '\\' +"Weighted_Escoot_Raster_Tool")


#raster to points
arcpy.conversion.RasterToPoint(ped, "PedRasterPoints")
arcpy.conversion.RasterToPoint(bike, "BikeRasterPoints")
arcpy.conversion.RasterToPoint(escoot, "EscootRasterPoints")

#spatial join
arcpy.analysis.SpatialJoin(schema, "PedRasterPoints", "PedInBlocks", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")
arcpy.analysis.SpatialJoin(schema, "BikeRasterPoints", "BikeInBlocks", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")
arcpy.analysis.SpatialJoin(schema, "EscootRasterPoints", "ScootInBlocks", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")

#spatial join
arcpy.analysis.SpatialJoin("PedInBlocks", bgpoints,"PedRasterDistance", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")
arcpy.analysis.SpatialJoin("BikeInBlocks", bgpoints, "BikeRasterDistance", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")
arcpy.analysis.SpatialJoin("ScootInBlocks", bgpoints, "ScootRasterDistance", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")

#alter fields
arcpy.management.AlterField("PedRasterDistance", "GRID_CODE", "PEDESTRIAN_DISTANCE_RANK", "PEDESTRIAN_DISTANCE_RANK", "", "","" , "")
arcpy.management.AlterField("BikeRasterDistance", "GRID_CODE", "BIKE_DISTANCE_RANK", "BIKE_DISTANCE_RANK", "", "", "", "")
arcpy.management.AlterField("ScootRasterDistance", "GRID_CODE", "ESCOOTER_DISTANCE_RANK", "ESCOOTER_DISTANCE_RANK", "", "", "", "")

#join bike ped
arcpy.management.JoinField("PedRasterDistance", "OBJECTID", "BikeRasterDistance", "OBJECTID", "BIKE_DISTANCE_RANK", "", "")

#join combine
final1=arcpy.management.JoinField("PedRasterDistance", "OBJECTID", "ScootRasterDistance", "OBJECTID", "ESCOOTER_DISTANCE_RANK", "", "")

#copy features
final3=arcpy.management.CopyFeatures(final1, "IndividualIndex", "", "", "", "")

#weighted sum

val8 = arcpy.GetParameterAsText(18)
val9 = arcpy.GetParameterAsText(19)
val10 = arcpy.GetParameterAsText(20)

wsumobj4 = WSTable([["Weighted_Ped_Raster_Tool", "VALUE", val8],
                                      ["Weighted_Bike_Raster_Tool", "VALUE", val9],
                                      ["Weighted_Escoot_Raster_Tool", "VALUE", val10]])

outWeightedsum4 = WeightedSum(wsumobj4)


agg_weight = outWeightedSum4.save(gdb_worksp + '\\' + "Agg_Weight")


#raster to point
arcpy.conversion.RasterToPoint(agg_weight, "AggregateRasterPoints", "VALUE")

#spatial join
arcpy.analysis.SpatialJoin(schema, "AggregateRasterPoints", "AggregateRasterPointsinSchema", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")

#spatial join
arcpy.analysis.SpatialJoin("AggregateRasterPointsinSchema", bgpoints, "AggregateIndex", "JOIN_ONE_TO_ONE", "", "", "CONTAINS", "", "")

#alter field
final2 = arcpy.management.AlterField("AggregateIndex", "GRID_CODE", "AggregateRanking", "AggregateRanking", "", "", "", "")
