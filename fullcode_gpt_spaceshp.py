from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec3, Point3, LVector3
from direct.task import Task
import random

class SpaceShooter(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable default camera control
        self.disableMouse()

        # Set up the game world
        self.setup_world()

        # Variables to store bullets and enemies
        self.bullets = []
        self.enemies = []

        # Schedule enemy spawning
        self.taskMgr.doMethodLater(2, self.spawn_enemy, "spawn_enemy_task")

        # Add game logic update task
        self.taskMgr.add(self.update, "update_task")

    def setup_world(self):
        # Set camera position
        self.camera.setPos(0, -30, 10)
        self.camera.lookAt(0, 0, 0)

        # Create the player's spaceship
        self.setup_player()

    def setup_player(self):
        # Load a spaceship model for the player (replace with your model's path)
        self.player = self.loader.loadModel("bsg_1978_-_fury-class_fanon.glb")  # Replace with your model path
        self.player.setScale(0.08, 0.08, 0.08)
        self.player.setPos(0, 0, 0)
        self.player.reparentTo(self.render)

        # Variables to track player movement
        self.player_speed = 15
        self.player_velocity = Vec3(0, 0, 0)

        # Player input for movement
        self.accept("arrow_left", self.set_player_velocity, [-1])
        self.accept("arrow_right", self.set_player_velocity, [1])
        self.accept("arrow_up", self.set_player_velocity, [0, 1])
        self.accept("arrow_down", self.set_player_velocity, [0, -1])

        self.accept("arrow_left-up", self.set_player_velocity, [0])
        self.accept("arrow_right-up", self.set_player_velocity, [0])
        self.accept("arrow_up-up", self.set_player_velocity, [0, 0])
        self.accept("arrow_down-up", self.set_player_velocity, [0, 0])

        # Player shooting with spacebar
        self.accept("space", self.shoot)

    def set_player_velocity(self, direction, axis=0):
        # Set player velocity based on input (horizontal or vertical)
        if axis == 0:
            self.player_velocity.setX(direction * self.player_speed)
        elif axis == 1:
            self.player_velocity.setZ(direction * self.player_speed)

    def shoot(self):
        # Load a projectile model (replace with your model's path)
        bullet = self.loader.loadModel("minecraft_arrow.glb")  # Replace with a projectile model path
        bullet.setScale(0.2, 0.2, 0.2)
        bullet.setPos(self.player.getPos())
        bullet.reparentTo(self.render)
        self.bullets.append(bullet)

    def spawn_enemy(self, task):
        # Load enemy model (replace with your model's path)
        enemy = self.loader.loadModel("bsg_1978_-_fury-class_fanon.glb")  # Replace with your enemy model path
        enemy.setScale(0.01, 0.01, 0.01)
        enemy.setPos(random.uniform(-10, 10), random.uniform(50, 100), random.uniform(-10, 10))
        enemy.reparentTo(self.render)
        self.enemies.append(enemy)

        # Respawn enemies periodically
        return task.again

    def update(self, task):
        dt = globalClock.getDt()

        # Update player position
        new_pos = self.player.getPos() + self.player_velocity * dt
        self.player.setPos(new_pos)

        # Update bullet positions
        for bullet in self.bullets:
            bullet.setY(bullet.getY() + dt * 20)  # Move bullets forward
            if bullet.getY() > 100:  # Remove bullets out of bounds
                bullet.removeNode()
                self.bullets.remove(bullet)

        # Update enemy positions
        for enemy in self.enemies:
            enemy.setY(enemy.getY() - dt * 10)  # Move enemies towards player
            if enemy.getY() < -50:  # Remove enemies out of bounds
                enemy.removeNode()
                self.enemies.remove(enemy)

        # Check for collisions between bullets and enemies
        self.check_collisions()

        return Task.cont

    def check_collisions(self):
        # Simple collision detection between bullets and enemies
        for bullet in self.bullets:
            for enemy in self.enemies:
                if self.is_collision(bullet, enemy):
                    # Bullet hits enemy
                    bullet.removeNode()
                    enemy.removeNode()
                    self.bullets.remove(bullet)
                    self.enemies.remove(enemy)
                    break

    def is_collision(self, obj1, obj2):
        # Simple bounding box collision detection
        distance = (obj1.getPos() - obj2.getPos()).length()
        return distance < 1.5  # Adjust collision radius as needed

# Run the game
game = SpaceShooter()
game.run()
