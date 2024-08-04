#IMPORTING LIBRARIES
import numpy as np
from keras.models import load_model
import cv2
import ctypes, time

# Creating Sendinput method
SendInput = ctypes.windll.user32.SendInput
# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

#Funtions to press and release a key takes hexcode as argument
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

#HashTables for Predicted Class
lookup = {'Fist': 0, 'Nothing': 1, 'Palm': 2, 'Swing': 3, 'Thumb': 4, 'Yo': 5}
reverselookup = {0: 'Fist', 1: 'Nothing', 2: 'Palm', 3: 'Swing', 4: 'Thumb', 5: 'Yo'}

keymap = {
    0:0x20,#Press D
    2:0x11,#Press W
    3:0x1E,#Press A
    4:0x1F,#Press S
    5:0x2A,#Press Shift
}
class Game:
    def presskey(self,key):
        PressKey(keymap.get(key,0x11)) # press D
        time.sleep(.05)
        ReleaseKey(keymap.get(key,0x11)) #release D

    def model_func(self,reverselookup,model):
        #Capture Video From Camera
        cap  = cv2.VideoCapture(0)

        _, first_frame = cap.read()
        #Selecting RangeOfInterest in rectangle form
        cv2.rectangle(first_frame,(0,100),(300,400),(0,255,0))
        roi = first_frame[100:400,0:300]
        first_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        first_roi = cv2.GaussianBlur(first_roi, (5, 5), 0)
        
        while True:
            _,frame = cap.read()
            #To flip the image if needed
            #frame = cv2.flip(frame,1)
            
            cv2.rectangle(frame,(0,100),(300,400),(0,255,0))
            roi = frame[100:400,0:300]
            
            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.GaussianBlur(gray_roi, (5, 5), 0)
            
            difference = cv2.absdiff(first_roi, gray_roi)
            _, difference = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)
            
            difference_resized = cv2.resize(difference,(400,400))
            difference_reshaped = difference_resized.reshape(1,400,400,1)/255.0
            cv2.putText(frame, reverselookup[np.argmax(model.predict(difference_reshaped))], (0,100), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)

            #Pressing Keystroke
            self.presskey(np.argmax(model.predict(difference_reshaped)))
            #cv2.imshow("first_frame",first_frame)
            cv2.imshow("frame",frame)
            cv2.imshow("difference",difference)
            
            if cv2.waitKey(1) & 0xFF == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
        

#Executing Main Function
if __name__ == "__main__":
    #Loads Model
    model = load_model("model.h5")
    #Executing Functions
    game = Game()
    game.model_func(reverselookup,model)
