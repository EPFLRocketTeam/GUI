from PCANBasic import *
# The Plug & Play Channel (PCAN-USB) is initialized
#
objPCAN = PCANBasic()
result = objPCAN.Initialize(PCAN_USBBUS1, PCAN_BAUD_250K)
if result != PCAN_ERROR_OK:
    # An error occurred, get a text describing the error and show it
    #
    result = objPCAN.GetErrorText(result)
    print(result[1])
else:
    print("PCAN-USB (Ch-1) was initialized")


readResult = PCAN_ERROR_OK,
while (readResult[0] & PCAN_ERROR_QRCVEMPTY) != PCAN_ERROR_QRCVEMPTY:
    # Check the receive queue for new messages
    
    readResult = objPCAN.Read(PCAN_USBBUS1)
    if readResult[0] != PCAN_ERROR_QRCVEMPTY:
        # Process the received message
        
        print("A message was received")
        print("Method code", readResult[0])
        print("ID", readResult[1].getID())
        print("MSGTYPE", readResult[1].MSGTYPE)
        print("LEN", readResult[1].LEN)
        print("DATA", readResult[1].DATA)
        print("")
        #ProcessMessage(result[1],result[2]) # Possible processing function, ProcessMessage(msg,timestamp)
    else:
        # An error occurred, get a text describing the error and show it
	    result = objPCAN.GetErrorText(readResult[0])
	    print(result[1], "\n")


# The USB Channel is released

result = objPCAN.Uninitialize(PCAN_USBBUS1)
if result != PCAN_ERROR_OK:
    # An error occurred, get a text describing the error and show it
    
    result = objPCAN.GetErrorText(result)
    print(result[1])
else:
    print("PCAN-USB (Ch-1) was released")
