from panda3d.core import Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task

class Platformer(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Variables for player movement and gravity
        self.player_speed = 5
        self.jump_speed = 10
        self.gravity = -0.5
        self.is_jumping = False
        self.player_velocity = Vec3(0, 0, 0)

        # Disable the default camera control
        self.disableMouse()

        # Set up the world
        self.setup_world()

        # Accept player input
        self.accept("arrow_left", self.set_movement, [-1])
        self.accept("arrow_right", self.set_movement, [1])
        self.accept("arrow_left-up", self.set_movement, [0])
        self.accept("arrow_right-up", self.set_movement, [0])
        self.accept("space", self.jump)

        # Add task to update the game every frame
        self.taskMgr.add(self.update, "update_task")

    def setup_world(self):
        # Set camera position
        self.camera.setPos(0, -30, 10)
        self.camera.lookAt(0, 0, 0)

        # Create a player character (a simple cube)
        self.player = self.loader.loadModel("models/box")
        self.player.setScale(0.5, 0.5, 0.5)
        self.player.setPos(0, 0, 2)
        self.player.reparentTo(self.render)

        # Create a ground platform
        self.ground = self.loader.loadModel("models/box")
        self.ground.setScale(10, 1, 1)
        self.ground.setPos(0, 0, 0)
        self.ground.reparentTo(self.render)

        # Create floating platforms
        self.platform1 = self.loader.loadModel("models/box")
        self.platform1.setScale(3, 1, 0.5)
        self.platform1.setPos(4, 0, 3)
        self.platform1.reparentTo(self.render)

        self.platform2 = self.loader.loadModel("models/box")
        self.platform2.setScale(2, 1, 0.5)
        self.platform2.setPos(-4, 0, 6)
        self.platform2.reparentTo(self.render)

    def set_movement(self, direction):
        self.player_velocity.setX(direction * self.player_speed)

    def jump(self):
        if not self.is_jumping:
            self.player_velocity.setZ(self.jump_speed)
            self.is_jumping = True

    def update(self, task):
        dt = globalClock.getDt()

        # Apply gravity
        if self.is_jumping:
            self.player_velocity.setZ(self.player_velocity.getZ() + self.gravity)

        # Update player position
        new_pos = self.player.getPos() + self.player_velocity * dt
        self.player.setPos(new_pos)

        # Move the camera to follow the player
        self.camera.setPos(new_pos.getX(), new_pos.getY() - 20, new_pos.getZ() + 5)

        # Check for collisions
        self.check_collisions()

        return Task.cont

    def check_collisions(self):
        player_pos = self.player.getPos()

        # Ground collision
        if player_pos.getZ() <= 0.5:
            self.player_velocity.setZ(0)
            self.is_jumping = False
            self.player.setZ(0.5)

        # Platform 1 collision
        if player_pos.getX() > 2 and player_pos.getX() < 6 and player_pos.getZ() < 3.5 and player_pos.getZ() > 2.5:
            self.player_velocity.setZ(0)
            self.is_jumping = False
            self.player.setZ(3)

        # Platform 2 collision
        if player_pos.getX() < -2 and player_pos.getX() > -6 and player_pos.getZ() < 6.5 and player_pos.getZ() > 5.5:
            self.player_velocity.setZ(0)
            self.is_jumping = False
            self.player.setZ(6)

# Run the game
game = Platformer()
game.run()
