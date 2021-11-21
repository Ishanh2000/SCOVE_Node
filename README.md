# SCOVE_Node
Smart CoVID Entrance IoT Project (Node Level)

A smart entrance device that detects temperature of the subject (face detection and temperature sensing) and whether he has worn mask or not (mask detection), then allows entry based on whether his face qualifies for entrance or not (face recognition). This is a part of the group project for the course CS698T (Intoduction to Internet of Things and Its Industrial Applications) taught by Dr. Priyanka Bagade at Indian Institute of Technology Kanpur in the fall of 2021 (2021-22-1).

The node will be a Raspberry Pi 4 Module, integrated with Pi Camera, InfraRed temperature sensor and proximity/motion/ultrasonic sensor. Further additions are possible too.

This repository is just one part of the complete project. The other repository [SCOVE_Web](https://github.com/rkchaudhary4/SCOVE_Web) is an Angual web application which communicates with our node(s).

### Resources

- Web Application Repository: https://github.com/rkchaudhary4/SCOVE_Web
- Similar Paper: https://www.jetir.org/view?paper=JETIR2107233
- Others: https://1drv.ms/u/s!ApA9gmreFg4nhcpSkhy20n7BuzpWQA?e=R1qTxy

### Running on Node (Raspberry Pi 4)

This repository runs on Python3. For running this repository on the edge device, the following need to be installed: RPLCD, smbus2, mlx90614, RPi, requests, tensorflow, numpy, opencv-python, imgaug, scikit-learn

Most of these can be installed by running (assumiing Python3 and pip3 are installed):
```
$ pip3 install RPLCD smbus2 mlx90614 RPi
$ pip3 install requests
$ pip3 install numpy scikit-learn tensorflow
$ pip3 install imgaug
$ pip3 install opencv-python
```

Then run
```
$ git clone https://github.com/Ishanh2000/SCOVE_Node
$ cd SCOVE_Node
$ mkdir img # if not exists
$ python3 main.py
```

Please note that you may have to goto Start >> Preferences and enable Camera and I2C in correspoding tabs. You may check out
this link: [https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/)

### Running as Server

This repository runs on Python3. For running this repository as a server, the following need to be installed: flask_pymongo, flask, flask_cors, tensorflow, numpy, opencv-python, imgaug, scikit-learn

Most of these can be installed by running (assumiing Python3 and pip3 are installed):
```
$ pip3 install flask flask_cors flask_pymongo
$ pip3 install numpy scikit-learn tensorflow
$ pip3 install imgaug
$ pip3 install opencv-python
```

Then run
```
$ git clone https://github.com/Ishanh2000/SCOVE_Node
$ cd SCOVE_Node
$ mkdir img # if not exists
$ export FLASK_APP=server
$ flask run --host=0.0.0.0
```

### Installation Issues

Sometimes packages like RPLCD, smbus2, mlx90614, opencv-python, tensorflow, imgaug, etc. can give dependency problems. There is no direct solution to handle such issues. Maybe, for opencv-python (most common problem), you may refer to [https://github.com/opencv/opencv-python/issues/](https://github.com/opencv/opencv-python/issues/) and other GitHub issue pages. Sometimes maually installing packages from their source repositores may even help.

If there are yet any issues, please contact the team members given below. We shall be very happy to help.

### Team Members

- Arpit Agarwal (180139): arpitarg@iitk.ac.in
- Ishanh Misra (180313): imisra@iitk.ac.in
- Rishabh Kumar Chaudhary (180609): rishukc@iitk.ac.in
- Yuvraj (180898): yuvrajg@iitk.ac.in

### TODO

Maintain TODO list here.
