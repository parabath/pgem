from panda3d.core import loadPrcFileData
from direct.actor.Actor import Actor

confVars = """
win-size 1280 720
window-title My Game
show-frame-rate-meter True
"""
loadPrcFileData("", confVars)
from direct.showbase.ShowBase import ShowBase

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()  # Initialize ShowBase first
        self.arm = Actor("my-models/arm", {"anim-1": "my-models/arm-anim1", "anim-2": "my-models/arm-anim2"})
        self.arm.setPos(0, 40, 0)
        self.arm.reparentTo(self.render)
        self.arm.loop("anim-1")
        self.x = 0
        self.speed = 2
        self.angle = 0

        self.taskMgr.add(self.update, "update")

    def update(self, task):
        dt = globalClock.getDt()
        self.angle = 1  # Correct assignment
        self.x += self.speed * dt

        return task.cont

game = MyGame()
game.run()
