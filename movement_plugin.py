from position_plugin import PluginPosition
from Vec2d import Vec2d

GRAVITY = 9.81


class PluginMovement(PluginPosition):
    """
    For dumb movement that only does velocity
    """
    def __init__(self, pos=(0.0, 0.0), velocity=(0.0, 0.0)):
        super(PluginMovement, self).__init__(pos=pos)
        self._velocity = Vec2d(velocity[0], velocity[1])

    @property
    def vx(self):
        return self.velocity.x

    @vx.setter
    def vx(self, value):
        self.velocity.x = value

    @property
    def vy(self):
        return self.velocity.y

    @vy.setter
    def vy(self, value):
        self.velocity.y = value

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity.x = value[0]
        self._velocity.y = value[1]

    def update_time(self, dt):
        self.pos += self.velocity * dt


class PluginForceSource(object):
    def __init__(self, force=0.0, reative_force_coefficient=0.0, friction_coefficient=0.0):
        """
        self.force = constant force. Example: conveyor belt, wind
        self.reactive_force_coefficient = force multiplier.
            force *= (1 - reactive force coefficient)
            Example:
                value = 1: object force is 0
                value > 1: object force is negative (e.g. a simple spring)
                value < 1: object force is damped
        self.friction_coefficient = slowing dependent on obj mass
            Friction only exists between the floor and the object, no wall friction
            velocity -= GRAVITY * obj_friction * friction * dt
            Example: "roughness factor", mass is factored out
                friction = 0: no change in velocity
                friction < 0: object speeds up
        """
        self.force = force
        self.reactive_force_coefficient = reative_force_coefficient
        self.friction_coefficient = friction_coefficient


class PluginPhysics(PluginMovement):
    """
    More involved movement with force resolution and friction etc.
        But no equations of force!

    friction_coefficient = "roughness" of this object. Is multiplied by force_sources summed friction coefficient

    Work in progress - need to think over how to handle force sources neatly
        specifically detecting when they apply to this object
    """
    def __init__(self, pos=(0.0, 0.0), velocity=(0.0, 0.0), mass=1.0, friction_coefficient=1.0):
        super(PluginPhysics, self).__init__(pos=pos, velocity=velocity)
        self._force = Vec2d(0.0, 0.0)
        self.force_sources = set()  # set of objects, each is expected to have a .force and .reactive_force_coefficient
        self.friction_coefficient = friction_coefficient
        self.mass = mass

    @property
    def fx(self):
        return self.force.x

    @property
    def fy(self):
        return self.force.y

    @property
    def force(self):
        return self._force

    @property
    def ax(self):
        return self._force[0] / self.mass

    @property
    def ay(self):
        return self._force[1] / self.mass

    @property
    def acceleration(self):
        return self._force / self.mass

    def update_force(self):
        sourced_friction = 0.0
        sourced_force = Vec2d(0.0, 0.0)
        sourced_reactive_force = 0.0
        for f in self.force_sources:
            sourced_friction += f.friction_coefficient
            sourced_force += f.force
            sourced_reactive_force += f.reactive_force_coefficient

        force = Vec2d(0.0, 0.0)
        force -= self.mass * GRAVITY * sourced_friction * self.friction_coefficient
        force += sourced_force
        force *= (1 - sourced_reactive_force)
        self._force[0] = force[0]
        self._force[1] = force[1]

    def update_time(self, dt):
        self.update_force()
        self.velocity += (self.force / self.mass) * dt
        super(PluginPhysics, self).update_time(dt)