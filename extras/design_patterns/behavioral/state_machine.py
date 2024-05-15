# This is an interface
class State:
    def run(self):
        assert 0, "run not implemented"

    def next(self, input):
        assert 0, "next not implemented"


class StateMachine:
    def __init__(self, initialState):
        self.currentState = initialState
        self.currentState.run()

    # Template method:
    def runAll(self, inputs):
        for i in inputs:
            print(i)
            self.currentState = self.currentState.next(i)
            self.currentState.run()


class MouseAction:
    def __init__(self, action):
        self.action = action

    def __str__(self):
        return self.action

    def __cmp__(self, other):
        return cmp(self.action, other.action)

    # Necessary when __cmp__ or __eq__ is defined
    # in order to make this class usable as a
    # dictionary key:
    def __hash__(self):
        return hash(self.action)


# Static fields; an enumeration of instances:
MouseAction.appears = MouseAction("mouse appears")
MouseAction.runsAway = MouseAction("mouse runs away")
MouseAction.enters = MouseAction("mouse enters trap")
MouseAction.escapes = MouseAction("mouse escapes")
MouseAction.trapped = MouseAction("mouse trapped")
MouseAction.removed = MouseAction("mouse removed")


class StateT(State):
    def __init__(self):
        self.transitions = None

    def next(self, input):
        if self.transitions.has_key(input):
            return self.transitions[input]
        else:
            raise "Input not supported for current state"


class Waiting(StateT):
    def run(self):
        print("Waiting: Broadcasting cheese smell")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {MouseAction.appears: MouseTrap.luring}
        return StateT.next(self, input)


class Luring(StateT):
    def run(self):
        print("Luring: Presenting Cheese, door open")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                MouseAction.enters: MouseTrap.trapping,
                MouseAction.runsAway: MouseTrap.waiting,
            }
        return StateT.next(self, input)


class Trapping(StateT):
    def run(self):
        print("Trapping: Closing door")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                MouseAction.escapes: MouseTrap.waiting,
                MouseAction.trapped: MouseTrap.holding,
            }
        return StateT.next(self, input)


class Holding(StateT):
    def run(self):
        print("Holding: Mouse caught")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {MouseAction.removed: MouseTrap.waiting}
        return StateT.next(self, input)


class MouseTrap(StateMachine):
    def __init__(self):
        # Initial state
        StateMachine.__init__(self, MouseTrap.waiting)


# Static variable initialization:
MouseTrap.waiting = Waiting()
MouseTrap.luring = Luring()
MouseTrap.trapping = Trapping()
MouseTrap.holding = Holding()

mouseMoves = [
    MouseAction("mouse appears"),
    MouseAction("mouse runs away"),
    MouseAction("mouse appears"),
]

MouseTrap().runAll(mouseMoves)
