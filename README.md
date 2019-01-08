# BumbleBot
This is the work for bumblebot 

BumbleBot is like a roomba but more pointless. 
I am making this to  teach myself python, vision systems, motor control, and how to use a combination of cloud and edge computing to acheive the goal I have set for myself.

BUILD LOG
==========

PHASE 1
==========
This phase was all about hardware and getting anything to work. So I learned a lot about batteries, motor controllers, and buying DC to DC converters on amazon. I started with a custom design for the robot chassis and had to abandon that design due to time. Hardware for this project could be a project on its own, so I got my hands on one of those arduino robot kits from amazon. They work on the same principal as the full sized robot so everythong carries over but I don't have to worry about acrylic cement. At the end I had all of the hardware done, and some small fires put out so on to phase 2.

PHASE 2
=========
This phase was all about the software. This is all of the test code and learning the hard way to make motors spin with python code. The motors were actually the easy part, it was the ultrasound sensors that drove me up a wall. The US (ultrasound) sensors are incredibly inconesistent so I had to devise a way to get usable numbers form them in a timely fashion. the algorithm I settled on was one of taking ten measurments then sorting those measurements. Then using the median mesurement and averaging all measurements that were within 50% of that median measurement. This algorithm works well. Whats nice too is that at smaller distances the outlier rejection becomes stricter. All of this was nicely wrapped into Bumble2.py. 

PHASE 2.5
=========
This is an intermediary phase. Here I cleaned up the code and made it more useable, I also added gamepad support so the robot can be driven by an xbox controller. This phase is really preparing for the machine learning component of this project and collecting data for the neural net. 

PHASE 3
=========
This is the phase where the project is now. I need to do a lot of data collection and data processing for the neural net. I have never done this before so its an enormous learning curve but that hasn't stopped me yet. I am testing with different data processing and collection techniques to continue the project as efficiently as possible. I have decided on using tensorflow and keras in a convolutional neural net as the training and building system for the ai but the actual data collection part of this system has yet to be fully sorted out. 

PHASE 3.5
=========
This is where I will be using the cloud computing to train larger and more complex models for the robot. I have no idea how tricky this will be but I know that tensorflow has to be recompiled to run on a ten year old craigslist server. This server infastructure is the cloud component of the project that will be collecting new data as the robot is out and about and using that new data to train new models that can be uploaded and used on the robot.

PHASE 4
=========
This is so far in the future I just want to put all goals aceived here. The fully built BumbleBot chassis, the long range battery system and all of the AI, but I am more focused on the machine learning aspects as of writing this. There will be more to report in the future but for now, phase 4 should be the final phase.

UPDATED (1/7/19)
