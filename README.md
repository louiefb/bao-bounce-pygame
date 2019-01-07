# bao-bounce-pygame
A highly customizable dodge game created with PyGame

The Game
--------
Bao Bounce is your simple dodge game and the objective is to survive as long as possible without getting hit by enemies. Use the directional keys to play and the Esc key to exit.

What Makes Bao Bounce Different
-------------------------------
A lot of the elements in the game can be customized. And each user-defined change can impact gameplay making it relatively easier or substantially harder. The elements that can be changed are as follows:

1. Gravity
Getting rid of gravity truly simplifies the game, making movements rudimentary. The goal is to have an appeal to retro gamers and ultra-retro gamers (I'm thinking of Nokia gamers?) alike.

2. Momentum
This is the term employed when referring to the follow-through of sideways movements. Momentum can be toggled to allow residual movement to occur after the user has let go of the left or right key.

3. Traction
Traction can be adjusted by value. This is how much residual sideways movement (momentum) is applied after Bao has tumbled to the ground. The Default is 0.3. The maximum is 2.0. Zero can be used but this translates to toggling momentum off.

4. Sensitivity
Sensitivity can be adjusted by value. This is how many pixels Bao moves upon hitting a key. A higher value means more travel. The Default is 15. The minimum is 10 and the maximum is 30 pixels.

5. Sticky vs. Slippery
Sticky floors means sideways movement across the floor eventually stops, just as it should in real life. Slippery means floor movement may go on forever (depending on whether Wall Bounce is enabled).

6. Wall Bounce
If on, Bao would bounce off the side walls and get affected by its momentum. If disabled, the walls would simply halt Bao from going beyond the screen and absorb all the momentum.

7. Spawn Origin
Users can specify where the enemies will come from, and can even turn off enemies altogether. At a maximum, enemies can come from the left and right sides, and from the top.

8. Spawn Rate
Users can also tune the difficulty by setting how often the enemies appear, in milliseconds. Easy is 1500ms, Medium is 1000ms, and Hard is 500ms.

Everything in the game is done in a very Pythonic way, with gravity, momentum, and all these parameters executed through variable updates, conditions, and flags instead of a physics engine or a complicated library.

Progress
--------
Actual sprites have been implemented. Next steps: user interaction including the Title Screen and how an end user will be able to customize the game through the game and not through the script.
