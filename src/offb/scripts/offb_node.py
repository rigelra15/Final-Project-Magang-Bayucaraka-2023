# Rigel Ramadhani Waloni
# 5024221058

#! /usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import State
from mavros_msgs.srv import CommandBool, CommandBoolRequest, SetMode, SetModeRequest
import cv2 as cv
import qrcode

current_state = State()

# As a substitute for the duration of the program or command is executed
detect = -1
start = -1

def state_cb(msg):
    global current_state
    current_state = msg

# Create a VideoCapture Object
# The argument '0' gets the default webcam
cam = cv.VideoCapture(0)

# For Capturing QR Code Object
detector = cv.QRCodeDetector() 

if __name__ == "__main__":
    rospy.init_node("offb_node_py")

    state_sub = rospy.Subscriber("mavros/state", State, callback = state_cb)

    local_pos_pub = rospy.Publisher("mavros/setpoint_position/local", PoseStamped, queue_size=10)
    
    rospy.wait_for_service("/mavros/cmd/arming")
    arming_client = rospy.ServiceProxy("mavros/cmd/arming", CommandBool)    

    rospy.wait_for_service("/mavros/set_mode")
    set_mode_client = rospy.ServiceProxy("mavros/set_mode", SetMode)

    # Setpoint publishing MUST be faster than 2Hz
    rate = rospy.Rate(20)

    # Wait for Flight Controller connection
    while(not rospy.is_shutdown() and not current_state.connected):
        rate.sleep()

    pose = PoseStamped()

    # Send a few setpoints before starting
    for i in range(100):   
        if(rospy.is_shutdown()):
            break

        local_pos_pub.publish(pose)
        rate.sleep()

    offb_set_mode = SetModeRequest()
    offb_set_mode.custom_mode = 'OFFBOARD'

    arm_cmd = CommandBoolRequest()
    arm_cmd.value = True

    last_req = rospy.Time.now()

    cam = cv.VideoCapture(0)

    while(not rospy.is_shutdown() and (start < 0)):
        rate.sleep()
        if (detect < 0):
            ret, frame = cam.read() # Capture frame-by-frame

            if ret == True:
                cv.imshow("Tes", frame)
                data, bbox, straight_qrcode = detector.detectAndDecode(frame) # Retrieve data from the detected QR Code

                if len(data) > 0:
                    if data == "House":
                        detect = 1
                        rospy.loginfo(f"QR Code Detected! Draw a {data.upper()}!") # Display the log
                        cam = cv.VideoCapture(-1) # Alternative Way to Turn Off the Webcam

                        pose.pose.position.x = 0
                        pose.pose.position.y = 0
                        pose.pose.position.z = 3

                    elif data == "Square":
                        detect = 2
                        rospy.loginfo(f"QR Code Detected!: Draw a {data.upper()}!") # Retrieve data from the detected QR Code
                        cam = cv.VideoCapture(-1) # Alternative Way to Turn Off the Webcam

                        pose.pose.position.x = 0
                        pose.pose.position.y = 0
                        pose.pose.position.z = 3

                    elif data == "Stop":
                        rospy.loginfo(f"QR Code Detected!: {data.upper()}!") # Retrieve data from the detected QR Code
                        raise SystemExit # Stop the Execution

                    else:
                        rospy.loginfo(f"QR Code Detected!: {data} - Sorry, I don't recognize that command.")
                        rospy.loginfo("Try another QR Code.")

        # DRAW A HOUSE
        elif (detect == 1):
            a = 0
            while(not rospy.is_shutdown() and detect == 1):
                if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                    if(set_mode_client.call(offb_set_mode).mode_sent == True):
                        rospy.loginfo("OFFBOARD enabled")
            
                    last_req = rospy.Time.now()
                else:
                    if(not current_state.armed and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                        if(arming_client.call(arm_cmd).success == True):
                            rospy.loginfo("Vehicle armed")
            
                        last_req = rospy.Time.now()

                # Garis 1 // Line 1
                if (a >= 300 and a < 400):
                    if (a == 300):
                        rospy.loginfo("Go To (0,-7)")
                    pose.pose.position.x = 0
                    pose.pose.position.y = -7

                # Garis 2 // Line 2
                elif (a >= 400 and a < 500):
                    if (a == 400):
                        rospy.loginfo("Go To (12,-7)")
                    pose.pose.position.x = 12
                    pose.pose.position.y = -7

                # Garis 3 // Line 3
                elif (a >= 500 and a < 600):
                    if (a == 500):
                        rospy.loginfo("Go To (12,0)")
                    pose.pose.position.x = 12
                    pose.pose.position.y = 0

                # Garis 4 // Line 4
                elif (a >= 600 and a < 700):
                    if (a == 600):
                        rospy.loginfo("Go To (6,10)")
                    pose.pose.position.x = 6
                    pose.pose.position.y = 10

                # Garis 5 // Line 5
                elif (a >= 700 and a < 800):
                    if (a == 700):
                        rospy.loginfo("Go To (0,0)")
                    pose.pose.position.x = 0
                    pose.pose.position.y = 0

                # Garis 6 // Line 6
                elif (a >= 800 and a < 900):
                    if (a == 800):
                        rospy.loginfo("Go To (12,0)")
                    pose.pose.position.x = 12
                    pose.pose.position.y = 0

                # Kembali ke Home (0,0) // Back to Home (0,0)
                elif (a >= 900 and a < 1000):
                    if (a == 900):
                        rospy.loginfo("Go To Home (0,0)")
                    pose.pose.position.x = 0
                    pose.pose.position.y = 0

                # Landing
                elif (a >= 1000 and a < 1100):
                    if (a == 1000):
                        rospy.loginfo("Landing...")
                    if (a == 1099):
                        rospy.loginfo("DONE!")
                        cam = cv.VideoCapture(0)
                        detect = -1
                        a = 0
                    pose.pose.position.x = 0
                    pose.pose.position.y = 0
                    pose.pose.position.z = 0

                a = a + 1

                local_pos_pub.publish(pose)

                rate.sleep()

        # DRAW A SQUARE
        elif (detect == 2):
            a = 0
            while(not rospy.is_shutdown() and detect == 2):
                if(current_state.mode != "OFFBOARD" and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                    if(set_mode_client.call(offb_set_mode).mode_sent == True):
                        rospy.loginfo("OFFBOARD enabled")
            
                    last_req = rospy.Time.now()
                else:
                    if(not current_state.armed and (rospy.Time.now() - last_req) > rospy.Duration(5.0)):
                        if(arming_client.call(arm_cmd).success == True):
                            rospy.loginfo("Vehicle armed")
            
                        last_req = rospy.Time.now()

                # Garis 1 // Line 1
                if (a >= 300 and a < 400):
                    if (a == 300):
                        rospy.loginfo("Go To (0,-5)")
                    pose.pose.position.x = 0
                    pose.pose.position.y = -5

                # Garis 2 // Line 2
                elif (a >= 400 and a < 500):
                    if (a == 400):
                        rospy.loginfo("Go To (5,-5)")
                    pose.pose.position.x = 5
                    pose.pose.position.y = -5

                # Garis 3 // Line 3
                elif (a >= 500 and a < 600):
                    if (a == 500):
                        rospy.loginfo("Go To (5,0)")
                    pose.pose.position.x = 5
                    pose.pose.position.y = 0

                # Garis 4 // Line 4
                elif (a >= 600 and a < 700):
                    if (a == 600):
                        rospy.loginfo("Go To (0,0)")
                    pose.pose.position.x = 0
                    pose.pose.position.y = 0

                # Landing
                elif (a >= 700 and a < 800):
                    if (a == 700):
                        rospy.loginfo("Landing...")
                    if (a == 799):
                        rospy.loginfo("DONE!")
                        detect = -1
                        a = 0
                        cam = cv.VideoCapture(0)
                    pose.pose.position.x = 0
                    pose.pose.position.y = 0
                    pose.pose.position.z = 0

                a = a + 1

                local_pos_pub.publish(pose)

                rate.sleep()


