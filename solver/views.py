from django.shortcuts import render
from .forms import SudokuForm

# Create your views here.
def sudoku_view(request):
    fields = [[f'cell_{i}_{j}' for j in range(9)] for i in range(9)]
    form = SudokuForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        board = form.cleaned_data
        # Now you can process the grid_data (9x9 list) for solving the puzzle
        # print(board)  # This prints the grid for debugging purposes
        solved_grid = solve_sudoku(board)
        # return render(request, 'solver/sudoku_form.html', {'form': form, 'fields': fields})
        return render(request, 'solver/result.html', {'solution': solved_grid})
        # return render(request, 'solver/sudoku_form.html', {'form': form, 'range':range(9), 'solved_grid': solved_grid})

    return render(request, 'solver/sudoku_form.html', {'form': form, 'fields': fields, 'range': range(9)})


def sudoku_solver_view(request):
    if request.method == 'POST':
        # Get the puzzle from the form
        puzzle = request.POST.get('puzzle', '')
        solution = solve_sudoku(puzzle)  # Call your Sudoku solver logic
        return render(request, 'solver/result.html', {'solution': solution})
    return render(request, 'solver/index.html')

def solve_sudoku(puzzle):
    # Integrate your Sudoku-solving logic here
    # Example placeholder:
    s = Sudoku()  # Create an object of MyClass
    s.read_input(puzzle)
    s.solver(0, 0)
    return s.sol #??? make an html page
    # s.printSolution()

class Sudoku:
    def __init__(self):
        self.grid = [[-1 for _ in range(9)] for _ in range(9)]
        self.sol = [[-1 for _ in range(9)] for _ in range(9)]
        self.rows = [set() for _ in range(9)]
        self.cols = [set() for _ in range(9)]
        self.boxes = [set() for _ in range(9)]
        self.sol_found = False

    def calc_boxes(self, row, col):
        if (row < 3 and col < 3):
            return 0
        elif (row < 3 and col > 2 and col < 6):
            return 1
        elif (row < 3 and col > 5):
            return 2
        elif (row > 2 and row < 6 and col < 3):
            return 3
        elif (row > 2 and row < 6 and col > 2 and col < 6):
            return 4
        elif(row > 2 and row < 6 and col > 5):
            return 5
        elif (row > 5 and col < 3):
            return 6
        elif (row > 5 and col > 2 and col < 6):
            return 7
        else:
            return 8
        
    def promising(self, row, col, val):
        if val in self.rows[row]:
            return False
        if val in self.cols[col]:
            return False
        box = self.calc_boxes(row, col)
        if val in self.boxes[box]:
            return False
        return True
    
    def solver(self, row, col):
        if row == 9:
            self.sol = self.grid
            self.sol_found = True
            return
        box = self.calc_boxes(row, col)
        next_col = col + 1
        next_row = row
        if (next_col >= 9):
            next_col = 0
            next_row = row + 1
        if (self.grid[row][col] == -1):
            for val in range(1, 10):
                if self.promising(row, col, val):
                    self.grid[row][col] = val
                    self.rows[row].add(val)
                    self.cols[col].add(val)
                    self.boxes[box].add(val)
                    self.solver(next_row, next_col)
                    if (self.sol_found):
                        return
                    self.grid[row][col] = -1
                    self.rows[row].remove(val)
                    self.cols[col].remove(val)
                    self.boxes[box].remove(val)        
        else:
            self.solver(next_row, next_col)


    def printSolution(self):
        for row in self.sol:
            print(" ".join(map(str, row)))
                # print(self.sol[row][col], end=" ")
            # print("\n")

    def read_input(self, input):
        for i in range(0,9):
            for j in range(0,9):
                # // int num = input[i][j] - '0';
                num = -1
                if (input[i][j] != "."):
                    num = int(input[i][j])
                box = self.calc_boxes(i, j)
                self.rows[i].add(num)
                self.cols[j].add(num)
                self.boxes[box].add(num)
                self.grid[i][j] = num