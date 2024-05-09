# kukavarproxy_to_kukasim - Fork of py_openshowvar
Python port of KUKA VarProxy client to KUKA SIM 
# Python Version
Python 2.7 (as KUKA SIM still only support Python 2.7), but can be easily modified for Python3.x

# Installation Steps for KUKA KRC4 to KUKA SIM
This is an unofficial step to simulate/ have a digital representation of the robot in KUKA SIM
With newer version of KUKA SIM 4.3x, this repo may be irrelevant!! as you can visualize the robot directly using the option shown below by being connected to the controller.

This option directly uses KRC4 controller's KSI option, so no hassle of changing network configuration which will be performed in this repo. I recommend using this option. 
##CAUTION: Refer to KUKA Documentation and training for this, as sending program files directly from KUKA SIM to controller and simulating it, may erase your entire robot controller, as the config.dat is modified during this process!!!
Please refer to official documentation from KUKA Support to properly execute this. It is quite straightforward. 
However, since we dont follow straight-forward steps, here is the unofficial way !!

## Steps for Real-time visualization using python port
This method follows a round-about way to visualize any program being executed on the KUKA KRC controller in KUKA SIM.
Limited testing has been performed. Follow the documentation at your own risk !!!

### Configuring KLI on KUKA Controller
1. First take a backup image of the KUKA Controller using the KUKA pendrive.
2. Follow the KUKA Official documentation for backing up the controller.
#### Quick steps for backup
a. Plug the KUKA pendrive into you laptop, inside the image folder, copy the contents of the existing backup to your harddisk/laptop
b. Power-down completely your KUKA robot and controller, plug-in your KUKA pendrive into the KUKA controller and switch-on the KUKA controller
c. You must notice that the Teach-pendant blacks-out for a moment and switches-off, but the blue-light is blinking on the KUKA pendrive, this means that the backup is in progress
d. Once backup is completed, the controller automatically turns-off and the pendrive blue-light blinking stops. 
e. Power down the robot controller and remove pendrive.
Follow KUKA's official documentation for safe backup

#### Configure KLI Network on Robot controller and KUKAVARPROXY installation
Just follow [https://www.youtube.com/watch?v=ucBxMxYJqIg&ab_channel=rebots](https://www.youtube.com/watch?v=ucBxMxYJqIg&ab_channel=rebots)
Best explanation on how to configure KLI and KUKAVARPROXY !

#### Install py_openshowvar
Follow this repo for establishing python communication with the robot
[https://github.com/linuxsand/py_openshowvar/tree/master](https://github.com/linuxsand/py_openshowvar/tree/master)
Open command prompt with administrative priveldges
```
pip install py-openshowvar
```

#### py_openshowvar for KUKA_SIM
1. Open KUKA SIM
2. Open one of the demo-layout, I have used KUKA Ready2Educate cell as we have that cell at our premise.
3. You should model the simulation of the task, in simulation by yourself of the actual robot cell you have in KUKA SIM
4. Once this is done, it is straightforward to see the simulation











