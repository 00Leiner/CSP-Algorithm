class CSPSolver {
  private variables: string[] = []; // Represents cells in the Sudoku grid
  private constraints: ((assignment: Record<string, number>) => boolean)[] = [];

  addVariable(cell: string) {
    this.variables.push(cell);
  }

  addConstraint(constraint: (assignment: Record<string, number>) => boolean) {
    this.constraints.push(constraint);
  }

  solve(): Record<string, number> | null {
    const assignment: Record<string, number> = {};

    return this.backtrack(assignment) ? assignment : null;
  }

  private backtrack(assignment: Record<string, number>): boolean {
    if (this.isComplete(assignment)) {
      return true; // Solution found
    }

    const cell = this.selectUnassignedVariable(assignment);

    for (let value = 1; value <= 9; value++) {
      if (this.isValueConsistent(cell, value, assignment)) {
        assignment[cell] = value;
        if (this.backtrack(assignment)) {
          return true;
        }
        delete assignment[cell];
      }
    }

    return false; // No valid assignment found
  }

  private isComplete(assignment: Record<string, number>): boolean {
    return this.variables.every((cell) => assignment[cell] !== undefined);
  }

  private selectUnassignedVariable(assignment: Record<string, number>): string {
    return this.variables.find((cell) => assignment[cell] === undefined) || '';
  }

  private isValueConsistent(
    cell: string,
    value: number,
    assignment: Record<string, number>
  ): boolean {
    assignment[cell] = value;
    for (const constraint of this.constraints) {
      if (!constraint(assignment)) {
        delete assignment[cell];
        return false;
      }
    }
    return true;
  }
}

// Sudoku Example:
const solver = new CSPSolver();

// Define Sudoku cells as variables
const sudokuCells = [];
for (let row = 1; row <= 9; row++) {
  for (let col = 1; col <= 9; col++) {
    sudokuCells.push(`R${row}C${col}`);
  }
} 

// Add Sudoku variables
for (const cell of sudokuCells) {
  solver.addVariable(cell);
}

// Define Sudoku constraints
// 1. Each row must contain all numbers from 1 to 9 without repetition.
for (let row = 1; row <= 9; row++) {
  const rowCells = sudokuCells.filter((cell) => cell.startsWith(`R${row}`));
  solver.addConstraint((assignment) => new Set(rowCells.map((cell) => assignment[cell])).size === 9);
}

// 2. Each column must contain all numbers from 1 to 9 without repetition.
for (let col = 1; col <= 9; col++) {
  const colCells = sudokuCells.filter((cell) => cell.startsWith(`C${col}`));
  solver.addConstraint((assignment) => new Set(colCells.map((cell) => assignment[cell])).size === 9);
}

// 3. Each 3x3 sub-grid must contain all numbers from 1 to 9 without repetition.
const subGrids = [
  ['R1C1', 'R1C2', 'R1C3', 'R2C1', 'R2C2', 'R2C3', 'R3C1', 'R3C2', 'R3C3'],
  ['R1C4', 'R1C5', 'R1C6', 'R2C4', 'R2C5', 'R2C6', 'R3C4', 'R3C5', 'R3C6'],
  ['R1C7', 'R1C8', 'R1C9', 'R2C7', 'R2C8', 'R2C9', 'R3C7', 'R3C8', 'R3C9'],
  ['R4C1', 'R4C2', 'R4C3', 'R5C1', 'R5C2', 'R5C3', 'R6C1', 'R6C2', 'R6C3'],
  ['R4C4', 'R4C5', 'R4C6', 'R5C4', 'R5C5', 'R5C6', 'R6C4', 'R6C5', 'R6C6'],
  ['R4C7', 'R4C8', 'R4C9', 'R5C7', 'R5C8', 'R5C9', 'R6C7', 'R6C8', 'R6C9'],
  ['R7C1', 'R7C2', 'R7C3', 'R8C1', 'R8C2', 'R8C3', 'R9C1', 'R9C2', 'R9C3'],
  ['R7C4', 'R7C5', 'R7C6', 'R8C4', 'R8C5', 'R8C6', 'R9C4', 'R9C5', 'R9C6'],
  ['R7C7', 'R7C8', 'R7C9', 'R8C7', 'R8C8', 'R8C9', 'R9C7', 'R9C8', 'R9C9'],
];

for (const subGrid of subGrids) {
  solver.addConstraint((assignment) => new Set(subGrid.map((cell) => assignment[cell])).size === 9);
}

const initialPuzzle: Record<string, number> = {
  R1C1: 5,
  R1C2: 3,
  R1C5: 7,
  R2C1: 6,
  R2C4: 1,
  R2C5: 9,
  R2C6: 5,
  R3C2: 9,
  R3C3: 8,
  R3C8: 6,
  R4C1: 8,
  R4C5: 6,
  R4C9: 3,
  R5C1: 4,
  R5C4: 8,
  R5C6: 3,
  R5C9: 1,
  R6C1: 7,
  R6C5: 2,
  R6C9: 6,
  R7C2: 6,
  R7C7: 2,
  R7C8: 8,
  R8C4: 4,
  R8C5: 1,
  R8C6: 9,
  R8C9: 5,
  R9C5: 8,
  R9C8: 7,
  R9C9: 9,
};

// Set initial values in the Sudoku puzzle
for (const cell in initialPuzzle) {
  solver.addConstraint((assignment) => assignment[cell] === initialPuzzle[cell]);
}

// Solve the Sudoku puzzle
const solution = solver.solve();

if (solution) {
  console.log('Sudoku Solution:');
  console.log(solution);
} else {
  console.log('No solution found.');
}