// Garden Hose Wrap
// 6/14/2024 By: David Bunch
// Garden Hose Wrap for kinks in the hose
//
// v1.0.0
// Change rev variable to adjust height of wrap
// With a Pitch of 48 these different rev's will give the corresponding heights
// The displayed Base_Ht is the final height of the Garden Hose Wrap
//10 = 468mm Height
// 9 = 420mm Height
// 8 = 372mm Height
// 7 = 324mm Height
// 6 = 276mm Height
// 5 = 228mm Height
// 4 = 180mm Height
// 3 = 132mm Height
// 2 = 84mm Height
// 1 = 36mm Height
Wid = .1;                       // Extrusion width of Rectangle profile (You want a small number here)
Thk = 1.7;                      // Thickness of Wrap
Thk2 = Thk / 2;
Res_Inc = 1;                    // Approximate length of each chord on Helix
ID = 24;                        // Defines Inside Diameter of Garden Hose Wrap
OD = ID + (2 * Thk);            // Calculate Outside Diameter of Garden Hose Wrap
Rad_OD = OD / 2;
Rad_ID = ID / 2;
Rnd_Y = Rad_ID + Thk2;          // Offset Radial Distance For Rounding the Ends
Pitch = 48.0;                   // Height of one revolution of the spiral, 48 works well for me, but you can change it
Pit2 = Pitch / 2;
Pit4 = Pitch / 4;               // Used for Rectangle Profile Height
rev = 4;                        // # of Rotations of Spiral (4 or 5 is maximum I have tried printing vertical)
                                // Always make rev an INTEGER, I did not do the math for fractional Revoutions
Base_Ht = rev * Pitch - Pit4;   // Total Height of Garden Hose Wrap
Cut_Ht = Base_Ht - Pit4;
OD_Res = (round(((OD * 3.14) / Res_Inc) / 2) * 4);    // Using the 4 gives me a vertex on each quadrant of circle
ang_inc = 360.0 / OD_Res;
Z_inc = Pitch / OD_Res;
Count = OD_Res * rev;
Rnd_ID = Thk;
Rnd_Ang = atan(Thk2 / Rnd_Y);
Rnd_ID_Res = (round(((Rnd_ID * 3.14) / .5) / 2) * 4);
echo("OD = ", OD);
echo("Base_Ht = ", Base_Ht);
echo("Base_Ht-Pit4 = ",Base_Ht - Pit4);
echo("Rad_OD = ", Rad_OD);
echo("Rad_ID = ", Rad_ID);
echo("Pit4 = ", Pit4);
echo("Thk2 = ", Thk2);
echo("Rnd_Y = ",Rnd_Y);
echo("Rnd_Ang = ",Rnd_Ang);
echo("Cut_Ht = ", Cut_Ht);
echo("OD_Res = ", OD_Res);
echo("Rnd_ID_Res = ", Rnd_ID_Res);
echo("ang_inc = ", ang_inc);
echo("Count = ", Count);
echo("ang_inc = ", ang_inc);
module RectCut()
{
    rotate([-90, 0, 0])
    translate([0, 0, -Wid / 2])
    linear_extrude(height = Wid, center = false, convexity = 10)polygon(points = 
    [[Rad_ID, -Pit4], [Rad_OD, -Pit4], [Rad_OD, Pit4], [Rad_ID, Pit4]]);
}
module DrawSpiral()
{
    for (i = [1 : Count])
    {
        hull()
        {
            rotate([0, 0, ang_inc * (i - 1)])
            translate([0, 0, Z_inc * (i - 1)])
            RectCut();
            rotate([0, 0, ang_inc * i])
            translate([0, 0, Z_inc * i])
            RectCut();
        }
    }
}
module RndEdge()
{
    difference()
    {
        cylinder(d = Thk * 2, h = Pit2, $fn = Rnd_ID_Res);
        translate([0, 0, -1])
        cylinder(d = Thk, h = Pit2 + 2, $fn = Rnd_ID_Res);
        translate([-Pit4 / 2, 0,  -1])
        cube([Pit4, Pit4, Pit2 + 2]);
    }
}
module DrawFinal()
{
    difference()
    {
        DrawSpiral();
        translate([0, 0, -Pit2])
        cylinder(d = OD * 2, h = Pit2, $fn = 16);       // Cut Below Bottom
        translate([0,0,Base_Ht])
        cylinder(d = OD*2, h = Pit2 + 1, $fn = 16);     // Cut Above Height
        translate([0, -OD, Cut_Ht - 1])
        cube([OD, OD + 1, Pit2 + 1]);                   // Trim the Top where we Round it
        rotate([0, 0, Rnd_Ang])
        translate([Rnd_Y, 0, -1])
        RndEdge();
        rotate([0, 0, -Rnd_Ang])
        translate([0, -Rnd_Y, Cut_Ht - 6])
        rotate([0, 0, 90])
        RndEdge();
    }
}
DrawFinal();
