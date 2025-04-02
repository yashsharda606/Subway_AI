import mss
import mss.tools
import subprocess
import numpy as np
import cv2
import pyautogui
pyautogui.FAILSAFE = False
from skimage.metrics import structural_similarity as ssim
import time
import keyboard
import os
import sys
import tensorflow as tf
from PIL import Image
import random
from pynput.keyboard import Controller, Key


PATH_TO_GAME = "C:\\Users\\Aayush\\Desktop\\Subway Surfers.lnk"
# subprocess.run(PATH_TO_GAME, shell=True, timeout=60)
# PATH_TO_GAME = 'C:\\Program Files\\WindowsApps\\' \
#                '16925JeuxjeuxjeuxGames.SubwaySurfersOriginalFree_1.0.0.0_x64__66k318ytnjhfe\\app\\app.exe'

GAME = {"top": 150, "left": 570, "width": 750, "height": 750}
PAUSE = {"top": 10, "left": 15, "width": 60, "height": 60}
PATH_TO_IMAGES = 'images\\training\\'

frame_width = 750
frame_height = 750
frame_rate = 12.0
# VIDEO_PATH = "C:\\Users\\nikla\\PycharmProjects\\subwAI\\recordings\\"
VIDEO_PATH = "recordings"
fourcc = cv2.VideoWriter_fourcc(*'XVID')
keyboard_controller = Controller()

class Game:
    def __init__(self):
        print("Starting the Game Subway Surfers!")
        # subprocess.run(PATH_TO_GAME)
        subprocess.Popen(PATH_TO_GAME, shell=True) 

        self.game_active = False
        self.all_zeros = False
        self.game_counter = 0
        self.key_pressed_counter = 0

        self.out_name = None  # VIDEO_PATH+time.strftime("%Y%m%d-%H%M%S")+'.avi'
        self.out = None  # cv2.VideoWriter(self.out_name, fourcc, frame_rate, (frame_width, frame_height))
        self.last_time = time.time()
        self.game_start = time.time()
        self.intro = False

        self.left = False
        self.right = False
        self.up = False
        self.down = False

        self.last_saved = None
        self.last_key = None

        self.actions = ['left', 'right', 'up', 'down', 'noop']

        self.model = None
        self.NN = None

        self.im_counter = dict()
        self.im_counter['left'] = len([name for name in os.listdir(os.path.join(PATH_TO_IMAGES, 'left'))
                                       if os.path.isfile(os.path.join(PATH_TO_IMAGES, 'left', name))])
        self.im_counter['right'] = len([name for name in os.listdir(os.path.join(PATH_TO_IMAGES, 'right'))
                                        if os.path.isfile(os.path.join(PATH_TO_IMAGES, 'right', name))])
        self.im_counter['up'] = len([name for name in os.listdir(os.path.join(PATH_TO_IMAGES, 'up'))
                                    if os.path.isfile(os.path.join(PATH_TO_IMAGES, 'up', name))])
        self.im_counter['down'] = len([name for name in os.listdir(os.path.join(PATH_TO_IMAGES, 'down'))
                                       if os.path.isfile(os.path.join(PATH_TO_IMAGES, 'down', name))])
        self.im_counter['noop'] = len([name for name in os.listdir(os.path.join(PATH_TO_IMAGES, 'noop'))
                                       if os.path.isfile(os.path.join(PATH_TO_IMAGES, 'noop', name))])
        for field in self.im_counter:
            print(self.im_counter[field])
        self.frame_history = []
        time.sleep(5)

    def disable_wifi(self):
        """
        Disable Wifi before playing to avoid ads.
        """
        if input("Please disable WIFI and enter 'y': ") == 'y':
            print("WIFI disabled")
        else:
            print("WIFI not disabled?")
            self.disable_wifi()

    def start_game(self):
        """
        For making the mouse-clicks necessary to start the game.
        """
        # self.disable_wifi()
        self.game_active = True
        pyautogui.moveTo(1, 1)
        pyautogui.click(x=890, y=640)
        self.game_counter += 1
        print(f"starting game {self.game_counter}!")

        time.sleep(4)
        pyautogui.click(1134, 943)
        time.sleep(2)
        pyautogui.click(970, 640)

        # self.out_name = VIDEO_PATH+time.strftime("%Y%m%d-%H%M%S")+'.avi'
        # self.out = cv2.VideoWriter(self.out_name, fourcc, frame_rate, (frame_width, frame_height))
        # Initialize video recording
        self.out_name = os.path.join(VIDEO_PATH, f"rec{time.strftime('%Y%m%d-%H%M%S')}.avi")
        self.out = cv2.VideoWriter(self.out_name, fourcc, frame_rate, (frame_width, frame_height))
        if not self.out.isOpened():
            print("Error: VideoWriter did not open correctly!")
            sys.exit(1)  # Stop execution if recording cannot start    
        
        print(f"🎥 Recording started: {self.out_name}")
        # Debugging: Check if the file exists right after initializing
        time.sleep(1)
        if not os.path.exists(self.out_name):
            print(f"Error: File {self.out_name} was NOT created!")
        else:
            print(f"Video file {self.out_name} was successfully created.")
        
        self.game_start = time.time()
        self.intro = True

    # def check_game_state(self):
    #     """
    #     Called when game is over (when pause-button is not visible anymore). Makes necessary mouse-clicks
    #     to start next run.
    #     """
    #     images = ['images/buttons/save_me4.png', 'images/buttons/play_button4.png', 'images/buttons/prizes.png']
    #     while not self.game_active:
    #         click_location = None
    #         while not click_location:
    #             if keyboard.is_pressed('esc') or keyboard.is_pressed('q'):
    #                 sys.exit('Terminating Program')
    #             for i in range(len(images)):
    #                 try:
    #                     click_location = pyautogui.center(pyautogui.locateOnScreen(images[i]))
    #                     click_location_x, click_location_y = click_location
    #                     if i == 0:
    #                         c = 250
    #                         b = 0
    #                     elif i == 2:
    #                         b = 300
    #                         c = 0
    #                     else:
    #                         b = 0
    #                         c = 0
    #                     pyautogui.click(click_location_x-b, click_location_y-c)
    #                     if i == 1:
    #                         print("starting")
    #                         self.game_active = True
    #                         self.game_counter += 1
    #                         print(f"starting game {self.game_counter}!")
    #                         self.out_name = VIDEO_PATH+time.strftime("%Y%m%d-%H%M%S")+'.avi'
    #                         self.out = cv2.VideoWriter(self.out_name, fourcc, frame_rate, (frame_width, frame_height))
    #                         self.game_start = time.time()
    #                         self.intro = True
    #                         break
    #                         # time.sleep(2)
    #                 except:
    #                     click_location = None

    def check_game_state(self):
        """
        Handles game over state. Restarts the game and closes the video file properly.
        """
        images = ['images/buttons/save_me4.png', 'images/buttons/play_button4.png', 'images/buttons/prizes.png']

        while not self.game_active:
            click_location = None

            while not click_location:
                if keyboard.is_pressed('esc') or keyboard.is_pressed('q'):
                    print("🛑 Terminating Program...")
                    if self.out:
                        self.out.release()  # Ensure the video is properly closed
                        print(f"✅ Video saved: {self.out_name}")
                    sys.exit('Terminating Program')

                for i in range(len(images)):
                    try:
                        click_location = pyautogui.center(pyautogui.locateOnScreen(images[i]))
                        click_location_x, click_location_y = click_location

                        # Adjust click positions
                        if i == 0:
                            c, b = 250, 0
                        elif i == 2:
                            c, b = 0, 300
                        else:
                            c, b = 0, 0

                        pyautogui.click(click_location_x - b, click_location_y - c)

                        if i == 1:
                            print("🎮 Restarting game...")
                            self.game_active = True
                            self.game_counter += 1
                            print(f"🎮 Game {self.game_counter} started!")

                            # Ensure the old video file is properly closed
                            if self.out:
                                self.out.release()
                                print(f"✅ Video saved successfully: {self.out_name}")

                            # Start new video recording
                            self.out_name = os.path.join(VIDEO_PATH, f"rec_{time.strftime('%Y%m%d-%H%M%S')}.avi")
                            self.out = cv2.VideoWriter(self.out_name, fourcc, frame_rate, (frame_width, frame_height))

                            if not self.out.isOpened():
                                print("⚠️ Error: VideoWriter failed to open! Exiting...")
                                sys.exit(1)

                            self.game_start = time.time()
                            self.intro = True
                            break

                    except:
                        click_location = None

    def get_next_state(self, key, last_frame):
        """
        Grabs next frame, saves it if in gathering-mode
        and checks if pause-button is still visible (if not, game is over).
        """
        if keyboard.is_pressed('esc') or keyboard.is_pressed('q'):
            print("Terminating...")
            self.out.release()
            # os.remove(self.out_name)
            time.sleep(2)
            sys.exit("Terminating Program")
        path = 'C:\\Users\\Aayush\\Downloads\\ML_Sem6\\subwAI-main\\images\\training\\'

        with mss.mss() as sct:

            img_game = sct.grab(GAME)
            img_pause = sct.grab(PAUSE)

            if self.model is None:
                if not self.frame_history:
                    self.frame_history = [img_game, img_game, img_game, img_game]
                else:
                    self.frame_history = self.frame_history[1:3]
                    self.frame_history.append(img_game)

                if key is not None and last_frame is not None:
                    rand = 1
                    if key == 'noop':
                        rand = random.random()

                    if rand >= 0.99:  # 0.99
                        for field in self.im_counter:
                            if field == key:
                                self.im_counter[field] += 1
                                nr = self.im_counter[field]
                                if key != 'noop':
                                    self.last_saved = os.path.join(path, key, str(nr)+'.png')
                                    self.last_key = key
                                break

                        mss.tools.to_png(self.frame_history[0].rgb, self.frame_history[0].size,
                                         output=os.path.join(path, key, str(nr)+'.png'))
                        print(f"image saved in {key} folder")

        ret, thresh1 = cv2.threshold(cv2.cvtColor(np.array(img_pause),
                                                  cv2.COLOR_BGRA2GRAY), 127, 255, cv2.THRESH_BINARY)

        self.all_zeros = not thresh1.any()
        if not self.intro:
            if self.all_zeros:
                self.game_active = False
                if self.last_saved is not None:
                    os.remove(self.last_saved)
                    print(f'{self.last_key} deleted')
                    self.im_counter[self.last_key] -= 1
                print("stopping game!")

        # return img_game[0] in case of perceptron maybe as it performs much faster and therefore is too quick
        return img_game

    def screen_cap(self, frame, action):
        """
        Screen recorder with frames that AI is seeing with action and FPS imprinted to individual video-frames.
        Necessary, when external screen recording drastically reduces FPS.
        """
        # monitor = cv2.cvtColor(img_game, cv2.COLOR_RGB2BGR)
        # frame = cv2.cvtColor(monitor, cv2.COLOR_BGR2RGB)

        # if not self.intro:
        #     if self.all_zeros:
        #         self.out.release()
        #         last_time = time.time()
        #         print("To keep recording enter 'y', else 'n'")
        #         while True:
        #             if sys.argv[-1] == 'auto':
        #                 print(self.last_time-self.game_start)
        #                 if self.last_time-self.game_start > 60:
        #                     print("Recording saved")
        #                     break
        #                 else:
        #                     os.remove(self.out_name)
        #                     print("Recording not saved")
        #                     break
        #             else:
        #                 if keyboard.is_pressed('y'):
        #                     print("Recording saved")
        #                     break
        #                 elif keyboard.is_pressed('n'):
        #                     os.remove(self.out_name)
        #                     print("Recording not saved")
        #                     break
        #                 if (time.time() - last_time) > 5:
        #                     print("Recording saved")
        #                     break
        #         return

        # cv2.putText(frame, "FPS: %f" % (1.0 / (time.time() - self.last_time)),
        #             (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
        # color = (0, 255, 0) if action != 'noop' else (255, 0, 0)
        # cv2.putText(frame, action, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        # self.out.write(frame)
        # return
        if not self.out or not self.out.isOpened():
            print("⚠ Warning: VideoWriter is not initialized or failed to open!")
            return  

        if frame is None:
            print("⚠ Warning: Frame is None! Skipping frame.")
            return

        # Ensure frame is converted to NumPy array
        if not isinstance(frame, np.ndarray):
            frame = np.array(frame)  # Convert PIL Image to NumPy array if needed

        # Convert frame to correct color format for OpenCV
        if frame.shape[-1] == 4:  # Some images have an alpha channel (RGBA)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)
        else:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Add FPS and action text overlay
        fps_text = f"FPS: {1.0 / max(0.001, (time.time() - self.last_time)):.2f}"
        cv2.putText(frame, fps_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

        color = (0, 255, 0) if action != 'noop' else (255, 0, 0)
        cv2.putText(frame, action, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)

        # Debug: Print frame details before writing
        print(f"🎥 Writing frame - Shape: {frame.shape}, Action: {action}")

        self.out.write(frame)

    def timer(self):
        """
        Updating time.
        """
        self.last_time = time.time()

    def get_prediction(self, frame):
        """
        Converting the frame to be passed into the CNN for calling a prediction, which action to take next.
        """
        img = Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX")
        img = np.array(img)
        img = img[:, :, ::-1].copy()
        cap = img
        img = cv2.resize(img, (96, 96), interpolation=cv2.INTER_AREA)
        # cap = img
        img = tf.keras.preprocessing.image.img_to_array(img)[:, :, :3]  # convert image to array

        if self.NN:
            img = tf.expand_dims(img, 0)  # create a batch
        else:
            img = np.array(img)
            img = img.flatten().reshape(1, -1)

        predictions = self.model.predict(img)

        return predictions, cap

    def take_action(self, action):
        """
        For executing the predicted action.
        """
        # print(f"Taking action: {action}")
        # # print(action)
        # if action == 'noop':
        #     return
        # keyboard.press(action)
        # time.sleep(0.01)
        # keyboard.release(action)
        key_mappings = {
            'left': 'A',      # AHK script uses 'A' for left
            'right': 'D',     # AHK script uses 'D' for right
            'up': 'W',        # AHK script uses 'W' for up
            'down': 'S',      # AHK script uses 'S' for down
        }

        if action == 'noop':
            return  # No action needed

        if action not in key_mappings:
            print(f"⚠️ Unknown action: {action}")
            return

        key_to_press = key_mappings[action]
    
        print(f"🚀 Pressing key: {action}")

        try:
            pyautogui.keyDown(key_to_press)  # Press the key
            time.sleep(0.1)  # Hold it briefly
            pyautogui.keyUp(key_to_press)  # Release the key
            print(f"✅ pyautogui successfully pressed key: {action}")
        except Exception as e:
            print(f"⚠️ pyautogui failed for key {action}: {e}")

    def listen(self):
        """
        Detects key presses and maps them to the correct actions.
        """
        key = 'noop'
        key_pressed = False

        if keyboard.is_pressed('left') or keyboard.is_pressed('a'):  # Detect A for Left
            print("LEFT Key Pressed!")
            key_pressed = True
            self.left, self.right, self.up, self.down = True, False, False, False
            key = 'left'

        elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):  # Detect D for Right
            print("RIGHT Key Pressed!")
            key_pressed = True
            self.left, self.right, self.up, self.down = False, True, False, False
            key = 'right'

        elif keyboard.is_pressed('up') or keyboard.is_pressed('w'):  # Detect W for Up
            print("UP Key Pressed!")
            key_pressed = True
            self.left, self.right, self.up, self.down = False, False, True, False
            key = 'up'

        elif keyboard.is_pressed('down') or keyboard.is_pressed('s'):  # Detect S for Down
            print("DOWN Key Pressed!")
            key_pressed = True
            self.left, self.right, self.up, self.down = False, False, False, True
            key = 'down'

        if not key_pressed and self.key_pressed_counter > 2:
            self.left = self.right = self.up = self.down = False
        else:
            self.key_pressed_counter += 1

        return key

    def mse(self, image_a, image_b):
        """
        For comparing images for similarity.
        """
        err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
        err /= float(image_a.shape[0] * image_a.shape[1])
        return err

    def compare_images(self, image_a, image_b):
        """
        For comparing images for similarity.
        """
        m = self.mse(image_a, image_b)
        s = ssim(image_a, image_b)
        return m, s

#     def play(self):
#         self.start_game()
#         last_frame = None  # Initialize last_frame before the loop
#         while True:
#             key = self.listen()
#             frame = self.get_next_state(key, last_frame)  # Pass last_frame as the second argument
#             last_frame = frame  # Update last_frame for the next iteration

#             frame = np.array(Image.frombytes("RGB", frame.size, frame.bgra, "raw", "BGRX"))
#             frame = cv2.resize(frame, (750, 750))
#             self.screen_cap(frame, key)
#             self.timer()
#             if not self.game_active:
#                 self.start_game()

# if __name__ == "__main__":
#     game = Game()
#     game.play()
