import sys

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_POS = {0: 2, 1: 4, 2: 6, 3: 8}
ROOM_FOR_TYPE = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
HALLWAY_STOPS = [0, 1, 3, 5, 7, 9, 10]

class PriorityQueue:
    def __init__(self):
        self.queue = []
    def push(self, item, priority):
        self.queue.append((priority, item))
        self.queue.sort()
    def pop(self):
        return self.queue.pop(0)
    def is_empty(self):
        return len(self.queue) == 0

def parse_input(lines):
    hallway = [None] * 11
    room_depth = len(lines) - 3
    rooms = [[None] * room_depth for _ in range(4)]
    for i, c in enumerate(lines[1][1:-1]):
        if c in "ABCD":
            hallway[i] = c
    for d in range(room_depth):
        line = lines[3 + d].rstrip()
        while len(line) < 11:
            line = " " + line
        for r, x in enumerate([3, 5, 7, 9]):
            ch = line[x]
            if ch in "ABCD":
                rooms[r][d] = ch
    state = tuple(hallway + [obj for room in rooms for obj in room])
    return state, room_depth

def is_final_state(state, room_depth):
    for r in range(4):
        start = 11 + r * room_depth
        for d in range(room_depth):
            obj = state[start + d]
            if obj not in ROOM_FOR_TYPE or ROOM_FOR_TYPE[obj] != r:
                return False
    return True

def can_move_to_room(state, obj, room, room_depth):
    if ROOM_FOR_TYPE[obj] != room:
        return None
    start = 11 + room * room_depth
    for d in range(room_depth):
        if state[start + d] not in (None, obj):
            return None
    for d in range(room_depth - 1, -1, -1):
        if state[start + d] is None:
            return d
    return None

def path_clear(state, start, end):
    step = 1 if start < end else -1
    for pos in range(start + step, end + step, step):
        if state[pos] is not None:
            return False
    return True

def get_moves(state, room_depth):
    moves = []
    for pos in HALLWAY_STOPS:
        obj = state[pos]
        if obj is None:
            continue
        room = ROOM_FOR_TYPE[obj]
        depth = can_move_to_room(state, obj, room, room_depth)
        if depth is None:
            continue
        room_pos = ROOM_POS[room]
        if not path_clear(state, pos, room_pos):
            continue
        steps = abs(pos - room_pos) + (depth + 1)
        cost = steps * COSTS[obj]
        new_state = list(state)
        new_state[pos] = None
        new_state[11 + room * room_depth + depth] = obj
        moves.append((tuple(new_state), cost))
    for room in range(4):
        start = 11 + room * room_depth
        for depth in range(room_depth):
            obj = state[start + depth]
            if obj is not None:
                if ROOM_FOR_TYPE[obj] == room and all(
                    state[start + d] == obj for d in range(depth, room_depth)
                ):
                    break
                for pos in HALLWAY_STOPS:
                    if path_clear(state, ROOM_POS[room], pos):
                        steps = (depth + 1) + abs(ROOM_POS[room] - pos)
                        cost = steps * COSTS[obj]
                        new_state = list(state)
                        new_state[start + depth] = None
                        new_state[pos] = obj
                        moves.append((tuple(new_state), cost))
                break
    return moves

def solve(lines):
    initial_state, room_depth = parse_input(lines)
    queue = PriorityQueue()
    queue.push(initial_state, 0)
    visited = {initial_state: 0}
    while not queue.is_empty():
        energy, state = queue.pop()
        if is_final_state(state, room_depth):
            return energy
        for new_state, cost in get_moves(state, room_depth):
            new_energy = energy + cost
            if new_state not in visited or new_energy < visited[new_state]:
                visited[new_state] = new_energy
                queue.push(new_state, new_energy)
    return -1

def main():
    lines = [line.rstrip('\n') for line in sys.stdin]
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()