
from inputs import get_gamepad

# Dictionary of game controller buttons we want to include.
#TRIGERS USE FOR SPEED OF THE 
controller_input = {'L_trig': 0, 'R_trig': 0, 'A': 0, 'B': 0}


def gamepad_update():
    # Code execution stops at the following line until gamepad event occurs.
    events = get_gamepad()
    return_code = 'No Match'
    for event in events:
        event_test = controller_input.get(event.code, 'No Match')
        if event_test != 'No Match':
            controller_input[event.code] = event.state
            return_code = event.code
        else:
            return_code = 'No Match'
 
    return return_code
 










 def main():
    """ Main entry point of the app """
    while 1:
        # Get next controller Input
        control_code = gamepad_update()
        
        if control_code == 
 
#-----------------------------------------------------------
 
if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()