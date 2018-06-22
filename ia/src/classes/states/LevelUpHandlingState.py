# coding = utf-8
import enum
from ia.src.classes.com.Controller import requirement
from ia.src.classes.ia_res.Ant import ant
from ia.src.classes.states.StateMachine import AAIState, statemachine
from ia.src.classes.states.WaitTeamState import WaitTeamState


class Status(enum.Enum):
    StandBy = 0
    Farming = 1
    Casting = 2


class LevelUpHandlingState(AAIState):

    def __init__(self):
        super().__init__("LevelUpHandler")
        self.lvl = ant.lvl + 1

    def on_push(self, cli):
        from ia.src.classes.states.LvlAloneState import LevelUpAlone
        super().on_push(cli)
        if requirement[self.lvl][0] == 1:
            statemachine.closure = lambda: statemachine.push(LevelUpAlone())
        else:
            statemachine.closure = lambda: statemachine.push(WaitTeamState())

    def popped_over(self):
        super().popped_over()
        statemachine.closure = lambda: statemachine.pop()
