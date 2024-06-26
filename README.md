# _GardenHoseWrap
Garden Hose Wrap for kinks in the hose

There is fusion 360 python script source code and an OpenSCAD source code that allow you to adjust the Inside Diameter, Pitch, Thickness of Wrap, Number of Revolutions and number of Spline Points
In Fusion 360, you change the values in a dialog box.  The 1st 3 variables should be entered in mm.<br>
![GardenHoseWrap_Dialog_v1_1_0](https://github.com/geodave810/_GardenHoseWrap/assets/13069472/b3f0bfa8-61e4-42eb-9320-ffcd6789da0c)

To use the fusion 360 python script copy the folder _GardenHoseWrap to this location.<br> C:\Users\<Username>\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\
![_GardenHoseWrapLocation](https://github.com/geodave810/_GardenHoseWrap/assets/13069472/b2a26397-f317-4725-b6b0-a795efd071a3)

The OpenSCAD source code, you change the variables in the source code, then render it followed by exporting the STL file for slicing

I have had the best luck with printing these with 3 layers of raft in the same orientation as they are created.  I use PLA+ filament so it is flexible enough to wrap around the garden hose.
![IMG_20240613_800x600](https://github.com/geodave810/_GardenHoseWrap/assets/13069472/930c528c-7c2a-4ba0-ad96-f7a31bcc8fc4)
![IMG_4935_800x600](https://github.com/geodave810/_GardenHoseWrap/assets/13069472/2c6bbfda-9b76-4fba-b471-acab1c621b94)

The fusion 360 python source draws an approximate helix with a fitted spline between points for the path of the wrap.  You can adjust the number of spline points, but 36 should be sufficient.  The OpenSCAD source has a different approach since it can't be done the same as Fusion.  It takes a rectangle profile and extrudes it a small amount and uses the hull() command to mesh it with another extruded profile a small angle along a helix path. It does that for the full length of the helix path.
If you find this program useful to you, consider making a donation from the link on the right or purchasing one of my audio recordings of Mountain streams from Amazon in the 2nd link on the right.

Shield: [![CC BY-NC 4.0][cc-by-nc-shield]][cc-by-nc]

This work is licensed under a
[Creative Commons Attribution-NonCommercial 4.0 International License][cc-by-nc].

[![CC BY-NC 4.0][cc-by-nc-image]][cc-by-nc]

[cc-by-nc]: https://creativecommons.org/licenses/by-nc/4.0/
[cc-by-nc-image]: https://licensebuttons.net/l/by-nc/4.0/88x31.png
[cc-by-nc-shield]: https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg
