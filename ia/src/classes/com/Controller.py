# coding = utf-8

import enum
import ia.src.classes.com.Client as COM
from ia.src.classes.ia_res.Ant import ant


class Cmd(enum.Enum):
    Forward = "Forward"
    Right = "Right"
    Left = "Left"
    Look = "Look"
    Inventory = "Inventory"
    Broadcast = "Broadcast"
    Connect_nbr = "Connect_nbr"
    Fork = "Fork"
    Eject = "Eject"
    Take = "Take"
    Set = "Set"
    IncantationStart = "Incantation"
    IncantationStop = None


class Resources(enum.Enum):
    Food = "food"
    Linemate = "linemate"
    Deraumere = "deraumere"
    Sibur = "sibur"
    Mendiane = "mendiane"
    Phiras = "phiras"
    Thystame = "thystame"


required = {
    2: (1, {Resources.Linemate: 1}),
    # 3: (2, {Resources.Linemate: 1}),
    # 4: (2, {Resources.Linemate: 2}),
    # 5: (4, {Resources.Linemate: 1}),
    # 6: (4, {Resources.Linemate: 1}),
    # 7: (6, {Resources.Linemate: 1}),
    # 8: (6, {Resources.Linemate: 2}),
}


class GameException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr("GameException : " + self.value)


def defaultError():
    raise GameException("An unexpected result come from a safe call")


def defaultConnectNbr(nbr):
    ant.current_nbr = int(nbr)


class Controller(object):
    """
    All callbacks take no arguments until it's specify
    """

    def __init__(self):
        self._answersCallers = {
            Cmd.Forward: Controller._applyDefault,
            Cmd.Right: Controller._applyDefault,
            Cmd.Left: Controller._applyDefault,
            Cmd.Look: Controller._applyLook,
            Cmd.Inventory: Controller._applyInventory,
            Cmd.Broadcast: Controller._applyDefault,
            Cmd.Connect_nbr: Controller._applyArgOK,
            Cmd.Fork: Controller._applyDefault,
            Cmd.Eject: Controller._applyDefault,
            Cmd.Take: Controller._applyTake,
            Cmd.Set: Controller._applySet,
            Cmd.IncantationStart: Controller._applyDefault,
            Cmd.IncantationStop: Controller._applyDefault,
        }
        self._cmdStack = []
        self._takeQueue = []
        self._setQueue = []
        self._writeStack = []

    def _write(self, value):
        if len(self._cmdStack) >= 10:
            self._cmdStack.append(value)
        else:
            COM.cli.write(value)

    def move(self, callback):
        cmd = Cmd.Forward
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def right(self, callback):
        cmd = Cmd.Right
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def left(self, callback):
        cmd = Cmd.Left
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def look(self, callback):
        """
        :param callback: (look list of dict) -> void
        :return: void
        """
        cmd = Cmd.Look
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def inventory(self, callback):
        """
        :param callback: (inventory dict) -> void
        :return: void
        """
        cmd = Cmd.Inventory
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def broadcast(self, msg, callback):
        cmd = Cmd.Broadcast
        self._write(' '.join((cmd.value, msg)))
        self._cmdStack.append((cmd, callback, defaultError))

    def connect_number(self, callback=defaultConnectNbr):
        """
        :param callback: (connect_numbers) -> void x 1
        :return:
        """
        cmd = Cmd.Connect_nbr
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def fork(self, callback):
        cmd = Cmd.Fork
        self._write(cmd.value)
        self._cmdStack.append((cmd, callback, defaultError))

    def eject(self, ok, ko):
        cmd = Cmd.Eject
        self._write(cmd.value)
        self._cmdStack.append((cmd, ok, ko))

    def take(self, type, ok, ko):
        """
        :param callback: (object) -> void x 2
        :return:
        """
        if type(type) != Resources:
            raise Exception("Invalid type")
        cmd = Cmd.Take
        self._write(' '.join((cmd.value, type.value)))
        self._cmdStack.append((cmd, ok, ko))
        self._takeQueue.append(type.value)

    def set(self, type, ok, ko):
        """
        :param callback: (object) -> void x 2
        :return:
        """
        if type(type) != Resources:
            raise Exception("Invalid type")
        cmd = Cmd.Set
        self._write(' '.join((cmd.value, type.value)))
        self._cmdStack.append((cmd, ok, ko))
        self._setQueue.append(type.value)

    def incantation(self, ok_start, ko_start, ok_end, ko_end):
        cmd = Cmd.IncantationStart
        self._write(cmd.value)
        self._cmdStack.append((cmd, ok_start, ko_start))
        self._cmdStack.append((cmd, ok_end, ko_end))

    @staticmethod
    def _applyDefault(server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2]()
        cmd_item[1]()

    @staticmethod
    def _applyArgOK(server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2]()
        cmd_item[1](server_answer)

    def _applySet(self, server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2](self._setQueue.pop(0))
        cmd_item[1](self._setQueue.pop(0))

    def _applyTake(self, server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2](self._takeQueue.pop(0))
        cmd_item[1](self._takeQueue.pop(0))

    @staticmethod
    def _applyLook(server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2]()
        server_answer = server_answer[1:-1].split(', ')
        while '' in server_answer:
            server_answer.remove('')
        for i in range(len(server_answer)):
            server_answer[i] = server_answer[i].split(' ')
            while '' in server_answer[i]:
                server_answer[i].remove('')
        cmd_item[1](server_answer)

    @staticmethod
    def _applyInventory(server_answer, cmd_item):
        if server_answer == "ko":
            cmd_item[2]()
        server_answer = server_answer[1:-1].split(', ')
        while '' in server_answer:
            server_answer.remove('')
        for i in range(len(server_answer)):
            server_answer[i] = server_answer[i].split(' ')
            while '' in server_answer[i]:
                server_answer[i].remove('')
        items = {Resources(v[0]): int(v[1]) for v in server_answer}
        cmd_item[1](items)

    def applyTop(self, server_answer):
        try:
            value = self._cmdStack.pop(0)
            self._answersCallers[value[0]](server_answer, value)
            return True
        except IndexError:
            return False

    def flushCmds(self):
        while len(self._cmdStack) < 10 and len(self._writeStack):
            value = self._writeStack.pop(0)
            COM.cli.write(value)

    def hasBufferizedCmds(self):
        return len(self._writeStack) != 0

    def checkEndGame(self, args):
        for elem in args:
            if elem == "dead":
                raise GameException("You died")


controller = Controller()
