#!/usr/bin/env python

###
# Copyright (c) 2002-2007 Systems in Motion
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

###
# This is an example from the Inventor Mentor,
# chapter 8, example 1.
#
# This example creates and displays a B-Spline curve.
# The curve is order 3 with 7 control points and a knot
# vector of length 10.  One of its knots has multiplicity
# 2 to illustrate a curve with a spike in it.
#

import sys

from pivy.coin import *
from pivy.sogui import *

floorData = """#Inventor V2.0 ascii
Separator {
   SpotLight {
      cutOffAngle 0.9
      dropOffRate 0.2 
      location 6 12 2 
      direction 0 -1 0
   }
   ShapeHints {
      faceType UNKNOWN_FACE_TYPE
   }
   Texture2Transform {
      #rotation 1.57
      scaleFactor 8 8
   }
   Texture2 {
      filename oak.rgb
   }
   NormalBinding {
        value  PER_PART
   }
   Material { diffuseColor 1 1 1 specularColor 1 1 1 shininess 0.4 }
   DEF FloorPanel Separator {
      DEF FloorStrip Separator {
         DEF FloorBoard Separator {
            Normal { vector 0 1 0 }
            TextureCoordinate2 {
               point [ 0 0, 0.5 0, 0.5 2, 0.5 4, 0.5 6,
                       0.5 8, 0 8, 0 6, 0 4, 0 2 ] }
            Coordinate3 {
               point [ 0 0 0, .5 0 0, .5 0 -2, .5 0 -4, .5 0 -6,
                       .5 0 -8, 0 0 -8, 0 0 -6, 0 0 -4, 0 0 -2, ]
            }
            FaceSet { numVertices 10 }
            BaseColor { rgb 0.3 0.1 0.0 }
            Translation { translation 0.125 0 -0.333 }
            Cylinder { parts TOP radius 0.04167 height 0.002 }
            Translation { translation 0.25 0 0 }
            Cylinder { parts TOP radius 0.04167 height 0.002 }
            Translation { translation 0 0 -7.333 }
            Cylinder { parts TOP radius 0.04167 height 0.002 }
            Translation { translation -0.25 0 0 }
            Cylinder { parts TOP radius 0.04167 height 0.002 }
         }
         Translation { translation 0 0 8.03 }
         USE FloorBoard
         Translation { translation 0 0 8.04 }
         USE FloorBoard
      }
      Translation { translation 0.53 0 -0.87 }
      USE FloorStrip
      Translation { translation 0.53 0 -2.3 }
      USE FloorStrip
      Translation { translation 0.53 0 1.3 }
      USE FloorStrip
      Translation { translation 0.53 0 1.1 }
      USE FloorStrip
      Translation { translation 0.53 0 -0.87 }
      USE FloorStrip
      Translation { translation 0.53 0 1.7 }
      USE FloorStrip
      Translation { translation 0.53 0 -0.5 }
      USE FloorStrip
   }
   Translation { translation 4.24 0 0 }
   USE FloorPanel
   Translation { translation 4.24 0 0 }
   USE FloorPanel
}"""

##############################################################
# CODE FOR The Inventor Mentor STARTS HERE

# The control points for this curve
pts = (
   ( 4.0, -6.0,  6.0),
   (-4.0,  1.0,  0.0),
   (-1.5,  5.0, -6.0),
   ( 0.0,  2.0, -2.0),
   ( 1.5,  5.0, -6.0),
   ( 4.0,  1.0,  0.0),
   (-4.0, -6.0,  6.0))

# The knot vector
knots = (1, 2, 3, 4, 5, 5, 6, 7, 8, 9)

# Create the nodes needed for the B-Spline curve.
def makeCurve():
    curveSep = SoSeparator()
    
    # Set the draw style of the curve.
    drawStyle = SoDrawStyle()
    drawStyle.lineWidth = 4
    curveSep.addChild(drawStyle)
    
    # Define the NURBS curve including the control points
    # and a complexity.
    complexity = SoComplexity()
    controlPts = SoCoordinate3()
    curve      = SoNurbsCurve()
    complexity.value = 0.8
    controlPts.point.setValues(0, 7, pts)
    curve.numControlPoints = 7
    curve.knotVector.setValues(0, 10, knots)
    curveSep.addChild(complexity)
    curveSep.addChild(controlPts)
    curveSep.addChild(curve)
    
    return curveSep

# CODE FOR The Inventor Mentor ENDS HERE
##############################################################

def main():   
    # Initialize Inventor and Qt
    appWindow = SoGui.init(sys.argv[0])
    if appWindow == None:
        sys.exit(1)
        
    root = SoSeparator()
    
    # Create the scene graph for the heart
    heart    = SoSeparator()
    curveSep = makeCurve()
    lmodel   = SoLightModel()
    clr      = SoBaseColor()
    
    lmodel.model = SoLightModel.BASE_COLOR
    clr.rgb = (1.0, 0.0, 0.1)
    heart.addChild(lmodel)
    heart.addChild(clr)
    heart.addChild(curveSep)
    root.addChild(heart)
    
    # Create the scene graph for the floor
    floor = SoSeparator()
    xlate = SoTranslation()
    rot   = SoRotation()
    scale = SoScale()
    input = SoInput()
    
    input.setBuffer(floorData)
    result = SoDB.readAll(input)
    xlate.translation = (-12.0, -5.0, -5.0)
    scale.scaleFactor = (2.0, 1.0, 2.0)
    rot.rotation.setValue(SbRotation(SbVec3f(0.0, 1.0, 0.0), M_PI/2.0))
    floor.addChild(rot)
    floor.addChild(xlate)
    floor.addChild(scale)
    floor.addChild(result)
    root.addChild(floor)
    
    # Create the scene graph for the heart's shadow
    shadow = SoSeparator()
    shmdl  = SoLightModel()
    shmtl  = SoMaterial()
    shclr  = SoBaseColor()
    shxl   = SoTranslation()
    shscl  = SoScale()
    
    shmdl.model = SoLightModel.BASE_COLOR
    shclr.rgb = (0.21, 0.15, 0.09)
    shmtl.transparency = 0.5
    shxl.translation = (0.0, -4.9, 0.0)
    shscl.scaleFactor = (1.0, 0.0, 1.0)
    shadow.addChild(shmtl)
    shadow.addChild(shmdl)
    shadow.addChild(shclr)
    shadow.addChild(shxl)
    shadow.addChild(shscl)
    shadow.addChild(curveSep)
    root.addChild(shadow)
    
    # Initialize an Examiner Viewer
    viewer = SoGuiExaminerViewer(appWindow)
    viewer.setSceneGraph(root)
    viewer.setTitle("B-Spline Curve")
    cam = viewer.getCamera()
    cam.position = (-6.0, 8.0, 20.0)
    cam.pointAt(SbVec3f(0.0, -2.0, -4.0))
    viewer.show()
    
    SoGui.show(appWindow)
    SoGui.mainLoop()

if __name__ == "__main__":
    main()
