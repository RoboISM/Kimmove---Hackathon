#Kimmove - Emulating *MS Kinect*.

>"Kimmove" recognizes human interfaces and gestures, hence allows FPS gaming just by hovering "Kimmove" in the air with all the buttons wirelessly embedded into a single device . This relishes the user's gaming experience by satiating the true gaming spirit. This project can be extended by integrating it with the micro-controller and using an array of IR blasters to detect the depth and human gestures more effectively and precisely.

##Prerequisites
Though *Kimmove* is a plug and play device, but for interfacing it with your machine.The following requirements must be met.  
**OS** - Windows  
**Graphic memory** - N/A  
**RAM** - N/A  
**Peripheral** - Bluetooth,camera (atleast 320x480)  
**FPS** - Any
**Dependencies** - pyautogui,pygame(only if GUI interface is required).
**OpenCV** - Not required (standalone executable).

The device can be operated in two modes:  
* Navigation Mode
* Gaming Mode

In **navigation mode** the handheld can be used for controlling your mouse pointer.
In **gaming mode** the handheld will control your movements in FPS.

##Code snippets:
[NavMode.cpp](https://github.com/markroxor/Kimmove---Hackathon/blob/master/NavMode.cpp)
and 
[GameMode.cpp](https://github.com/markroxor/Kimmove---Hackathon/blob/master/GameMode.cpp)
differ at line *133-134*

``` C++
SetCursorPos(-pposX+posX+FRAME_WIDTH/2,-pposY+posY+FRAME_HEIGHT/2);
SetCursorPos(posX, posY);
```
In *navigation mode* the co-ordinates of cursor are directly mapped to the desktop screen.
while in *gaming mode* the co-ordinates of cursor which are mapped from a 2 dimensional screen for a 3 dimensional gameplay by adjusting the x and y coordinates according to the frame size.

##Handheld:
It is embedded with three *SPST* buttons on the front, a *thumb* button at the rear and a *I/O* switch below.  
The front three buttons are for _Left,right click_ and _reload_.  The *thumb* button is for switching between the two modes of operation. The _I/O_ button powers up the Arduino board and HC-05 (bluetooth module).

##Usage:
* Execute GUI.py, which will guide you further.
  
[![IMAGE ALT TEXT](http://img.youtube.com/vi/h4vNtrnT10Q/0.jpg)](http://www.youtube.com/watch?v=h4vNtrnT10Q "Kimmove")


> Standalone bundle.  
> With background noise cancellation and fine color tuning.  
> Button deboucing mechanism.  
> A 9V replaceable battery.
> Tested on: i3120m (mobile), 4GB RAM, AMD 7680,Windows 10, Call Of Duty ModernWarfare - 1 and 3  
> Cost of device - with:
* **Arduino Uno** development board is around _1000 INR_  
* **Arduino nano** development board is less than _500 INR_ (with no reduction in performance.)
