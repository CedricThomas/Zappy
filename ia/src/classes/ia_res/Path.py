# coding = utf-8
import math
from ia.src.classes.ia_res.Ant import Vector
from ia.src.classes.com.Controller import Cmd, controller


def vecSize(vector):
    return math.sqrt(vector.x * vector.x + vector.y * vector.y)


def normalize(vector):
    size = vecSize(vector)
    if size == 0:
        return Vector()
    return Vector(vector.x / size, vector.y / size)

class PointEvent(object):

    def __init__(self, item, nb, time_estimation):
        self.item = item
        self.nb = nb
        self._time_estimation = time_estimation
        self.position = Vector()

    @property
    def time_estimation(self):
        return self._time_estimation

    def execute(self):
        raise NotImplementedError("execute")

class TakeEvent(PointEvent):

    def __init__(self, item, nb, time_estimation, last, ok, ko):
        super().__init__(item, nb, time_estimation)
        self.last = last
        self.ko = ko
        self.ok = ok

    def execute(self):
        print("take execute ", self.item.value)
        for j in range(self.nb):
            if j == self.nb - 1:
                controller.take(self.item, self.last, self.ko)
            else:
                controller.take(self.item, self.ok, self.ko)

class SetEvent(PointEvent):

    def __init__(self, item, nb, time_estimation, last, ok, ko):
        super().__init__(item, nb, time_estimation)
        self.last = last
        self.ko = ko
        self.ok = ok

    def execute(self):
        raise NotImplementedError("execute")

class Path(object):

    def __init__(self):
        self.path = list()

        self.points = list()

    def addPoint(self, pos, callback):
        callback.position = pos
        self.points.append((pos, callback))

    def addConePoint(self, idx, callback):
        pos = None
        min_val = 0
        max_val = 0
        deep = 0
        while pos is None:
            if min_val <= idx <= max_val:
                middle = min_val + (max_val - min_val) // 2
                x = idx - middle
                pos = Vector(x, deep)
            deep += 1
            min_val = max_val + 1
            max_val = min_val + deep * 2
        self.addPoint(pos, callback)

    def _alignX(self, look, src_point, dest_point):
        wsrc_point = Vector(src_point.x, 0)
        wdest_point = Vector(dest_point.x, 0)
        dir_vec = normalize(Vector(wdest_point.x - wsrc_point.x, wdest_point.y - wsrc_point.y))
        nlook = normalize(look)
        new_look = dir_vec
        moves = list()
        if nlook.y == 0 and nlook.x == -dir_vec.x and nlook.x != 0:
            moves += [Cmd.Left, Cmd.Left]
        elif nlook.y != 0 and dir_vec.x == -nlook.y:
            moves += [Cmd.Left]
        elif nlook.y != 0 and dir_vec.x == nlook.y:
            moves += [Cmd.Right]
        else:
            new_look = look
        size = vecSize(Vector(wdest_point.x - wsrc_point.x, wdest_point.y - wsrc_point.y))
        for i in range(int(size)):
            moves += [Cmd.Forward]
        return new_look, moves, Vector(dest_point.x, src_point.y)

    def _alignY(self, look, src_point, dest_point):
        wsrc_point = Vector(0, src_point.y)
        wdest_point = Vector(0, dest_point.y)
        dir_vec = normalize(Vector(wdest_point.x - wsrc_point.x, wdest_point.y - wsrc_point.y))
        nlook = normalize(look)
        new_look = dir_vec
        moves = list()
        if nlook.x == 0 and nlook.y == -dir_vec.y and nlook.y != 0:
            moves += [Cmd.Left, Cmd.Left]
        elif nlook.x != 0 and dir_vec.y == nlook.x:
            moves += [Cmd.Left]
        elif nlook.x != 0 and dir_vec.y == -nlook.x:
            moves += [Cmd.Right]
        else:
            new_look = look
        size = vecSize(Vector(wdest_point.x - wsrc_point.x, wdest_point.y - wsrc_point.y))
        for i in range(int(size)):
            moves += [Cmd.Forward]
        return new_look, moves, Vector(src_point.x, dest_point.y)

    def _calcMove(self, look, src_point, dest_point):
        if src_point.x == dest_point.x and src_point.y == dest_point.y:
            return look, list()
        xylook = look
        xysrc_point = src_point
        xyactions_list = list()
        xylook, new_moves, xysrc_point = self._alignX(xylook, xysrc_point, dest_point)
        xyactions_list += new_moves
        xylook, new_moves, xysrc_point = self._alignY(xylook, xysrc_point, dest_point)
        xyactions_list += new_moves
        yxlook = look
        yxsrc_point = src_point
        yxactions_list = list()
        yxlook, new_moves, yxsrc_point = self._alignY(yxlook, yxsrc_point, dest_point)
        yxactions_list += new_moves
        yxlook, new_moves, yxsrc_point = self._alignX(yxlook, yxsrc_point, dest_point)
        yxactions_list += new_moves

        if len(yxactions_list) < len(xyactions_list):
            return yxlook, yxactions_list
        return xylook, xyactions_list

    def _generateGoOpti(self, path, moves, points, current_point, current_look):
        if len(points) == 0:
            len_go = len(self.path)
            if len(moves) < len_go or len_go == 0:
                self.path = moves
            return
        save = list(points)
        move_save = list(moves)
        for i in range(len(points)):
            save.pop(i)
            path.insert(0, points[i][0])
            new_look, new_moves = self._calcMove(current_look, current_point, points[i][0])
            moves += new_moves + [points[i][1]]
            self._generateGoOpti(path, moves, save, points[i][0], new_look)
            moves = list(move_save)
            path.pop(0)
            save = list(points)

    def _generateGoOrder(self, points, current_point, current_look):
        actions_list = list()
        for point in points:
            current_look, actions = self._calcMove(current_look, current_point, point[0])
            actions_list += actions + [point[1]]
            current_point = point[0]
        self.path = actions_list

    def generateOpti(self):
        self._generateGoOpti(list(), list(), self.points, Vector(), Vector(0, 1))
        ret = self.path
        self.path = list()
        return ret

    def generateOrder(self):
        self._generateGoOrder(self.points, Vector(), Vector(0, 1))
        ret = self.path
        self.path = list()
        return ret


class PathManipulator(object):

    def __init__(self, path):
        self.cmds = {
            Cmd.Forward: controller.forward,
            Cmd.Left: controller.left,
            Cmd.Right: controller.right,
        }
        self.path = path

    def costEstimation(self, next_point=False):
        cost = 0
        for elem in self.path:
            if type(elem) is Cmd:
                cost += 7
            elif type(elem) is PointEvent:
                cost += elem.time_estimation
                if next_point:
                    break
        return cost

    def step(self, callback=lambda: None):
        user_cmd = None
        if len(self.path) == 0:
            return False, type(user_cmd) == Cmd
        first = self.path.pop(0)
        if issubclass(type(first), PointEvent):
            first.execute()
            return True, False
        if len(self.path) != 0 and issubclass(type(self.path[0]), PointEvent):
            user_cmd = self.path.pop(0)

        def call():
            callback()
            if user_cmd:
                user_cmd.execute()

        self.cmds[first](call)
        return True, not issubclass(type(self.path[0]), PointEvent)

    def stepNextPoint(self, callback=lambda: None):
        stepped, is_cmd = self.step(callback)
        while stepped and is_cmd:
            stepped, is_cmd = self.step(callback)
        return stepped