import os
from gpiozero import Robot
import pygame

pygame.init()

robot = Robot(left=(26, 19), right=(13, 6))

def stop():
	robot.stop()


def snap():
	cmd = "streamer -f jpeg -o /home/pi/images/$DATE. " + string(time()) + ".jpeg"
	os.system(cmd)
	return

while True:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				robot.forward()

			if event.key == pygame.K_DOWN:
				robot.backward()

			if event.key == pygame.K_RIGHT:
				robot.right()

			if event.key == pygame.K_LEFT:
				robot.left()

			if event.key == pygame.K_p:
				snap()

		if event.type == pygame.KEYUP:
			stop()

	clock.tick(60)

pygame.quit()
quit()