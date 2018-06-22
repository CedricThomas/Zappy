from ia.src.classes.ia_res.Path import Path, PathManipulator, PositionTracker
from ia.src.classes.ia_res.TrackableTransactions import TakeTransaction, LookTransaction, CheckTransaction
from ia.src.classes.states.StateMachine import AAIState, statemachine
from ia.src.classes.com.Controller import Resources
from ia.src.classes.ia_res.Ant import ant
from ia.src.classes.ia_res.Vector import Vector


class SeekItemsState(AAIState):

    def findLooksItems(self, look):
        dup_items = dict(self.items_dict)
        path = Path()
        found = False
        for item in dup_items:
            for i in range(len(look)):
                if dup_items[item] != 0 and item.value in look[i]:
                    found = True
                    nb = min(look[i].count(item.value), dup_items[item])
                    if nb < 0:
                        nb = look[i].count(item.value)
                    dup_items[item] -= nb
                    event = TakeTransaction(item, nb, lambda value: None, self.take_ok, self.take_ko)
                    path.addConePoint(i, event)
        return found, path

    def goNextPlace(self):
        path = Path()
        if self.progress == self.surface:
            left_dist = ant.lvl - 1
            path.addPoint(Vector(-left_dist, 0), CheckTransaction())
            path.addPoint(Vector(-left_dist, -1), LookTransaction(lambda value: None))
            move = Vector(-left_dist, -1)
            self.progress = 0
        else:
            path.addPoint(Vector(0, 1), LookTransaction(lambda value: None))
            move = Vector(0, 1)
            self.progress += 1
        path, look = path.generateOrder(False)
        self.tracker.addMove(move, look)
        self.pathHandler = PathManipulator(path, self.updateAntLook)  # TODO estimate ?
        self.pathHandler.execute()

    def updateAntLook(self, look):
        ant.look = look
        found, path = self.findLooksItems(look)
        if found:
            self.pathHandler = PathManipulator(path.generateOpti(True)[0], self.checkEnd)  # TODO estimate ?
            self.pathHandler.execute()
        else:
            self.goNextPlace()

    def take_ko(self, value):
        print("TAKE FAILED ", value)
        del value

    def take_ok(self, value):
        print("TAKE OK ", value)
        self.items_dict[Resources(value)] -= 1

    def on_push(self, cli):
        super().on_push(cli)
        LookTransaction(self.updateAntLook).execute()

    def update(self, cli, inputs):
        super().update(cli, inputs)

    def checkEnd(self, *args):
        del args
        check = True

        def closurePop():
            statemachine.pop()

        for k, v in self.items_dict.items():
            if v > 0:
                check = False
        if check and not self.rollback:
            statemachine.closure = closurePop
        elif check and self.rollback:
            self.rollback = False
            look, path = self.tracker.returnHome()
            self.pathHandler = PathManipulator(path, self.checkEnd)  # TODO estimate ?
            self.pathHandler.execute()
        else:
            LookTransaction(self.updateAntLook).execute()

    def __init__(self, items_dict, rollback=False):
        super().__init__("SeekItems")
        self.progress = 0
        self.tracker = PositionTracker()
        self.pathHandler = None
        self.surface = max(ant.map_size.x, ant.map_size.y)
        self.items_dict = items_dict
        self.rollback = rollback
