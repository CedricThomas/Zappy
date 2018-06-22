# coding = utf-8
from src.classes.ia_res.Ant import ant
from src.classes.states.SeekTeamState import SeekTeamState
from src.classes.states.StateMachine import AAIState, statemachine
from src.classes.states.WaitTeamState import WaitTeamState


class QueenState(AAIState):

    def __init__(self):
        super().__init__("QueenState")

    def on_push(self, cli):
        super().on_push(cli)
        statemachine.closure = lambda: statemachine.push(SeekTeamState())

    def popped_over(self):
        super().popped_over()
        if not ant.queen:
            statemachine.closure = lambda: statemachine.replace(WaitTeamState())
