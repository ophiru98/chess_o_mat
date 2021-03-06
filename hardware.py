import os
import cv2
#import RPi.GPIO as gpioFUCKCKCSKAKC
import gpio
import picamera
import time
from scipy import misc
import gui_img_manager
import sender
import listener

"""
This file is for user communication and hardware.
"""



ul = 21
ur = 5
dr = 13
dl = 4
btn = 17
VibTime = 0.5
save_and_print=True
IS_PI = True
ENABLE_VIBRATIONS = True # disable vibrations
RESIZE_SIZE = 1000

class hardware:

    def __init__(self, angle_num, imgs_if_tester = None):
        if imgs_if_tester is not None: 
            self.is_test = True
            self.angles_imgs_lst = []
            self.angles_imgs_counter = []
            for i in range(angle_num):
                img_names = os.listdir(imgs_if_tester[i])
                sorted_img_names = sorted(img_names, key= first_2_chars)
                img_array = []
                for j in range(len(sorted_img_names)):
                    img_array.append(cv2.cvtColor(cv2.imread(imgs_if_tester[i] +
                                              sorted_img_names[j]),cv2.COLOR_RGB2BGR))
                print(sorted_img_names)
                self.angles_imgs_lst.append(img_array)
                self.angles_imgs_counter.append(-1)
        else:
            self.is_test = False

        if (IS_PI):
            self.socket = sender.sender()
        else:
            self.socket = listener.listener()

    def init_vib(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(ur, gpio.OUT)
        gpio.setup(ul, gpio.OUT)
        gpio.setup(dr, gpio.OUT)
        gpio.setup(dl, gpio.OUT)

    def get_image(self, angle_idx):
        if self.is_test:
            self.angles_imgs_counter[angle_idx] += 1
            img = self.angles_imgs_lst[angle_idx][self.angles_imgs_counter[angle_idx]]
    #        img = cv2.resize(img,(RESIZE_SIZE,RESIZE_SIZE))
            if(IS_PI):
                self.socket.send_image(img)  # asynchronus send, w/ timeout
            gui_img_manager.add_img(img)
            return img
        else:
            if(IS_PI):
                gpio.setmode(gpio.BOARD)
                gpio.setup(btn, gpio.IN, pull_up_down=gpio.PUD_DOWN)
                should_enter = True
                try:
                    print("plz press me honz")
                    while True:
                        if (gpio.input(btn) == 1):
                            should_enter = True

                        elif (should_enter):
                            img = self.one_still()
                            
                            #img = cv2.resize(img,(RESIZE_SIZE,RESIZE_SIZE))
                            self.socket.send_image(img)
                            should_enter = False
                            gpio.cleanup()
                            return img

                except KeyboardInterrupt:
                    print ('cam err!')

            else: # gui
                img =self.socket.get_image()
                gui_img_manager.add_img(img)
                return img

    def one_still(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (1024, 768)
            camera.shutter_speed= camera.exposure_speed
        #    camera.iso=400
        #    camera.exposure_mode='off'
        #    #g=camera.awb_gains
            camera.awb_mode='off'
            camera.awb_gains=[1.3,1.3]
        #    camera.color_effects=(64,170)
        #    camera.brightness=55
        #    camera.contrast=20
       #     camera.drc_strength='medium'
            camera.start_preview()
            # Camera warm-up time
            time.sleep(0.1)
            camera.capture('cam.jpg')
            return(cv2.imread('cam.jpg'))



    def is_i_first(self):
        return True
    # TODO write this func


    def givevibration(self, move):
        gpio.output(move, gpio.HIGH)
        time.sleep(VibTime)
        gpio.output(move, gpio.LOW)

    def givevibrationagain(self):
        gpio.output(ul, gpio.HIGH)
        gpio.output(dl, gpio.HIGH)
        gpio.output(ur, gpio.HIGH)
        gpio.output(dr, gpio.HIGH)
        time.sleep(VibTime)
        gpio.output(ul, gpio.LOW)
        gpio.output(dl, gpio.LOW)
        gpio.output(ur, gpio.LOW)
        gpio.output(dr, gpio.LOW)

    def player_indication(self, move):
        if(not ENABLE_VIBRATIONS):
            return

        self.init_vib()

        if move=="again":
            self.givevibrationagain()
            gpio.cleanup()
            return

        for string in move:
            if (string == "a1"):
                self.givevibration(dl)
                self.givevibration(dl)
                self.givevibration(dl)
        
            elif (string == "a2"):
                self.givevibration(dl)
                self.givevibration(dl)
                self.givevibration(ul)
        
            elif (string == "a3"):
                self.givevibration(dl)
                self.givevibration(ul)
                self.givevibration(dl)
        
            elif (string == "a4"):
                self.givevibration(dl)
                self.givevibration(ul)
                self.givevibration(ul)
        
            elif (string == "a5"):
                self.givevibration(ul)
                self.givevibration(dl)
                self.givevibration(dl)
        
            elif (string == "a6"):
                self.givevibration(ul)
                self.givevibration(dl)
                self.givevibration(ul)
        
            elif (string == "a7"):
                self.givevibration(ul)
                self.givevibration(ul)
                self.givevibration(dl)
        
            elif (string == "a8"):
                self.givevibration(ul)
                self.givevibration(ul)
                self.givevibration(ul)
        
            elif (string == "b1"):
                self.givevibration(dl)
                self.givevibration(dl)
                self.givevibration(dr)
        
            elif (string == "b2"):
                self.givevibration(dl)
                self.givevibration(dl)
                self.givevibration(ur)
        
            elif (string == "b3"):
                self.givevibration(dl)
                self.givevibration(ul)
                self.givevibration(dr)
        
            elif (string == "b4"):
                self.givevibration(dl)
                self.givevibration(ul)
                self.givevibration(ur)
        
            elif (string == "b5"):
                self.givevibration(ul)
                self.givevibration(dl)
                self.givevibration(dr)
        
            elif (string == "b6"):
                self.givevibration(ul)
                self.givevibration(dl)
                self.givevibration(ur)
        
            elif (string == "b7"):
                self.givevibration(ul)
                self.givevibration(ul)
                self.givevibration(dr)
        
            elif (string == "b8"):
                self.givevibration(ul)
                self.givevibration(ul)
                self.givevibration(ur)
        
            elif (string == "c1"):
                self.givevibration(dl)
                self.givevibration(dr)
                self.givevibration(dl)
        
            elif (string == "c2"):
                self.givevibration(dl)
                self.givevibration(dr)
                self.givevibration(ul)
        
            elif (string == "c3"):
                self.givevibration(dl)
                self.givevibration(ur)
                self.givevibration(dl)
        
            elif (string == "c4"):
                self.givevibration(dl)
                self.givevibration(ur)
                self.givevibration(ul)
        
            elif (string == "c5"):
                self.givevibration(ul)
                self.givevibration(dr)
                self.givevibration(dl)
        
            elif (string == "c6"):
                self.givevibration(ul)
                self.givevibration(dr)
                self.givevibration(ul)
        
            elif (string == "c7"):
                self.givevibration(ul)
                self.givevibration(ur)
                self.givevibration(dl)
        
            elif (string == "c8"):
                self.givevibration(ul)
                self.givevibration(ur)
                self.givevibration(ul)
        
            elif (string == "d1"):
                self.givevibration(dl)
                self.givevibration(dr)
                self.givevibration(dr)
        
            elif (string == "d2"):
                self.givevibration(dl)
                self.givevibration(dr)
                self.givevibration(ur)
        
            elif (string == "d3"):
                self.givevibration(dl)
                self.givevibration(ur)
                self.givevibration(dr)
        
            elif (string == "d4"):
                self.givevibration(dl)
                self.givevibration(ur)
                self.givevibration(ur)
        
            elif (string == "d5"):
                self.givevibration(ul)
                self.givevibration(dr)
                self.givevibration(dr)
        
            elif (string == "d6"):
                self.givevibration(ul)
                self.givevibration(dr)
                self.givevibration(ur)
        
            elif (string == "d7"):
                self.givevibration(ul)
                self.givevibration(ur)
                self.givevibration(dr)
        
            elif (string == "d8"):
                self.givevibration(ul)
                self.givevibration(ur)
                self.givevibration(ur)
        
            elif (string == "e1"):
                self.givevibration(dr)
                self.givevibration(dl)
                self.givevibration(dl)
        
            elif (string == "e2"):
                self.givevibration(dr)
                self.givevibration(dl)
                self.givevibration(ul)
        
            elif (string == "e3"):
                self.givevibration(dr)
                self.givevibration(ul)
                self.givevibration(dl)
        
            elif (string == "e4"):
                self.givevibration(dr)
                self.givevibration(ul)
                self.givevibration(ul)
        
            elif (string == "e5"):
                self.givevibration(ur)
                self.givevibration(dl)
                self.givevibration(dl)
        
            elif (string == "e6"):
                self.givevibration(ur)
                self.givevibration(dl)
                self.givevibration(ul)
        
            elif (string == "e7"):
                self.givevibration(ur)
                self.givevibration(ul)
                self.givevibration(dl)
        
            elif (string == "e8"):
                self.givevibration(ur)
                self.givevibration(ul)
                self.givevibration(ul)
        
            elif (string == "f1"):
                self.givevibration(dr)
                self.givevibration(dl)
                self.givevibration(dr)
        
            elif (string == "f2"):
                self.givevibration(dr)
                self.givevibration(dl)
                self.givevibration(ur)
        
            elif (string == "f3"):
                self.givevibration(dr)
                self.givevibration(ul)
                self.givevibration(dr)
        
            elif (string == "f4"):
                self.givevibration(dr)
                self.givevibration(ul)
                self.givevibration(ur)
        
            elif (string == "f5"):
                self.givevibration(ur)
                self.givevibration(dl)
                self.givevibration(dr)
        
            elif (string == "f6"):
                self.givevibration(ur)
                self.givevibration(dl)
                self.givevibration(ur)
        
            elif (string == "f7"):
                self.givevibration(ur)
                self.givevibration(ul)
                self.givevibration(dr)
        
            elif (string == "f8"):
                self.givevibration(ur)
                self.givevibration(ul)
                self.givevibration(ur)
        
            elif (string == "g1"):
                self.givevibration(dr)
                self.givevibration(dr)
                self.givevibration(dl)
        
            elif (string == "g2"):
                self.givevibration(dr)
                self.givevibration(dr)
                self.givevibration(ul)
        
            elif (string == "g3"):
                self.givevibration(dr)
                self.givevibration(ur)
                self.givevibration(dl)
        
            elif (string == "g4"):
                self.givevibration(dr)
                self.givevibration(ur)
                self.givevibration(ul)
        
            elif (string == "g5"):
                self.givevibration(ur)
                self.givevibration(dr)
                self.givevibration(dl)
        
            elif (string == "g6"):
                self.givevibration(ur)
                self.givevibration(dr)
                self.givevibration(ul)
        
            elif (string == "g7"):
                self.givevibration(ur)
                self.givevibration(ur)
                self.givevibration(dl)
        
            elif (string == "g8"):
                self.givevibration(ur)
                self.givevibration(ur)
                self.givevibration(ul)
        
            elif (string == "h1"):
                self.givevibration(dr)
                self.givevibration(dr)
                self.givevibration(dr)
        
            elif (string == "h2"):
                self.givevibration(dr)
                self.givevibration(dr)
                self.givevibration(ur)
        
            elif (string == "h3"):
                self.givevibration(dr)
                self.givevibration(ur)
                self.givevibration(dr)
        
            elif (string == "h4"):
                self.givevibration(dr)
                self.givevibration(ur)
                self.givevibration(ur)
        
            elif (string == "h5"):
                self.givevibration(ur)
                self.givevibration(dr)
                self.givevibration(dr)
        
            elif (string == "h6"):
                self.givevibration(ur)
                self.givevibration(dr)
                self.givevibration(ur)
        
            elif (string == "h7"):
                self.givevibration(ur)
                self.givevibration(ur)
                self.givevibration(dr)
        
            elif (string == "h8"):
                self.givevibration(ur)
                self.givevibration(ur)
                self.givevibration(ur)
            if string == move[0]:
                time.sleep(1.5)

            gpio.cleanup()

def first_2_chars(x):
    return int(x[0:-4])


