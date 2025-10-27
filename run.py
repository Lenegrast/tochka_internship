import heapq
import sys

energy_costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
letter_to_room = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
room_to_letter = {0: 'A', 1: 'B', 2: 'C', 3: 'D'}
forbidden_hall_positions = [2, 4, 6, 8]

def read_input(lines):
    depth = 2 if len(lines) == 5 else 4
    hall = lines[1][1:12]
    rooms = []
    for i in range(4):
        s = ''
        for j in range(2, 2 + depth):
            s += lines[j][3 + i * 2]
        rooms.append(s)
    return hall, tuple(rooms), depth

def check_goal(rooms, depth):
    return rooms == tuple(ch * depth for ch in "ABCD")

def push_state(queue, seen, new_state, new_cost):
    if new_cost < seen.get(new_state, float('inf')):
        seen[new_state] = new_cost
        heapq.heappush(queue, (new_cost, new_state))

def move_from_room_to_hall(hall, rooms, room_index, pos, ch, depth_in_room, door, cost):
    new_hall = hall[:pos] + ch + hall[pos + 1:]
    temp_rooms = list(rooms)
    temp_room = list(temp_rooms[room_index])
    temp_room[depth_in_room] = '.'
    temp_rooms[room_index] = ''.join(temp_room)
    new_rooms = tuple(temp_rooms)
    new_cost = cost + (abs(pos - door) + depth_in_room + 1) * energy_costs[ch]
    return new_hall, new_rooms, new_cost

def move_from_hall_to_room(hall, rooms, pos, ch, room_index, door, cost):
    temp_rooms = list(rooms)
    r = list(temp_rooms[room_index])
    idx = len(r) - 1
    while r[idx] != '.':
        idx -= 1
    r[idx] = ch
    temp_rooms[room_index] = ''.join(r)
    new_rooms = tuple(temp_rooms)
    new_hall = hall[:pos] + '.' + hall[pos + 1:]
    new_cost = cost + (abs(pos - door) + idx + 1) * energy_costs[ch]
    return new_hall, new_rooms, new_cost

def possible_moves_from_rooms(hall, rooms):
    result = []
    for room_index, room in enumerate(rooms):
        if all(ch == '.' or ch == room_to_letter[room_index] for ch in room):
            continue
        door = 2 + room_index * 2
        d = 0
        while rooms[room_index][d] == '.':
            d += 1
        ch = room[d]
        for pos in range(door - 1, -1, -1):
            if hall[pos] != '.':
                break
            if pos not in forbidden_hall_positions:
                result.append((room_index, pos, ch, d, door))
        for pos in range(door + 1, 11):
            if hall[pos] != '.':
                break
            if pos not in forbidden_hall_positions:
                result.append((room_index, pos, ch, d, door))
    return result

def possible_moves_to_rooms(hall, rooms):
    result = []
    for pos, ch in enumerate(hall):
        if ch == '.':
            continue
        room_index = letter_to_room[ch]
        door = 2 + room_index * 2
        if any(c != '.' and c != ch for c in rooms[room_index]):
            continue
        path = range(pos + 1, door + 1) if pos < door else range(door, pos)
        if any(hall[p] != '.' for p in path):
            continue
        result.append((pos, ch, room_index, door))
    return result

def solve(lines):
    hall, rooms, depth = read_input(lines)
    start = (hall, rooms)
    queue = [(0, start)]
    seen = {start: 0}

    while queue:
        cost, state = heapq.heappop(queue)
        if cost > seen[state]:
            continue
        hall, rooms = state
        if check_goal(rooms, depth):
            return cost
        for r_i, pos, ch, d, door in possible_moves_from_rooms(hall, rooms):
            nh, nr, nc = move_from_room_to_hall(hall, rooms, r_i, pos, ch, d, door, cost)
            push_state(queue, seen, (nh, nr), nc)
        for pos, ch, r_i, door in possible_moves_to_rooms(hall, rooms):
            nh, nr, nc = move_from_hall_to_room(hall, rooms, pos, ch, r_i, door, cost)
            push_state(queue, seen, (nh, nr), nc)
    return 0

def main():
    lines = [line.strip() for line in sys.stdin]
    print(solve(lines))

if __name__ == "__main__":
    main()