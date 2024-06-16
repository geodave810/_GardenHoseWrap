# Garden Hose Wrap
# 6/15/2024 By: David Bunch
import adsk.core, adsk.fusion, adsk.cam, traceback
import math
# Global list to keep all event handlers in scope.
handlers = []

# Initialize app and ui variables.
app = adsk.core.Application.get()
design = app.activeProduct
rootComp = design.rootComponent
ui = app.userInterface
preferences = app.preferences
def CreateNewComponent():
    global subComp1
    allOccs = rootComp.occurrences
    transform = adsk.core.Matrix3D.create()
    occ1 = allOccs.addNewComponent(transform)
    subComp1 = occ1.component
    subComp1.name = Body_Name
def Draw_GardenHoseWrap(ID, pitch, Thk, rev, SplinePts):
    global sketch_Helix
    global sketch_Profile
    global R_Min1
    global Body_Name
    F_ID = float(ID)
    F_pitch = float(pitch)
    F_Thk = float(Thk)
    I_rev = int(rev)
    I_Pts = int(SplinePts)
    F_OD = F_ID + (2 * F_Thk)
    Rad = F_OD / 2.0
    Rad1 = Rad * .1
    R_Min = F_ID / 2.0
    R_Min1 = R_Min * .1
    Pit2 = F_pitch / 2 * .1
    Pit4 = F_pitch / 4 * .1
    Pit8 = F_pitch / 8 * .1
    Ht = F_pitch * I_rev
    Ht1 = Ht * .1
    F_Rnd = (F_Thk / 2.0) * .1
    Tstart = design.timeline.markerPosition
    Base_Ht_mm = (I_rev * F_pitch)
    S_Base_Ht = f"{Base_Ht_mm:.2f}"
# Add all the input parameters to component & body name to make it easier to determine what settings were used
    Body_Name = "GHW_" + ID + "mm_ID_" + pitch + "P_" + Thk + "mm_Thk_" + S_Base_Ht + "mm_Ht_" + rev + "_rev_" + SplinePts + "_Spts"
    CreateNewComponent()
    P1 = adsk.core.Point3D.create(R_Min1, Pit4, 0)
    P2 = adsk.core.Point3D.create(Rad1, Pit4, 0)
    P3 = adsk.core.Point3D.create(Rad1, -Pit4, 0)
    P4 = adsk.core.Point3D.create(R_Min1, -Pit4, 0)
# Create a new 3D sketch.
    sketches = subComp1.sketches
    xyPlane = subComp1.xYConstructionPlane
    sketch_Helix = sketches.add(xyPlane)
    sketch_Helix.name = "Sketch_Helix"
# Create sketch for the profile to sweep
    sketch_Profile = sketches.add(subComp1.xZConstructionPlane)
    sketch_Profile.name = "HoseWrap_Profile"
    sketchLines = sketch_Profile.sketchCurves.sketchLines
    points = [P1, P2, P3, P4, P1]              # Create a list of points for single thread profile
    draw_lines_between_points(sketch_Profile, points)
    largest_profile = sketch_Profile.profiles.item(0)
    DrawHelix(Rad, F_pitch, Ht, Ht1, I_Pts, 'P', 'R', largest_profile)
    if I_rev > 1:
        DrawPatternThreads(F_pitch, I_rev)
# Draw a circle.
    circles = sketch_Helix.sketchCurves.sketchCircles
    circle1 = circles.addByCenterRadius(adsk.core.Point3D.create(0, 0, 0), Rad1 + .1)
# Get the profile defined by the circle.
    profCir = sketch_Helix.profiles.item(0)
    Ht2 = adsk.core.ValueInput.createByReal(-Pit2)
    extrudes = subComp1.features.extrudeFeatures
    ext = extrudes.addSimple(profCir, Ht2, adsk.fusion.FeatureOperations.CutFeatureOperation)
# Create an extrude input.
    extrudes = subComp1.features.extrudeFeatures
    extInput = extrudes.createInput(profCir, adsk.fusion.FeatureOperations.CutFeatureOperation)
# Define the distance to extrude.
    distance = adsk.core.ValueInput.createByReal(Pit2)  # 10mm
    Base_Ht = Base_Ht_mm * .1
    #ui.messageBox(f'Base_Ht = {Base_Ht}\nIrev = {I_rev}\nF_pitch = {F_pitch}\F_pitch / 4 = {F_pitch / 4}')
# Set the starting offset.
    startOffset = adsk.core.ValueInput.createByReal(Base_Ht)
# Set the extrude input parameters.
    extInput.setDistanceExtent(False, distance)
    extInput.startExtent = adsk.fusion.FromEntityStartDefinition.create(xyPlane, startOffset)
# Create the extrusion.
    extrudes.add(extInput)
    timelineGroups = design.timeline.timelineGroups
    TLend = design.timeline.markerPosition - 1
    timelineGroup = timelineGroups.add(Tstart, TLend)
###################################################################################################
def DrawPatternThreads(PitHlx, rev):
    PitHlx2 = PitHlx * .1
    bsubComp1_bodies = subComp1.bRepBodies              # Collect the bodies used in our component
    numBodies = bsubComp1_bodies.count                  # Get a count of the bodies used
    targetBody = bsubComp1_bodies.item(numBodies-1)     # This should be the Nut just drawnf
# Create input entities for rectangular pattern
    inputEntites = adsk.core.ObjectCollection.create()
    inputEntites.add(targetBody)
    path = subComp1.features.createPath(Vert_Line)
    General_Precision = preferences.unitAndValuePreferences.generalPrecision        # Get current precision
    preferences.unitAndValuePreferences.generalPrecision = 9                    # Set to maximum of 9 before running the pathPatterns code
    patternQuantity = adsk.core.ValueInput.createByReal(rev)
    patternDistance = adsk.core.ValueInput.createByReal(PitHlx2)
    pathPatterns = subComp1.features.pathPatternFeatures
    pathPatternInput = pathPatterns.createInput(inputEntites, path, patternQuantity, patternDistance, adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
# Create the path pattern
    pathFeature = pathPatterns.add(pathPatternInput)
    preferences.unitAndValuePreferences.generalPrecision = General_Precision        # Set precision back to what user had
    panel_comb_fea = subComp1.features.combineFeatures
    tool_bodies_oc = adsk.core.ObjectCollection.createWithArray(
        [subComp1.bRepBodies[i] for i in range(1, subComp1.bRepBodies.count)]
    )
    comb_input: adsk.fusion.CombineFeatureInput = panel_comb_fea.createInput(
        subComp1.bRepBodies[0],
        tool_bodies_oc
    )
    comb_input.isKeepToolBodies = False
    comb_input.operation = adsk.fusion.FeatureOperations.JoinFeatureOperation
    panel_comb_fea.add(comb_input)
##########################################################################
def draw_lines_between_points(sketch, points):
    for i in range(len(points)-1):
        sketch.sketchCurves.sketchLines.addByTwoPoints(points[i], points[i+1])
###################################################################
def DrawHelix(Rad, Pitch, Ht, Ht1, sPts, G_Rail, RL_thread, prof):
    global sketchSplines
    global Vert_Line
    P10 = adsk.core.Point3D.create(0,0,Ht1)
    rev = int(Ht / Pitch) + 1               # Number of revolutions, add one to it so we don't do a partial revolution
    Pitch2 = Pitch * 0.1
    Pitch1 = round(Pitch2, 6)
# Create an object collection for the points.
    sketchSplines = sketch_Helix.sketchCurves.sketchFittedSplines
    sketchCenter = sketch_Helix.sketchCurves.sketchLines    # used for Centerline Guide Rail, does not work as well as Helix
    P0 = adsk.core.Point3D.create(0,0,0)
    Vert_Line = sketchCenter.addByTwoPoints(P0,P10)         # Draw Center Vertical for Guide Rail with Sweeep
    Z0 = 0.0
    Draw_1_Helix(rev, Rad, Pitch1, sPts, Z0, G_Rail, prof, RL_thread)    # Now draw the Helix
##########################################################################
def Draw_1_Helix(rev, Rad, Pitch1, sPts, Z0, G_Rail, prof, RL_thread):
    global body1
    global Rad1
    global sweeper
    Rad1 = Rad * .1
    ang1 = 360.0 / sPts                             # Increment angle in degrees between horizontal spline points
    ang_R = ang1 * math.pi / 180                    # Increment angle in radians between horizontal spline points
    Z_inc = Pitch1 / sPts                           # Z increment amount between spline points
    sPts_Total = sPts                               # Number of spline points for 1 revolution of Helix
    Icount = 0                                      # Initalize Loop counter
    ang = 0                                         # Set beginning angle of Helix spline poing
    points = adsk.core.ObjectCollection.create()    # Create the points collection for the inner Helix Path
    points1 = adsk.core.ObjectCollection.create()   # Create the points collection for the outer Helix Guide Rail
    while (Icount <= sPts_Total):
        x = R_Min1 * math.cos(ang)                  # Helix x, y points along inside Radius minus .1mm to connect multiple threads
        y = R_Min1 * math.sin(ang)
        z = Z0
        Z0 = Z0 + Z_inc                             # Increment the Z to get to next spline Z coordinate
        x1 = Rad1 * math.cos(ang)                   # Helix x, y points along outside radius of thread
        y1 = Rad1 * math.sin(ang)
        points1.add(adsk.core.Point3D.create(x1, y1, z))     # Need 2nd spline for guide rail
        points.add(adsk.core.Point3D.create(x, y, z))
        ang = ang + ang_R                           # Increment angle for next coordiante in loop
        Icount = Icount + 1                         # increment loop counter
    spline = sketchSplines.add(points)              # Create the inner spline helix from points
    spline1 = sketchSplines.add(points1)        # Create the outer spline helix from points
    guide = subComp1.features.createPath(spline1)        
##################################################
    path = subComp1.features.createPath(spline)
# Create a sweep input
    sweeps = subComp1.features.sweepFeatures
    sweepInput = sweeps.createInput(prof, path, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    sweepInput.guideRail = guide            # Default guide rail is the outer Helix
    sweepInput.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileScaleOption
# Create the sweep.
    sweeper = sweeps.add(sweepInput)              # This seems to be the slowest part of the code
    body1 = sweeper.bodies.item(0)
    body1.name = Body_Name                        # rename body to most of input parameters from main routine
##########################################################################
# Event handler for the input changed event.
class CommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            command = args.command
            inputs = command.commandInputs
            inputs.addTextBoxCommandInput('ID', 'Inside Diameter (mm): ', '24', 1, False)
            inputs.addTextBoxCommandInput('pitch', 'Pitch (mm): ', '48', 1, False)
            inputs.addTextBoxCommandInput('Thk', 'Thickness of Wrap (mm): ', '1.7', 1, False)
            inputs.addTextBoxCommandInput('rev', 'How Many Revolutions: ', '4', 1, False)
            inputs.addTextBoxCommandInput('SplinePts', 'Number of Spline Points: ', '18', 1, False)
# Connect to the execute event.
            onExecute = CommandExecuteHandler()
            command.execute.add(onExecute)
            handlers.append(onExecute)

# Connect to the destroy event.
            onDestroy = CommandDestroyHandler()
            command.destroy.add(onDestroy)
            handlers.append(onDestroy)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Event handler for the execute event.
class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            command = args.command
            inputs = command.commandInputs

            # Get the values from the text boxes.
            IDInput = inputs.itemById('ID')
            pitchInput = inputs.itemById('pitch')
            ThkInput = inputs.itemById('Thk')
            revInput = inputs.itemById('rev')
            SplinePtsInput = inputs.itemById('SplinePts')

            ID = IDInput.text
            pitch = pitchInput.text
            Thk = ThkInput.text
            rev = revInput.text
            SplinePts = SplinePtsInput.text
            Draw_GardenHoseWrap(ID, pitch, Thk, rev, SplinePts)
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Event handler for the destroy event.
class CommandDestroyHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            adsk.terminate()
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Entry point for the script.
def run(context):
    try:
# Check if the command definition already exists and delete it if it does.
        cmdDef = ui.commandDefinitions.itemById('inputDialogCmd')
        if cmdDef:
            cmdDef.deleteMe()
# Create a new command.
        cmdDef = ui.commandDefinitions.addButtonDefinition('inputDialogCmd', 'Input Dialog', 'Enter Values')
# Connect to the command created event.
        onCommandCreated = CommandCreatedEventHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)
# Execute the command.
        cmdDef.execute()
# Keep the script running.
        adsk.autoTerminate(False)
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
# Entry point for the script.
def stop(context):
    try:
        #ui.messageBox('Script stopped.')
        adsk.terminate()
    except Exception as e:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))