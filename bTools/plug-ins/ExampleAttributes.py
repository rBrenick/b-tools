#
# Creation Date: 11 February 2010
#
# Description:
#	Trivial extension of MPxObjectSet
#

import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import math, sys

kNodeName = "myCustomNode"
kNodeId = OpenMaya.MTypeId(0x84012)


kDefaulBoolAttrValue = True
kDefaultEnumAttrValue = 0
kDefaultNumericAttrIntValue = 0
kDefaultNumericAttrFloatValue = 0.0
kDefaultStringAttrValue = "default"


# Node definition
class myCustomNode(OpenMayaMPx.MPxObjectSet):
    def __init__(self):
        OpenMayaMPx.MPxObjectSet.__init__(self)

    aMessageAttr = OpenMaya.MObject()
    aMessageAttrMulti = OpenMaya.MObject()
    aBooleanAttr = OpenMaya.MObject()
    aEnumAttr = OpenMaya.MObject()
    aNumericAttrInt = OpenMaya.MObject()
    aNumericAttrFloat = OpenMaya.MObject()
    aStringAttr = OpenMaya.MObject()


# creator
def nodeCreator():
    return OpenMayaMPx.asMPxPtr(myCustomNode())


# initializer
def nodeInitializer():

    # msg attr
    msgAttr = OpenMaya.MFnMessageAttribute()
    myCustomNode.aMessageAttr = msgAttr.create("messageAttr", "msga")
    myCustomNode.addAttribute(myCustomNode.aMessageAttr)

    # msg attr (multi)
    msgAttrMulti = OpenMaya.MFnMessageAttribute()
    myCustomNode.aMessageAttrMulti = msgAttrMulti.create("messageAttrMulti", "msgam")
    msgAttrMulti.setArray(True)
    myCustomNode.addAttribute(myCustomNode.aMessageAttrMulti)

    # boolean attr
    booleanAttr = OpenMaya.MFnNumericAttribute()
    myCustomNode.aBoolAttr = booleanAttr.create("booleanAttr", "ba", OpenMaya.MFnNumericData.kBoolean)
    booleanAttr.setHidden(False)
    booleanAttr.setKeyable(True)
    myCustomNode.addAttribute(myCustomNode.aBoolAttr)

    #enum attr
    enumAttr = OpenMaya.MFnEnumAttribute()
    myCustomNode.aEnumAttr = enumAttr.create("enumAttr", "ea", kDefaultEnumAttrValue)
    enumAttr.addField("enum1", 0)
    enumAttr.addField("enum2", 1)
    enumAttr.addField("enum3", 2)
    enumAttr.setHidden(False)
    enumAttr.setKeyable(True)
    myCustomNode.addAttribute(myCustomNode.aEnumAttr)

    # numeric int attr
    numericAttrInt = OpenMaya.MFnNumericAttribute()
    myCustomNode.aNumericAttrInt = numericAttrInt.create("numericAttrInt", "nai", OpenMaya.MFnNumericData.kInt, kDefaultNumericAttrIntValue)
    numericAttrInt.setHidden(False)
    numericAttrInt.setKeyable(True)
    myCustomNode.addAttribute(myCustomNode.aNumericAttrInt)

    # numeric float attr
    numericAttrFloat = OpenMaya.MFnNumericAttribute()
    myCustomNode.aNumericAttrFloat = numericAttrFloat.create("numericAttrFloat", "naf", OpenMaya.MFnNumericData.kFloat, kDefaultNumericAttrFloatValue)
    numericAttrFloat.setHidden(False)
    numericAttrFloat.setKeyable(True)
    myCustomNode.addAttribute(myCustomNode.aNumericAttrFloat)

    # string attr
    stringData = OpenMaya.MFnStringData().create(kDefaultStringAttrValue)
    stringAttr = OpenMaya.MFnTypedAttribute()
    myCustomNode.aStringAttr = stringAttr.create("stringAttr", "sa", OpenMaya.MFnData.kString, stringData)
    numericAttrFloat.setHidden(False)
    numericAttrFloat.setKeyable(True)
    myCustomNode.addAttribute(myCustomNode.aStringAttr)


def cmdSyntaxCreator():
    return OpenMaya.MSyntax()


# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    try:
        mplugin.registerNode(kNodeName, kNodeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kObjectSet)
    except:
        sys.stderr.write("Failed to register node: %s" % kNodeName)
        raise


# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterNode(kNodeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" % kNodeName)
        raise