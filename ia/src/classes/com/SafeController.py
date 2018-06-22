# coding = utf-8
from src.classes.com.Controller import Resources
from src.classes.ia_res.Ant import ant
from src.classes.ia_res.TrackableTransactions import InventoryTransaction
from src.classes.states.StateMachine import statemachine
from src.misc import my_print


class SafeController(object):

    def __init__(self):
        self.save = None
        self.endTransaction = None
        self.safe = True

    def clear_transaction(self, *args, **kwargs):
        my_print("END TRANSACTION")
        endTransa = self.endTransaction
        self.save = None
        self.endTransaction = None
        endTransa(*args, **kwargs)

    def clear_state(self, cli):
        del cli
        self.safe = True
        self.safe_exec(self.save)

    def estimate_food(self, inventory):
        from src.classes.states.SeekItemsState import SeekItemsState
        ant.inventory = inventory
        my_print("Food Level : ", inventory[Resources.Food])
        if inventory[Resources.Food] < self.save.get_estimated_time() / 126 or inventory[Resources.Food] < 7:
            my_print("EMERGENCY MOD")
            self.safe = False
            state = SeekItemsState({Resources.Food: int(self.save.get_estimated_time() / 126 + 10)}, True)
            state.on_pop = self.clear_state
            statemachine.push(state)
        else:
            self.endTransaction = self.save.end
            self.save.end = self.clear_transaction
            self.save.execute()

    def safe_exec(self, transaction):
        self.save = transaction
        InventoryTransaction(self.estimate_food).execute()

    def execute(self, transaction):
        my_print("START TRANSACTION")
        if self.save and self.safe:
            my_print(transaction)
            my_print(self.save)
            raise Exception("Invalid Concurrent transaction")
        if self.safe:
            self.safe_exec(transaction)
        else:
            transaction.execute()


safe_controller = SafeController()
