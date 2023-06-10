import json
from extras.system import System
import cv2


config = json.load(open('config.json'))['config']
cameras = config['cameras']

threads = []
for camera in cameras:
    thread = System(camera)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

cv2.destroyAllWindows()
