import random

SIZE = 10

# --- Допоміжні функції ---
def create_board():
    return [["." for _ in range(SIZE)] for _ in range(SIZE)]

def print_board(board, hide=False):
    print("   " + " ".join(str(i) for i in range(SIZE)))
    for i, row in enumerate(board):
        line = []
        for cell in row:
            if hide and cell == "S":
                line.append(".")
            else:
                line.append(cell)
        print(f"{i:2} " + " ".join(line))
    print()

def is_valid(board, x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE

def can_place(board, x, y):
    if not is_valid(board, x, y) or board[x][y] != ".":
        return False
    # перевірка сусідніх клітинок
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            nx, ny = x + dx, y + dy
            if is_valid(board, nx, ny) and board[nx][ny] == "S":
                return False
    return True

def place_ship(board, length):
    placed = False
    while not placed:
        x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        orientation = random.choice(["H", "V"])
        coords = []
        for i in range(length):
            nx = x + (i if orientation == "V" else 0)
            ny = y + (i if orientation == "H" else 0)
            if not can_place(board, nx, ny):
                break
            coords.append((nx, ny))
        if len(coords) == length:
            for nx, ny in coords:
                board[nx][ny] = "S"
            placed = True

def place_all_ships(board):
    place_ship(board, 4)
    for _ in range(2):
        place_ship(board, 2)
    for _ in range(2):
        place_ship(board, 1)

def shoot(board, x, y):
    if board[x][y] == "S":
        board[x][y] = "X"
        return True
    elif board[x][y] == ".":
        board[x][y] = "*"
    return False

def ships_remaining(board):
    return sum(row.count("S") for row in board)

# --- Основна гра ---
def play_game():
    player_board = create_board()
    comp_board = create_board()
    place_all_ships(player_board)
    place_all_ships(comp_board)

    comp_shots = set()

    while True:
        print("Ваше поле:")
        print_board(player_board)
        print("Поле комп'ютера:")
        print_board(comp_board, hide=True)

        # хід гравця
        try:
            x, y = map(int, input("Ваш постріл (x y): ").split())
        except:
            print("Некоректний ввід!")
            continue
        if not is_valid(comp_board, x, y):
            print("Координати поза межами поля!")
            continue
        hit = shoot(comp_board, x, y)
        print("Влучили!" if hit else "Мимо!")

        if ships_remaining(comp_board) == 0:
            print("Ви перемогли!")
            break

        # хід комп'ютера
        while True:
            cx, cy = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
            if (cx, cy) not in comp_shots:
                comp_shots.add((cx, cy))
                break
        hit = shoot(player_board, cx, cy)
        print(f"Комп'ютер стріляє у ({cx}, {cy}) -> {'Влучив!' if hit else 'Мимо!'}")

        if ships_remaining(player_board) == 0:
            print("Комп'ютер переміг!")
            break

if __name__ == "__main__":
    play_game()