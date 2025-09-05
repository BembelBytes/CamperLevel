# CamperLevel
This script can be used to calculate the optimal positions of leveling ramps to level the RV.

## 1 Preparation
Before being able to use this script, you need to evaluate two values that are specific to your combination of leveling ramps and RV.
Place your RV with **one** wheel to the top position of your ramp and note the effect on your RVs pitch and bank in ° [degrees].

## 2 Usage
The script can either be used directly by executing the file or ist can be imported as a python module and executed by using the `Camper` class.  
Pitch and bank values are expressed in degrees where positive pitch values corresponds to a nose high (front of car higher than the tail) and positive bank values corresponds to an incline to the right (right side of car lower than left side).

### Direct usage
1) Go to the end of the script and modify the values of `MY_PITCH_PER_RAMP` and `MY_BANK_PER_RAMP` to fit the effect of your ramps to your RV as measured according to the procedure described above.

2) Use python to execute the script. You will be asked to enter the current attitude (pitch and bank) of your RV **without any ramp under your wheels**.

3) The best position of your ramps will be displayed together with the attitude before and after the usage of the ramps and the amount of correction that could be applied using your ramps.

```
python camper.py
Enter the attitude of your RV without any ramps below your wheels
Pitch (+ is nose up): 0.8
Bank (+ is right side low): -0.3

RAMPS:
Front:     0% |   0%
Rear:     59% |  39%


ATTITUDE:
       BEFORE | AFTER
Pitch:  +0.8° | +0.0°
Bank:   -0.3° | -0.0°
Total:  +0.9° | +0.0°


CORRECTION:       99%
```

### Usage as module

```py
# Import the Camper class
from camper import Camper

# Create the Camper object
# The value for pitch and bank per ramp can be set during initialization
camper = Camper(0.5, 1.25)

# Enter pitch and bank values without ramps applied
camper.pitch = -1.2
camper.bank = 0.2

# Get best possible attitude after applying the ramps
print(camper.best_attitude)

"""
Ramps:
  FL:  91%, FR:  99%
  RL:   0%, RR:   0%

Attitude:
  Pitch: -0.2°
  Bank:  +0.1°
"""
```

## 3 Changelog
### V1.0.0
Initial Release

### V1.0.1
- Bugfix in calculation of best attitude
- Refactoring

## 4 License
Copyright (c) 2025 Aljoscha Greim aljoscha@bembelbytes.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.