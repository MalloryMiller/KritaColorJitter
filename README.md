<!DOCTYPE html
<html lang="en">


<body>
  <a href="https://github.com/MalloryMiller/KritaColorJitter/wiki"><p align="center"> <img src="logo.svg" alt="css-in-readme"> </p></a>
  <p align="center">Intuitive color jittering for any brush.</p>

  <h2>Description</h2>
  <p>This plugin endeavors to allow color jitter, also sometimes called color dynamics, in Krita. While there is a way to create stamps <a href="https://www.youtube.com/watch?v=-WSQvjhjT3o">where each stamp is a slightly different color</a>, I could find no way to allow a brush to change color slightly with each stroke with the extensibility that other art programs do in default Krita.</p>
  <p>With color jittering active, every stroke (or fill tool) you make will have a slightly different color. While active, color jittering allows for effortlessly subtle hue, value, and saturation variation without needing to reswatch colors for every single stroke.</p>


  <h2>Setup</h2>
  <p>Check if you have a version of Krita that this plugin will work for:</p>

✅ Linux 64-bit appimage 5.2.2
 
⚠️  Windows 11 (known issue with slightly drifting base color, otherwise functional)
 
⬜  MacOS (untested)

  <p> I haven't tested this plugin on everything, so even if it's not on this list feel free to try it out and let me know if it works or if you run into any issues! There shouldn't be any other dependencies.</p>
  <p>From this page, scroll up and click the blue "Code" button and then "Download ZIP." In Krita, go to the bar at the top and navigate to "Tools" > "Scripts" > "Import Python Plugin From File." After clicking on that, find the downloaded .zip file and select it.</p>
  <p>The added plugin may be automatically turned on, but go to "Settings" > "Configure Krita" and scroll to the bottom of the left pannel to find "Python Plugin Manager." Ensure that ColorJitter is checked off there. If ColorJitter seems not to be working at this point, close and reopen Krita.</p>


  <h2>Usage</h2>
  <p>You can probably figure out how to work it by experimenting, but if you get confused this is here to help. This plugin is primarily controlled by its Docker. If the docker isn't automatically on your screen, navigate to "Settings" > "Dockers" > "Color Jitter" and click that to turn it on. </p>
  
  <h3>1. Stroke Color Jitter</h3>
  <p>This first option is off by default. Toggling on this option in the Color Jitter Docker will activate color jittering. While this option is checked, your active color will be switched to a jittered one right after you finish a stroke, a fill tool use, or any action that can be undone. If you select a new color from any of the color selection dockers, that color will be set as the new Base Color. When you uncheck this option your active (foreground) color will switch back to your base color. </p>

  <h3>2. Jitter Ranges</h3>
  <p>Most of the Color Jitter Docker consists of three options labeled "Hue Range", "Saturation Range", and "Value Range". Each of these function the same, but affect different aspects of the colors being selected when a new color is picked by the plugin. The value entry box (which by default has "25.00%" in it) controls the range of the colors that could be picked by a given jitter. A value of 25% entered here means that 25% of all possibilities are included (12.5% left of your base color's respective value, 12.5 right). 100% means that 50% to the left and 50% to the right of your base Color is possible.</p>
  <p>The dropdown menu under the range corresponds to the one above it. The default is Random, which means any value in the range is equally likely, but you can also change it to be Normal. This means that values closer to your base color are much more likely than ones far away. You may need to give Normal distributions a larger range for the desired affect.</p>
  <p>n.b. in the extremes of Value and Saturation 100% will only give about 50% variation. (for white it may have 50% below, 0% above because there are no values above). For this reason, you can adjust the ranges to up to 200%. <b>Using a value over 100%, however, may cause probablities to behave unexpectedly in other circumstances.</b></p>

  <h3>3. Shortcuts</h3>
  <p>Three default shortcuts can be used: Ctrl+Alt+A (generate new random color), Ctrl+Alt+Z (return to original color), and Ctrl+Alt+X (set current color as the new base color). You can configure these shortcuts to be different in "Settings" > "Configure Krita" if you would like, and I recommend binding a button on your tablet to Ctrl+Alt+A if you use one and think you'd like more control over generating new colors. By holding Ctrl+Alt+A and watching your color selector of choice you can also get an idea of what colors are included in the ranges you've set.</p>


  <h2>Feedback</h2>
  <p>If you find any issues using this plugin (which has been best tested using the Linux 64-bit appimage version of the software on version 5.2.2, but not as carefully tested otherwise), please submit an issue on its <a href="https://github.com/MalloryMiller/KritaColorJitter/issues">Github Issues page</a> with the "bug" label if you get the chance.</p>

  <h2>Credits</h2>
  <p>I looked at <a href="https://github.com/EyeOdin/Pigment.O">Pigment.O</a> quite a bit as reference since it dealt with colors. I used the VSCode <a href="https://github.com/cg-cnu/vscode-krita-plugin-generator">Krita Plugin Generator</a> extension to generate a base to build from for the extension and docker. I also used some code from <a href="https://krita-artists.org/t/how-can-i-listen-to-foregroundcolorchanged/40889/13">this thread</a>; all hail <a href="https://krita-artists.org/u/seguso/summary"> seguso</a>  </p>

</body>

</html>
