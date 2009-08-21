from characterControl.Camera import Camera
import direct.directbase.DirectStart
from characterControl import Player
from worldControl import World

if __name__ == '__main__':
    c = Camera()
    p = Player(c)
    run()
