from __future__ import print_function

import time
from sr.robot import *

""" Inizialization global variable"""

""" Initializing lists which contain codes already placed"""
silver_code = []
golden_code = []

""" float: Threshold for the control of the linear distance"""
a_th = 2.2

""" float: Threshold for the control of the orientation"""
d_th = 0.5

""" instance of the class Robot"""
R = Robot()

def drive(speed, seconds):
        """
    	Function for setting a linear velocity
    
    	Args: speed (float): the speed of the wheels
	      seconds (float): the time interval
        """
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	"""
    	Function for setting an angular velocity
    
    	Args: speed (float): the speed of the wheels
	      seconds (float): the time interval
    	"""
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def search_silver_token():
	"""
    	 Function to find the closest silver token

    	 Returns:
	 	 dist (float): distance of the closest silver token (-1 if no silver token is detected)
	         rot_y (float): angle between the robot and the silver token (-1 if no silver token is detected)
	         code (int) : token's identification code (-1 if no silver token is detected)
	"""
       
	dist = 100
	for token in R.see():
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER:
			dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code  
    	if dist==100:
		return -1, -1, -1
    	else:
   		return dist, rot_y, code

def search_golden_token():
	"""
        Function to find the closest golden token

        Returns:
	       dist (float): distance of the closest golden token (-1 if no golden token is detected)
	       rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
	       code (int): token's identification code (-1 if no golden token is detected)
	"""
	dist=100
	for token in R.see():
        	if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code 
	if dist==100:
		return -1, -1, -1
    	else:
   		return dist, rot_y, code

def bring_to_golden(x):
	"""
	Function to find the golden token in which to bring the silver token (which has been taken in the grab_silver function)
	
	This is a void function and only when x=0 the program will finish through exit() function
	
	"""
	while 1:
		dist, rot_y, code = search_golden_token()
		
		if code in golden_code: # If code is in golden_code list, we assign dist = -1
			dist = -1
		
		if dist==-1: # if no token is detected (because dist = -1), we make the robot turn 
			print("I don't see any golden token!!")
			turn(+15.0, 1.0)
			
		elif dist <1.2*d_th: # if we are close to the golden token, we try release it.
		
			if R.release(): # if we release the token
				golden_code.append(code) # we append the token's code inside golden_code list
				
				if x==0: # when x=0 we understand that the robot has done its job, so we've finished all its tasks
					print('well job!')
					exit()
					
				drive(-17.0, 1.2)
				turn(2,2)
				grab_silver(x) # after having released the token, we do the same task for the next tokens
			
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(30.0, 0.5)
		
	    	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
			turn(-2.0, 0.5)
		
	    	elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
			turn(+2.0, 0.5)

	
def grab_silver(x):
	"""
	Void function to grab the silver token 
	
	"""
	while 1:
		dist, rot_y, code = search_silver_token()
		
		if code in silver_code: # If code is in golden_code list, we assign dist = -1
			dist = -1
		
		if dist==-1: # # if no token is detected (because dist = -1), we make the robot turn 
			print("I don't see any silver token!!")
			turn(+15.0, 1.0)
			
		elif dist <d_th: # if we are close to the token, we try grab it.
			print("Found it!")
			if R.grab(): # if we grab the token
				print("Gotcha!")
				silver_code.append(code) # we append the token's code inside silver_code list
				x-=1 # we decrease x value each time we grab a silver token
				turn(-17.0,2.5)
				bring_to_golden(x)
			else: # this else needs to move forward the robot in order to grab the token at the right distance
				drive(10.0,0.3)
				    	
		elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			drive(30.0, 0.5)
		
	    	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
			turn(-2.0, 0.5)
		
	    	elif rot_y > a_th:
			turn(+2.0, 0.5) # if the robot is not well aligned with the token, we move it on the right

def main():
	""" int: Number of silver and golden pairs in order to undestand when the robot will finisch its tasks"""
	x=6	
	grab_silver(x)

main()
