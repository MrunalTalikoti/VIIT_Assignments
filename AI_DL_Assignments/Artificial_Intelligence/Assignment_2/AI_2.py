class MissionaryCannibal:
    def __init__(self):
        self.left = [3, 3, 1]  # [missionaries, cannibals, boat]
        self.right = [0, 0, 0]

    def display_state(self):
        print(f"Left side: {self.left[0]} Missionaries, {self.left[1]} Cannibals, Boat: {'Yes' if self.left[2] == 1 else 'No'}")
        print(f"Right side: {self.right[0]} Missionaries, {self.right[1]} Cannibals, Boat: {'Yes' if self.right[2] == 1 else 'No'}")

    def move(self, missionaries, cannibals, to_right):
        if missionaries + cannibals > 2 or missionaries < 0 or cannibals < 0 or (missionaries == 0 and cannibals == 0):
            return False

        if to_right:
            if self.left[0] >= missionaries and self.left[1] >= cannibals and self.left[2] == 1:
                self.left[0] -= missionaries
                self.left[1] -= cannibals
                self.right[0] += missionaries
                self.right[1] += cannibals
                self.left[2] = 0
                self.right[2] = 1
                return True
        else:
            if self.right[0] >= missionaries and self.right[1] >= cannibals and self.right[2] == 1:
                self.right[0] -= missionaries
                self.right[1] -= cannibals
                self.left[0] += missionaries
                self.left[1] += cannibals
                self.right[2] = 0
                self.left[2] = 1
                return True
        return False

    def check_lose(self):
        if (self.left[0] > 0 and self.left[1] > self.left[0]) or (self.right[0] > 0 and self.right[1] > self.right[0]):
            return True
        return False

    def win(self):
        if self.right[0] == 3 and self.right[1] == 3:
            return True
        return False

def main():
    game = MissionaryCannibal()

    while True:
        game.display_state()
        if game.win():
            print("Congratulations! All missionaries and cannibals have successfully crossed the river.")
            break

        if game.check_lose():
            print("You lose. Cannibals outnumber missionaries on one side.")
            break

        try:
            missionaries = int(input("Enter number of missionaries to move: "))
            cannibals = int(input("Enter number of cannibals to move: "))
        except ValueError:
            print("Invalid input. Please enter integers.")
            continue

        to_right = game.left[2] == 1

        if not game.move(missionaries, cannibals, to_right):
            print("Invalid move. Try again.")

if __name__ == "__main__":
    main()
