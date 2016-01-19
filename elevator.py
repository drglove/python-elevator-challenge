UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.callbacks = None
        self.queue = {}
        self.queue[UP] = []
        self.queue[DOWN] = []
        self.current_queue = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        # Queue up their request
        self.queue[direction].append(floor)
        if self.current_queue is None:
            if floor > self.callbacks.current_floor:
                self.current_queue = UP
            elif floor < self.callbacks.current_floor:
                self.current_queue = DOWN

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        # Figure out which direction we would need to go in
        if floor > self.callbacks.current_floor:
            direction = UP
        elif floor < self.callbacks.current_floor:
            direction = DOWN
        else:
            direction = None

        # Queue up their request
        if direction is not None and (self.callbacks.motor_direction is None or direction == self.callbacks.motor_direction):
            self.queue[direction].append(floor)
            if self.current_queue is None:
                self.current_queue = direction

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        # Stop when we see a floor in the current queue we need to stop at
        if self.callbacks.current_floor in self.queue[self.current_queue]:
            # Pop the element and stop moving
            i = self.queue[self.current_queue].index(self.callbacks.current_floor)
            del self.queue[self.current_queue][i]
            self.callbacks.motor_direction = None

        # Check if we need to update which direction we're going in
        if not self.queue[UP] and not self.queue[DOWN]:
            # Both queues exhausted
            self.current_queue = None
        elif self.queue[UP] and not self.queue[DOWN]:
            # Out of downwards movements
            self.current_queue = UP
        elif not self.queue[UP] and self.queue[DOWN]:
            # Out of upwards movements
            self.current_queue = DOWN
        # else: use the current queue

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        self.callbacks.motor_direction = self.current_queue
