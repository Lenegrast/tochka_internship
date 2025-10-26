import heapq
import sys

COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_POSITIONS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
HALLWAY_SPOTS = [0, 1, 3, 5, 7, 9, 10]

class State:
    __slots__ = ('hallway', 'rooms', 'cost', 'room_size')
    
    def __init__(self, hallway, rooms, cost, room_size=2):
        self.hallway = tuple(hallway)
        self.rooms = tuple(tuple(room) for room in rooms)
        self.cost = cost
        self.room_size = room_size
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def is_done(self):
        for i, expected_type in enumerate(['A', 'B', 'C', 'D']):
            room = self.rooms[i]
            if len(room) != self.room_size or any(obj != expected_type for obj in room):
                return False
        return True
    
    def __hash__(self):
        return hash((self.hallway, self.rooms))
    
    def __eq__(self, other):
        return self.hallway == other.hallway and self.rooms == other.rooms

def can_move_through_hallway(hallway, start, end):
    if start == end:
        return True
    
    step = 1 if end > start else -1
    for pos in range(start + step, end + step, step):
        if hallway[pos] is not None:
            return False
    return True

def get_moves(state):
    moves = []
    hallway = list(state.hallway)
    rooms = [list(room) for room in state.rooms]
    room_types = ['A', 'B', 'C', 'D']
    room_size = state.room_size
    
    for hall_pos in range(11):
        if hallway[hall_pos] is not None:
            obj_type = hallway[hall_pos]
            target_room_idx = room_types.index(obj_type)
            target_room_pos = ROOM_POSITIONS[obj_type]
            target_room = rooms[target_room_idx]
            
            if not can_move_through_hallway(hallway, hall_pos, target_room_pos):
                continue
            
            if len(target_room) >= room_size:
                continue
            if target_room and any(obj != obj_type for obj in target_room):
                continue
            
            hallway_steps = abs(hall_pos - target_room_pos)
            room_steps = room_size - len(target_room)
            total_steps = hallway_steps + room_steps
            move_cost = total_steps * COSTS[obj_type]
            
            new_hallway = list(hallway)
            new_hallway[hall_pos] = None
            
            new_rooms = [list(room) for room in rooms]
            new_rooms[target_room_idx].append(obj_type)
            
            moves.append(State(new_hallway, new_rooms, state.cost + move_cost, room_size))
    
    
    for room_idx in range(4):
        room_type = room_types[room_idx]
        room = rooms[room_idx]
        
        if not room:
            continue
        
        if all(obj == room_type for obj in room):
            continue
        
        obj_to_move = room[0]
        room_entry_pos = ROOM_POSITIONS[room_type]
        
        room_depth = room_size - len(room) + 1
        
        for hall_pos in HALLWAY_SPOTS:
            if hallway[hall_pos] is not None:
                continue
            
            if not can_move_through_hallway(hallway, room_entry_pos, hall_pos):
                continue
            
            hallway_steps = abs(room_entry_pos - hall_pos)
            total_steps = room_depth + hallway_steps
            move_cost = total_steps * COSTS[obj_to_move]
            
            new_hallway = list(hallway)
            new_hallway[hall_pos] = obj_to_move
            
            new_rooms = [list(r) for r in rooms]
            new_rooms[room_idx].pop(0)
            
            moves.append(State(new_hallway, new_rooms, state.cost + move_cost, room_size))
    
    return moves

def solve(lines):
    if not lines or len(lines) < 3:
        return 0
    
    
    room_size = len(lines) - 3
    
    
    rooms = [[] for _ in range(4)]
    
    
    for depth in range(room_size):
        line = lines[2 + depth].strip()
        
        if line.startswith('  '):
            line = line[2:]
        
        if depth == 0:  
            positions = [3, 5, 7, 9]
        else:  
            positions = [1, 3, 5, 7]
        
        for j, pos in enumerate(positions):
            if pos < len(line) and line[pos] in 'ABCD':
                rooms[j].append(line[pos])
    
    initial_hallway = [None] * 11
    
    start = State(initial_hallway, rooms, 0, room_size)
    
    heap = [start]
    visited = set()
    min_cost = float('inf')
    
    while heap:
        state = heapq.heappop(heap)
        
        if state in visited:
            continue
        visited.add(state)
        
        if state.cost >= min_cost:
            continue
        
        if state.is_done():
            if state.cost < min_cost:
                min_cost = state.cost
            continue
        
        for new_state in get_moves(state):
            if new_state not in visited and new_state.cost < min_cost:
                heapq.heappush(heap, new_state)
    
    return min_cost if min_cost != float('inf') else 0

def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))
    
    result = solve(lines)
    print(result)

if __name__ == "__main__":
    main()