# Ti UNO
*A simple UNO implementation for the TI-82 Advanced Python Edition calculator.*

## Overview
TI Uno is a lightweight, terminal app UNO clone written in Python specifically for the TI-82 Advanced Python Edition calculator by Texas Instruments. It was made mostly as a fun side project (= "a waste of time") and is now released as open source for anyone who wants to learn from it, improve it, or just play UNO on their calculator.

There are *two versions* included:
- ```ti_uno.py``` - The version that actually runs on the calculator (tested on real hardware).
- ```ti_uno_advanced.py``` - A more advanced version that did not fit or run on the calculator (kept for reference and future optimization).

The advanced verion includes centered printing and a UNO declaration mechanic where players must memorize and use UNO codes assigned at the start of the game.

## Calculator Constraints
The TI-82 Advanced Python Edition has a display size of 32 characters x 11 lines. It supports ANSI color codes in the console.
Python scripts have around 18 KB of RAM available to them.

## Features
- 2-4 local multiplayer (players pass the calculator around).
- Works on actual TI hardware (main version).
- Simple console UI using ANSI colors.
- All the basic card mechanics (+4, Reverse, Skip, Debt accumulation).

In ```ti_uno.py```, near the top of the file, you will find a set of commented / uncommented lines that determine which ANSI color codes the game uses. Calculator compatible colors are enabled by default, the standard ANSI colors for PC terminals are commented out. Simply swap the commenting for testing on the PC. 

## Installation
1. Transfer ```ti_uno.py``` to the calculator via "ti Connect SE" app and a USB-B mini cable.
2. Run the file from the Python82 App.
3. Wow done
