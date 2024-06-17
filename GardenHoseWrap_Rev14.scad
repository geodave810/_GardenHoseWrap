// Garden Hose Wrap
// 6/14/2024 By: David Bunch
// Garden Hose Wrap for kinks in the hose
//
// Update 6/17/2024 v1.1.0
//                  Optional rounding of spiral edges added
//                  Optional Gap size added, use positive numbers for gap width or -1 for full gap or -2 for half gap
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
ID = 24;                            // Defines Inside Diameter of Garden Hose Wrap
Thk = 1.7;                          // Thickness of Wrap
Pitch = 48.0;                       // Height of one revolution of the spiral, 48 works well for me, but you can change it
rev = 4;                            // # of Rotations of Spiral (4 or 5 is maximum I have tried printing vertical)
                                    // Always make rev an INTEGER, I did not do the math for fractional Revoutions

Gap_Type = -1;                      // -1 = Full Gap, -2 = Half Gap or any other positive number is the actual gap
Rnd_YesNo = 1;                      // 0 = No, 1 = Yes for rounding square corners
// *******  Only change the variables above
Pit2 = Pitch / 2;
Pit4 = Pitch / 4;                   // Used for Rectangle Profile Height
R0 = Pit4;
Thk2 = Thk / 2;
Res_Inc = 1;                        // Approximate length of each chord on Helix
Wid = .1;                           // Extrusion width of Rectangle profile (You want a small number here)
OD = ID + (2 * Thk);                // Calculate Outside Diameter of Garden Hose Wrap
Rad_OD = OD / 2;
Rad_ID = ID / 2;
Rnd_Y = Rad_ID + Thk2;              // Offset Radial Distance For Rounding the Ends
Base_Ht = rev * Pitch - Pit4;       // Total Height of Garden Hose Wrap
Cut_Ht = Base_Ht - Pit4;
OD_Res = (round(((OD * 3.14) / Res_Inc) / 2) * 4);    // Using the 4 gives me a vertex on each quadrant of circle
ang_inc = 360.0 / OD_Res;
Z_inc = Pitch / OD_Res;
OD_Res14 = OD_Res / 4;              // 1/4 revolution
Count = OD_Res * rev - OD_Res14;    // Stop 1/4 revolution from the end
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
module RectCut(R_Ht)
{
    R_Ht_Rnd = R_Ht - Thk2;
    if (Rnd_YesNo == 0)
    {
        rotate([-90, 0, 0])
        translate([0, 0, -Wid / 2])
        linear_extrude(height = Wid, center = false, convexity = 10)polygon(points = 
        [[Rad_ID, -R_Ht], [Rad_OD, -R_Ht], [Rad_OD, R_Ht], [Rad_ID, R_Ht]]);
    } else
    {
        rotate([-90,0,0])
        hull()
        {
            translate([Rad_ID + Thk2, -R_Ht_Rnd,0])
            cylinder(d = Thk,h = Wid, $fn=Rnd_ID_Res);
            translate([Rad_ID + Thk2, R_Ht_Rnd,0])
            cylinder(d = Thk,h = Wid, $fn=Rnd_ID_Res);
        }
    }
}
module DrawSpiral(R_Ht)
{
    for (i = [1 : Count])
    {
        hull()
        {
            rotate([0, 0, ang_inc * (i - 1)])
            translate([0, 0, Z_inc * (i - 1)])
            RectCut(R_Ht);
            rotate([0, 0, ang_inc * i])
            translate([0, 0, Z_inc * i])
            RectCut(R_Ht);
        }
    }
}
module RndEdge(Pit20)
{
    difference()
    {
        cylinder(d = Thk * 2, h = Pit20, $fn = Rnd_ID_Res);
        translate([0, 0, -1])
        cylinder(d = Thk, h = Pit20 + 2, $fn = Rnd_ID_Res);
        translate([-Pit4 / 2, 0,  -1])
        cube([Pit4, Pit4, Pit20 + 2]);
    }
}
module DrawFinal(R_Ht = Pit4)
{
    Top_Ht = (rev - .25) * Pitch - (R_Ht) - .1;
    difference()
    {
        DrawSpiral(R_Ht);
        translate([0, 0, -Pit2])
        cylinder(d = OD * 2, h = Pit2, $fn = 16);       // Cut Below Bottom
        translate([0,0,Base_Ht])
        cylinder(d = OD*2, h = Pit2 + 1, $fn = 16);     // Cut Above Height
        rotate([0, 0, Rnd_Ang])
        translate([Rnd_Y, 0, -1])
        RndEdge(Pit2);
        rotate([0, 0, -Rnd_Ang])
        translate([0,-Rnd_Y, Top_Ht])
        rotate([0, 0, 90])
        RndEdge(R_Ht*2+1);
    }
}
if (Gap_Type == -2)
{
    R0 = Pitch / 2.666666667;
    DrawFinal(R0);
}
else if (Gap_Type == -1)
{
    DrawFinal(R0);
}
else
{
    R0 = (Pitch / 2) - (Gap_Type / 2);
    DrawFinal(R0);
}