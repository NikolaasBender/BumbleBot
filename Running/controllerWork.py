
import pygame
import time
 
pygame.init
pygame.joystick.init()
 
# Get count of joysticks
joystick_count = pygame.joystick.get_count()
 
# Wait until joystick is connected
while joystick_count < 1:
    print("joystick not connected")
    # Sleep for 1 second
    time.sleep(1)
 
print(joystick_count)
 
# For controlling robots we would only be
# connecting 1 joystick controller. So we
# connect to the first available controller.
# So the first joystick will be at index 0.
joystick = pygame.joystick.Joystick(0)
joystick.init()
 
name = joystick.get_name()
print("Joystick name: {}".format(name) )
 
axes = joystick.get_numaxes()
print("Number of axes: {}".format(axes) )
 
for i in range( axes ):
    axis = joystick.get_axis( i )
    print("Axis {} value: {:>6.3f}".format(i, axis) )
 
buttons = joystick.get_numbuttons()
print("Number of buttons: ", buttons)
 
for i in range( buttons ):
    button = joystick.get_button( i )
    print("Button {:>2} value: {}".format(i,button) )
 
hats = joystick.get_numhats()
print("Number of hats: {}".format(hats) )
 
for i in range( hats ):
    hat = joystick.get_hat( i )
    print("Hat {} value: {}".format(i, str(hat)) )