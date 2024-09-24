from panda3d.core import Point3, Vec3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from panda3d.core import WindowProperties
from direct.gui.OnscreenText import OnscreenText

class PongGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the default camera control.
        self.disableMouse()

        # Set window title and size
        properties = WindowProperties()
        properties.setTitle("Pong in Panda3D")
        self.win.requestProperties(properties)
        
        # Set up the game
        self.setup_game()

    def setup_game(self):
        # Set the camera position
        self.camera.setPos(0, -20, 0)

        # Create the paddles and ball as rectangular planes
        self.paddle_1 = self.loader.loadModel("models/box")
        self.paddle_1.setScale(0.3, 0.2, 1)
        self.paddle_1.setPos(-5, 0, 0)
        self.paddle_1.reparentTo(self.render)

        self.paddle_2 = self.loader.loadModel("models/box")
        self.paddle_2.setScale(0.3, 0.2, 1)
        self.paddle_2.setPos(5, 0, 0)
        self.paddle_2.reparentTo(self.render)

        self.ball = self.loader.loadModel("models/smiley")
        self.ball.setScale(0.3, 0.3, 0.3)
        self.ball.setPos(0, 0, 0)
        self.ball.reparentTo(self.render)

        # Ball movement variables
        self.ball_velocity = Vec3(0.1, 0, 0.1)

        # Add task to update the ball position
        self.taskMgr.add(self.update_ball, "update_ball_task")

        # Paddle control variables
        self.paddle_speed = 10
        self.paddle_1_velocity = 0
        self.paddle_2_velocity = 0

        self.accept("w", self.set_paddle_velocity, [self.paddle_1, 1])
        self.accept("s", self.set_paddle_velocity, [self.paddle_1, -1])
        self.accept("arrow_up", self.set_paddle_velocity, [self.paddle_2, 1])
        self.accept("arrow_down", self.set_paddle_velocity, [self.paddle_2, -1])

        # Stop paddle movement on key release
        self.accept("w-up", self.stop_paddle, [self.paddle_1])
        self.accept("s-up", self.stop_paddle, [self.paddle_1])
        self.accept("arrow_up-up", self.stop_paddle, [self.paddle_2])
        self.accept("arrow_down-up", self.stop_paddle, [self.paddle_2])

        # Add task to update paddle positions
        self.taskMgr.add(self.update_paddles, "update_paddles_task")

        # Initialize score
        self.score_1 = 0
        self.score_2 = 0

        # Score display
        self.score_display = OnscreenText(text="Player 1: 0  Player 2: 0", pos=(0, 0.9), scale=0.07)

    def update_ball(self, task):
        dt = globalClock.getDt()

        # Move the ball
        self.ball.setPos(self.ball.getPos() + self.ball_velocity * dt)

        # Check for collision with the top and bottom walls
        if self.ball.getZ() > 5 or self.ball.getZ() < -5:
            self.ball_velocity.setZ(-self.ball_velocity.getZ())

        # Check for collision with the paddles
        if self.ball.getX() < -4.5 and abs(self.paddle_1.getZ() - self.ball.getZ()) < 1:
            self.ball_velocity.setX(-self.ball_velocity.getX())

        if self.ball.getX() > 4.5 and abs(self.paddle_2.getZ() - self.ball.getZ()) < 1:
            self.ball_velocity.setX(-self.ball_velocity.getX())

        # Reset ball if it goes off-screen and update score
        if self.ball.getX() < -6:
            self.score_2 += 1
            self.reset_ball()

        if self.ball.getX() > 6:
            self.score_1 += 1
            self.reset_ball()

        # Update the score display
        self.score_display.setText(f"Player 1: {self.score_1}  Player 2: {self.score_2}")

        return Task.cont

    def update_paddles(self, task):
        dt = globalClock.getDt()

        # Move paddle 1
        new_z1 = self.paddle_1.getZ() + self.paddle_1_velocity * dt * self.paddle_speed
        self.paddle_1.setZ(min(max(new_z1, -5), 5))

        # Move paddle 2
        new_z2 = self.paddle_2.getZ() + self.paddle_2_velocity * dt * self.paddle_speed
        self.paddle_2.setZ(min(max(new_z2, -5), 5))

        return Task.cont

    def set_paddle_velocity(self, paddle, direction):
        if paddle == self.paddle_1:
            self.paddle_1_velocity = direction
        elif paddle == self.paddle_2:
            self.paddle_2_velocity = direction

    def stop_paddle(self, paddle):
        if paddle == self.paddle_1:
            self.paddle_1_velocity = 0
        elif paddle == self.paddle_2:
            self.paddle_2_velocity = 0

    def reset_ball(self):
        self.ball.setPos(0, 0, 0)
        self.ball_velocity = Vec3(0.1 * (1 if self.ball_velocity.getX() > 0 else -1), 0, 0.1)

game = PongGame()
game.run()
