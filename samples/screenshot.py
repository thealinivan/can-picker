import picamera
from time import sleep

with picamera.PiCamera() as cam:
    cam.resolution = (1024, 768)

    print('feed: starting cam...')
    sleep(1)

    cam.start_preview()

    print('feed: cam started')
    sleep(1)
    print('feed: taking screenshot...')
    sleep(1)

    cam.capture('test.jpg')

    print('feed: screenshot taken')
    print('feed: closing cam...')
    sleep(1)

    cam.stop_preview()

    print('feed: cam closed')
 