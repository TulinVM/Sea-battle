
class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = set()

    def is_sunk(self):
        return len(self.hits) == len(self.coordinates)

    def hit(self, coordinate):
        if coordinate in self.coordinates:
            self.hits.add(coordinate)
            return True
        return False

import random


class Board:
    def __init__(self, size=6):
        self.size = size
        self.ships = []
        self.shots = set()
        self.grid = [['O'] * size for _ in range(size)]

    def add_ship(self, ship):
        if self.can_place_ship(ship):
            self.ships.append(ship)
            for x, y in ship.coordinates:
                self.grid[y][x] = '■'

    def can_place_ship(self, ship):
        for x, y in ship.coordinates:
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return False
            if self.grid[y][x] == '■':
                return False
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size:
                        if self.grid[ny][nx] == '■':
                            return False
        return True

    def receive_shot(self, x, y):
        if (x, y) in self.shots:
            raise ValueError("Already shot at this coordinate.")
        self.shots.add((x, y))

        for ship in self.ships:
            if ship.hit((x, y)):
                self.grid[y][x] = 'X'
                if ship.is_sunk():
                    print("Ship sunk!")
                return True

        self.grid[y][x] = 'T'
        return False

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
        print()


class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.place_ships(self.player_board)
        self.place_ships(self.computer_board)
        self.current_turn = 'player'

    def place_ships(self, board):
        ship_sizes = [3, 2, 2, 1, 1, 1, 1]
        for size in ship_sizes:
            placed = False
            while not placed:
                x = random.randint(0, board.size - 1)
                y = random.randint(0, board.size - 1)
                orientation = random.choice(['horizontal', 'vertical'])
                coordinates = []
                for i in range(size):
                    if orientation == 'horizontal':
                        coordinates.append((x + i, y))
                    else:
                        coordinates.append((x, y + i))
                ship = Ship(coordinates)
                if board.can_place_ship(ship):
                    board.add_ship(ship)
                    placed = True

    def player_turn(self):
        print("Player's turn")
        self.player_board.display()
        while True:
            try:
                x = int(input("Enter X coordinate: ")) - 1
                y = int(input("Enter Y coordinate: ")) - 1
                hit = self.computer_board.receive_shot(x, y)
                if hit:
                    print("Hit!")
                else:
                    print("Miss!")
                break
            except ValueError as e:
                print(e)

    def computer_turn(self):
        print("Computer's turn")
        while True:
            x = random.randint(0, self.computer_board.size - 1)
            y = random.randint(0, self.computer_board.size - 1)
            try:
                hit = self.player_board.receive_shot(x, y)
                if hit:
                    print(f"Computer hit at ({x + 1}, {y + 1})!")
                else:
                    print(f"Computer miss at ({x + 1}, {y + 1}).")
                break
            except ValueError:
                continue

    def play(self):
        while not self.player_board.all_ships_sunk() and not self.computer_board.all_ships_sunk():
            if self.current_turn == 'player':
                self.player_turn()
                self.current_turn = 'computer'
            else:
                self.computer_turn()
                self.current_turn = 'player'

        if self.player_board.all_ships_sunk():
            print("Computer wins!")
        else:
            print("Player wins!")

1

if __name__ == "__main__":
    game = Game()
    game.play()
