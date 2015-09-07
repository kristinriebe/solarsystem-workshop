#Creating planets of the solar system with Blender

<img width="100%" src="http://kristinriebe.github.io/solarsystem-workshop/images/planets-long.png"/>

These instructions will guide you through creating planets of the solar system in 3D using Blender and its Python API. At the end, you will have written a Python script which creates your planets, their orbits and even animates their rotation from scratch in one go. If you get stuck at some point, you can contact me at 
kristin.riebe@mk-star.de.

Have fun!


##Materials
Following files are provided/needed:

* [planets-template.blend](https://github.com/kristinriebe/solarsystem-workshop/blob/master/planets-template.blend): 
    a blender file with basic setup
* [create_planet.py](https://github.com/kristinriebe/solarsystem-workshop/blob/master/create_planet.py): 
    a simple script for creating one planet
* [planets.csv](https://github.com/kristinriebe/solarsystem-workshop/blob/master/planets.csv): 
    file with most basic parameters for each planet of the solar system and the sun
* [textures](http://kristinriebe.github.io/solarsystem-workshop/textures.zip): 
    directory with texture maps of the planets, 17 MB
* [rings.py](https://github.com/kristinriebe/solarsystem-workshop/blob/master/rings.py): 
    contains two functions for adding rings around Saturn and Uranus
* (Extra:) [animate_camera.py](https://github.com/kristinriebe/blendertools/blob/master/animate_camera.py):
    a script that sets the camera moving along a path looking at a certain object

Other things you need:

* Blender (download from [blender.org](http://www.blender.org)). These instructions were only tested with version 2.75. I expect them to work with versions from ~ 2.6 on. Install it such that you can start Blender directly from the command line.
* Web browser with internet connection, for checking the online documentation or Blender StackExchange occasionally for help

It helps, if you are already a bit familiar with Blender's graphical user interface. Look at e.g. the [Blender manual](http://www.blender.org/manual/) or follow these short [Blender basics videos](https://cgcookie.com/course/blender-basics/). 

Ready? Let's get started!

##Basic instructions 
* Open `planets-template.blend` with Blender from the command line:

    `blender planets-template.blend`

    Go to `File`->`Save As` to save it under a custom name, e.g. 
    just `planets.blend`.

* Your 3D scene is shown in the *3D view* area, that's the big central area.
  The template already contains a camera, a bright point lamp in the center to illuminate the planets you are going to create and a dark blue world background with a bit environment light switched on so that shadows are not too dark. You don't see its effects now, only later, when rendering your scene (`F12`).

* The window layout is already changed to `Scripting` for you (in the top
    menu bar, next to `File`, `Render`, `Window` and `Help`). 
    Go to the *Text Editor* area, (left main area) and load a script by selecting `Text`->`Open Text Block` and choosing `create_planet.py`.

* Select `Text`->`Run Script` to execute the script. A blue sphere called 
    `Planet-Earth` should appear in your *3D view*.

If this works, then you can go ahead, expand the script and experiment with the following tasks. If it didn't work, check the output in the console from which you started Blender for error messages. 


##Experimenting
* Look in the Python script in your *Text area* for the `add_sphere`-function.
    Improve it such that the `size` (radius) of the sphere is provided as an 
    additional parameter. This should be used in Blender's 
    `primitive_uv_sphere_add` function to create the sphere.

* Provide e.g. `size=2` in the `main`-function when creating the sphere and 
    rerun your script. Check if the size has changed correctly. Note that the 
    script contains a `delete_objects`-function that removes all objects with 
    names matching `Planet*` from the scene. This is useful to cleanup before 
    recreating your planet.

* Adjust the material settings in the `add_material` function to create a planet with a different base color (e.g. red for `diffuse_color`) and no specular. Colors are given as RGB-triplets in Blender, so red would be 
`[1,0,0]`.


##More planets
So far, all these things can be done much faster via the interface. But such a script becomes very useful when creating more than one planet at once. Let's do this! 

* Write a read-routine to read planet and sun parameters from the provided 
  csv-file. Blender comes with bundled Python that also includes the csv-module for reading comma-separated value files, which makes this task very easy, e.g like this:  

    ```python
    with open(myfilename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        lines = [r for r in reader 
                    if not r[reader.fieldnames[0]].startswith("#")]
    ```
    Be careful to provide the correct (full) path to your csv-file.
    Alternatively you can also create a dictionary or array with parameters for different planets directly in your script. The parameters we use here are:  

    - `name` of the planet (or sun) 
    - `radius` of the planet (at equator), in km  
    - `art_distance` - artificial distance for good visual impression, 
                       in Blender units  
    - `distance` of the planet from the sun (semi-major axis)  
    - `flattening` of the planet  
    - `tilt` of the planet's axis  
    - `rotperiod` - time for rotation of the planet around its axis in 
                    days  
    - `eccentricity` of the planet's orbit  
    - `orbitperiod` - time for rotation of the planet on its orbit 
                          around the sun  
    - `texture` image for the planet  
    - `color` RGB triplet for the planet  

* In your `main`-function, write a loop to create more than one planet at 
  once, with different names and sizes. Use the column `art_distance` from the 
  provided csv-file to set the planets apart, e.g. along the +`x`-axis, 
  using `location` when adding the sphere.

* Take care to **scale down the radii** of the planets and the Sun to something between 0 and 10 Blender units, otherwise they may be too big to be visible in your Blender scene. (A basic size scale factor of 1/100,000 is a good value. For better visual impressions, increase the size of rocklike planets (Mercury, Venus, Earth, Mars) by a factor of 6, gas planets by a factor of 2.)

##Sun material adjustments
The Sun is special, since it is a self-glowing star. Thus its material needs to be adjusted. 
In general, you can always discover the available attributes for objects and materials via the *Python Console*: 

* First get the Sun-object: `obj = bpy.data.objects['Planet-Sun']`.  
* Type `obj.` and press `Ctrl`+`Space` in the console to get autocomplete suggestions.
* You can select the (first) material of your object using:   
  `mat = obj.material_slots[0].material`.
* Type `mat.` and press `Ctrl`+`Space` in the console to explore the available attributes. You can also set them here and see their effects immediately.
* In your script, include:  

    ```python
    # suppress any shadows and don't receive any
    mat.use_shadeless = True
    mat.use_shadows = False
    
    # allow light of point source to transmit through the sun's surface
    mat.use_cast_shadows = False
    mat.use_cast_buffer_shadows = False
    ```
* These settings could also be adjusted in the GUI, in the *Properties* area, *Material* tab, in sections `Shading` and `Shadow`. They ensure that the Sun does not receive any shadows and does not cast any.


##Colors and texture
* It's boring if all the planets have got the same color, so use a different color triplet for each planet. You can use the values from the file (parse them and convert them to a list of three values) or choose your own. Pass the color-triplet on to the `add_material` function, use it for `diffuse_color` in the script and rerun the script. Check, if every planet got its own color now.

* Adjust the position of your camera, so you get a good view on all your planets. (Check by going into *Camera View*: *View*, *Camera* or `Numpad 0`.)
  Render your scene with *Render* (top menu), *Render Image* or hit `F12`.

* Let's make the planets even prettier by adding an image texture map to each 
  of them. Most planet textures are freely available from NASA. Download your own texture maps or use those from the *textures*-directory. Adjust the name of the texture image for each planet in your csv-file/dictionary.

* Enable the `add_texture` function in the script's `main`-function. Make sure
  to provide the correct path to your images; otherwise your script will fail. 
  This function will load the image to a texture and map it using spherical coordinates.

* Rerun your script. The texture will only be visible when rendered, so render your scene again (`F12`). 


##Flattening
* Actually, planets are rarely exact spheres, but mostly a bit flattened in z-direction. This is described by the flattening parameter, given e.g. at Wikipedia for each planet. `0` flattening is a perfect sphere. Adjust each planet-sphere's `z`-scale by the factor `1-flattening` in your script.


##Axial tilt
* Improve your script even further by adding a tilt to the planet's axis. The axial tilt is defined as deviation from the axis perpendicular to the planet's orbit, with Earth's north pole pointing upwards.
  The true direction to which the planet's north pole points is usually given in Earth's coordinate system. For simplicity, the provided csv-file already gives the correct precalculated rotation angles around x, y and z-axes for each planet in the global coordinate system. Thus you only need to set:

    `rotation_euler.x = tilt_x/180. * pi`

  etc. The angles in the file are given in degrees, thus they must be converted to radians first using angle[rad] = angle[degree] / 180 * pi.
* If you do not want to set pi manually, import the `math` module to use `math.pi` instead.

##Extra: Add rings
* Saturn is popular for its prominent ring system. Such rings are a bit tricky to set up, so there are functions prepared that take care of this for you, stored in `rings.py`. This uses more advances techniques which we won't discuss here. In principle, for Saturn we add a disk with a hole and put a ring texture on top of it; for Uranus we create one circle with a thin thickness. 

* Copy the functions over or load them as a module by adding following lines at the beginning of your script:  

    ```python
    blend_dir = os.path.dirname(bpy.data.filepath)
    if blend_dir not in sys.path:
        sys.path.append(blend_dir)
    import rings
    import imp
    imp.reload(rings)
    ```
  The reload-line ensures that the rings-module is reloaded every time you run the script. This is important if you want to make custom changes there.

* Add calls for the functions `add_saturn_rings` and `add_uranus_rings` to your `main` function. Neptune and Jupiter also have rings, but they are very thin and we'll skip them here.


##Simple orbit paths
* Add a circle as orbit path for each planet (not for the Sun!), using `art_distance` for radius. This can be done via Blender's interface, `Add`, `Curve`, `Circle`. 

* Check in the log-output (*Info* window at the top) which function was used. Write your own `add_orbit`-function for your script to add an orbit circle for each planet. Do not make an orbit path for the Sun.

* Name the orbit paths e.g. 'Planet-Earth-Orbit' etc. If you use the same 'Planet-' prefix as for the planet spheres, they will also be automatically deleted every time you run the script again.

* Adjust the circles' resolution to increase the number of points for the curve and thus its smoothness (e.g. 60). You can find this setting in the *Properties* area at the right side, in the *Data* tab (small line symbol). Add this to your `add_orbit` function as well.

* The circles cannot be seen in a rendered image, unless you give them some thickness. Thus increase the circles' thickness by setting the bevel depth to 0.006 or higher. In the interface, these setting are adjusted in the *Properties* area, at the tab for *Data* (bend curve symbol). Here you can look for the correct Blender attributes for your circle object and experiment which settings look good for you. Add them to your script as well.

* You may want to add a material to your orbits and adjust its shadow and shading options, so that orbits do not cast or receive any shadows. This is achieved with exactly the same settings as for the Sun material which was explained above.

* In fact, the planets move on ellipses, with the Sun at one of the focal points. We'll ignore this in this workshop and stick to the simplified circles.


##Extra: Orbit eccentricity
* Take the orbit eccentricity into account:
shift the orbit path, so the sun lies at one of the focal points of the ellipse. I.e.: shift it in x-direction by `a*ecc` (semi-major axis times eccentricity).
Scale the x-direction by a/distance, the y-direction by b/distance. b is the semi-minor axis, `b = a*sqrt(1-ecc**2)`.
(Don't forget `import math` for sqrt!)

* The orbit orientation is not yet correct - in truth, the orbits axes are not aligned! But taking the true orientation and also the inclination angle against e.g. Earth's orbit plane into account is beyond the scope of this workshop.


##Camera Animation (may be skipped here)
* Let's get the camera moving and add a camera path. Follow the next steps first via Blender's graphical interface, then check the log-output and the mouse-over tips for the functions and attributes to script this part as well. 
  - Add a circle via `Add`, `Curve`, `Circle`. Rename it to something like *CameraPath*. Set its location to (0,0,0) (`Alt`+`G`). Scale it such that there is still some distance between the circle and the sun (view it from top view to check this, `Numpad 7`; scale factor ~ 3.3 if using the scales from above).
  - Switch to `Edit Mode` (`Tab` key), drag the right-most point of the circle beyond the last planet. Switch back to `Object Mode` (`Tab` key).
  - Select your camera. In the *Properties* area, switch to the *Constraints* tab (chain-symbol). Click on `Add Object Constraint` and select `Follow Path` at the right side in the menu.
  - Choose your camera path as `target` for the Follow Path constraint and click `Animate Path`. 

* Split the *Python console* window horizontally and switch the new frame to *Timeline*. Click and drag the green line to move forward/backward in time. Can you see the camera moving?

* We are not yet done, the camera still looks away from the planets. We need to constrain its look-direction as well by adding an empty object to look at and another constraint: 
  - Add an empty using `Add`, `Empty`, `Cube`. This adds a cube-object that will not be rendered. Place it e.g. directly at Jupiter.
  - Add another constraint to your camera, choose `Track To`. This must be added below the Follow Path constraint. Select the just created empty object as `target`.

* When you move the time slider, you should now see the camera always looking to your empty object. 

* Do the same steps via scripting (also see `animate_camera.py`), in order to be able to reproduce them, when needed.

* The camera moves quite fast, you can slow it down by adjusting the animation manually:
  - Select the camera path, in *Properties* area switch to the *Curve data* tab and look for the `Evaluation time`. It is marked in green, because it is animated. Right click with the mouse and select `Clear keyframes`. 
  - In the timeline, choose frame 1. Set the curve's evaluation time to 0 and hit the `I` key while hovering over the evaluation time field. This sets a new animation keyframe (yellow). 
  - Now set the ti
  - me to e.g. 500 frames, set the evaluation time of the curve to 100 and again hit `I`. This sets the second (final) keyframe. Your camera will now move along the whole path within 500 frames.

* Further details of animations can be adjusted in the *Graph Editor*, we'll look into this in the next sections.


##Orbit animation
We will now let the planets move along their orbit paths.

* First do it for one planet and its path in the interface, then code the steps by checking which functions were used in the log/hover info. 

* Reset the position of the planet to (0,0,0).

* Select the planet's orbit. In the *Properties* area, switch to the *Constraints* tab. Click `Add Object Constraint` and select `Follow Path`.

* As `target`, choose the planet's orbit path. This will constrain the movement of the planet to its path! It is important that the path's rotation angles are set to 0 here, otherwise the planet will "inherit" the rotation and appear upside down or otherwise rotated.

* Split the *Python Console* window horizontally (drag the triangle) and switch the new window to *Timeline* (if you haven't done so yet). Here you can set start and end frame of your animation and set the current frame. 

* In order to get the planet moving, we need to set animation keyframes on the *Evaluation time* of the path:
  - Select the orbit path. In *Properties* area switch to *Curve data* tab and look for the `Evaluation time`. If the field is green, then right click with the mouse and select `Clear keyframes` first to reset everything. 
  - In the timeline, choose frame 1. Set the curve's evaluation time to 0 and hit the `I` key while hovering over the evaluation time field. This sets a new animation keyframe (yellow). 
  - Now set the time in your timeline to some duration, e.g. 365 frames. 
  - Set the evaluation time of the curve to 100 and again hit the `I` key. This sets the second (final) keyframe. 
  - Click and drag the green line to move forward/backward in time between these two keyframes. Can you see the planets moving on their orbits now?

* Switch the *Python Console* window to *Graph Editor* to fine tune your animation curve. When you have the orbit path selected, you should see a curve that represents the interpolation of the evaluation time between your two set keyframes. You can use the mouse wheel to zoom in and out and `Shift`+ middle mouse button (`MMB`) to pan the area.

* Adjust the interpolation type of the curve in the right toolbar within the *Graph Editor* (enable with `T` key, if you cannot see it). At *Active keyframe*, choose `Interpolation`: `Linear` instead of the default Bezier curve. 

* Planets also do not rotate only once, but repeatedly. To achieve this, we could repeat setting keyframes at multiples of the orbitperiod and evalution time, but we can simplify it by using a graph modifier. At *Modifiers* in the toolbar select `Cycles` and select `Repeat with Offset` for *Before* and *After*. 

* That's (nearly) it! Your planet should move now continuously around the Sun on its orbit.

* There is still something not quite right: the planets of our solar system rotate counter-clockwise when seen from the northern side of the ecliptic, i.e. when seen from +z downwards in our Blender setup. But your planet currently moves in clock-wise direction! That's because your orbit circle has clock-wise direction. The easiest way to switch the orbit direction is to rotate it via the `y`-axis by `180` degrees. Add another rotation via its `z`-axis by `90` degrees to put the first point of the orbit along the +x-axis. Now `Apply` the orbit rotation: `Object`, `Apply`, `Rotation`. This applies the rotation to the points of the curve, they are all shifted now, and resets the rotation angles to 0. As mentioned already above, this is important for maintaining the correct planet orientation, otherwise the planet would inherit its orbits orientations.

* Include all these steps in your script for each planet. Set the keyframes according to the actual orbit rotation period given in the planets-file (`orbitperiod`). This value is given in days; use a timefactor to make your planets move slower or faster than 1 frame for 1 day.  
*Hint:* use the `keyframe_insert`-function, e.g. like this: 
`orbit.data.keyframe_insert(data_path="eval_time", frame=1)`

* If you used ellipses, then the speed of the planets should be faster closer to the sun (according to Kepler's laws). Blender does not easily allow to do that, so we will ignore this here. Just be aware that the true speed would be different than what we currently have.


##Rotation animation
Planets also rotate around their own axes, that's given by `rotperiod` in the file. This gets slightly more complicated than just adding animation keyframes for the `z`-rotation values, because the planet's axes are already tilted. If a z-rotation is added, then the planet would rotate around the current z-axis, not around the planet-axis. You can see this easily with Saturn and its rings or Earth, when changing the z-rotation value in the *3D view*, properties panel (enable with `N` if it is hidden).

We therefore use a special trick: we add an axes object for each planet and assign it the axial tilt. Then we clear the rotation of the planet and *parent* it to the axes object. This has the effect that the planet is basically unrotated, but inherits the tilt from its parent axes object. Now it's possible to keyframe the z-rotation of the planet!

* Use `Add`, `Empty`, `Arrows` in the interface and check from the log-output which function was used. Add this function in your script to create such arrows for each planet. Give it a name like `Planet-Earth-Axes` etc. for clear identification and to include it in the deleting process at the beginning of the script. 

* Assign the planet's tilt angles to the corresponding axes object.

* Clear the planet's rotation angles, i.e. set them to (0,0,0).

* Add the axes-object as parent to each planet. In the interface, select a planet, go to the *Properties* area, switch to the *Object* tab and look for `Parent` at the *Relations*-section. Here one can enter the axes object. Check the tooltip for the field to get an idea how to include setting the parent in your script.

* So far, nothing much has changed, the planets should still look the same. But now we are ready to add the rotation animation. Let's do it first in the interface:
  - Select a planet (not it's axes!).
  - In the *Timeline*, set the time to frame 1.
  - In *3D view*, go to the properties region at the right side and look for the rotation. The `z rotation` should be 0. Hover with the mouse over this field and press the `I` key to insert a keyframe.
  - Set the time to the rotation period, e.g. 10, set the rotation to 360 degrees and again insert a keyframe.
  - Move the time slider to see the planet rotating around its axis.
  - Switch your *Python Console* area (or any other) to the *Graph Editor* area, again set the `Interpolation` type to `Linear`.
  - Add a `Cycles` modifier and set Before and After values to `Repeat with Offset`, just the same way as for the orbit animation. This ensures a continuous and smooth planet rotation.

* Include these steps in your script, for each planet and for the Sun.


##Render your animation
* Render your animation by selecting `Render`, `Render Animation` in the top menu. The render resolution and other properties can be adjusted in the *Properties* area, at the *Render* tab (photo camera symbol). By default, Blender will create one png-image for each frame in the `tmp`-directory. 

* You can stop the rendering any time using the `Esc` key.

* Play your rendered animation with Blender, using `Render`, `Play Rendered Animation`.

* It is also possible to render your frames in the background, using the command line:

    ```
    blender -b <blender-file> -s 1 -e 600 -a
    ```

  This will render the frames 1 to 600.


##Further improvements
The solar system that we built up to now is still lacking in many details. Here are some suggestions to improve it further:

* Use real distances (scaled down by the same factor) for planets from the Sun.
* Switch on shadows for the lamp, so that rings and moons can cast shadows on their planets. This was switched off initially, because we had the planets unrealistically close to each other.
* Make orbits eccentric, use correct orbit orientation.
* Use true (non-uniform) speed along eccentric orbits.
* Use different image textures (e.g including clouds for Earth and Venus).
* Use animated textures, e.g. for the Sun to mimick evolving Sun spots, or for Earth to have different clouds evolving with time.
* Use UV-unwrapping for a more accurate mapping of textures to the sphere, especially at the poles.
* Add moons, minor planets and asteroids.
* Add stars in the background as reference system, maybe even the true stars from the sky, using a sky map.


If you made it this far: thanks for staying with me and congratulations! I hope you enjoyed this tutorial. For comments and suggestions, mistakes or questions, please send a mail to kristin.riebe@mk-star.de.
