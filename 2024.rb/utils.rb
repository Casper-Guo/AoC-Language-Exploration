# Utility class for grids/matrices etc.
# Assumes the input is rectangular

def ints(line)
  line.scan(/-?\d+/).map(&:to_i)
end

# utility functions for a 2D grid
class Grid
  attr_accessor :grid, :num_rows, :num_cols

  # clockwise from north
  @@neighbor_delta = [[-1, 0], [0, 1], [1, 0], [0, -1]]
  @@adj_delta = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]

  def initialize(grid)
    @grid = grid
    @num_rows = grid.length
    @num_cols = grid[0].length
  end

  def [](coord)
    @grid[coord[0]][coord[1]]
  end

  def []=(coord, val)
    @grid[coord[0]][coord[1]] = val
  end

  def to_s
    @grid.map { |row| row.join('') }.join("\n")
  end

  def inbound?(row, col)
    row.between?(0, @num_rows - 1) && col.between?(0, @num_cols - 1)
  end

  def euclid(row1, col1, row2, col2)
    Math.sqrt((row2 - row1)**2 + (col2 - col1)**2)
  end

  def manhattan(row1, col1, row2, col2)
    (row2 - row1).abs + (col2 - col1).abs
  end

  def chebyshev(row1, col1, row2, col2)
    [(row2 - row1).abs, (col2 - col1).abs].max
  end

  def coords
    coords = []
    (0...@num_rows).each do |row|
      (0...@num_cols).each do |col|
        coords << [row, col]
      end
    end
    coords
  end

  def get_row(row)
    @grid[row]
  end

  def get_col(col)
    (0...@num_rows).map { |row| @grid[[row, col]] }
  end

  def at(row, col)
    inbound?(row, col) ? @grid[row][col] : nil
  end

  def find(item)
    instances = []
    (0...@num_rows).each do |row|
      (0...@num_cols).each do |col|
        instances << [row, col] if @grid[row][col] == item
      end
    end
    instances
  end

  def get_direct_neighbors(row, col, all: false)
    neighbors = []
    @@neighbor_delta.each do |drow, dcol|
      neighbor = [row + drow, col + dcol]
      if !all
        neighbors << [neighbor, at(*neighbor)] if inbound?(*neighbor)
      else
        neighbors << [neighbor, at(*neighbor)]
      end
    end
    neighbors
  end

  def get_adjacent_neighbors(row, col, all: false)
    neighbors = []
    @@adj_delta.each do |drow, dcol|
      neighbor = [row + drow, col + dcol]
      if !all
        neighbors << [neighbor, at(*neighbor)] if inbound?(*neighbor)
      else
        neighbors << [neighbor, at(*neighbor)]
      end
    end
    neighbors
  end

  def move_one(row, col, drow, dcol)
    [row + drow, col + dcol]
  end

  def move_n(row, col, drow, dcol, n)
    [row + drow * n, col + dcol * n]
  end

  def get_direction(from_row, from_col, to_row, to_col)
    [to_row - from_row, to_col - from_col]
  end
end

DELTA_TO_DIRECTION = {
  [-1, 0] => 'N',
  [0, 1] => 'E',
  [1, 0] => 'S',
  [0, -1] => 'W'
}.freeze

DELTA_TO_CHAR = {
  [-1, 0] => '^',
  [0, 1] => '>',
  [1, 0] => 'v',
  [0, -1] => '<'
}.freeze

DIRECTION_TO_DELTA = DELTA_TO_DIRECTION.invert
CHAR_TO_DELTA = DELTA_TO_CHAR.invert

# reverse assembler and simulator for 2024 day 17 ISA
class Computer
  attr_accessor :program, :regA, :regB, :regC

  @@opcodes = {
    0 => 'adv',
    1 => 'bxl',
    2 => 'bst',
    3 => 'jnz',
    4 => 'bxc',
    5 => 'out',
    6 => 'bdv',
    7 => 'cdv'
  }

  def initialize(program, regA = 0, regB = 0, regC = 0)
    @program = program
    @regA = regA
    @regB = regB
    @regC = regC
  end

  def get_combo_operand(arg)
    case arg
    when (0..3)
      arg
    when 4
      @regA
    when 5
      @regB
    when 6
      @regC
    end
  end

  def arg_to_s(arg)
    case arg
    when (0..3)
      arg.to_s
    when 4
      'A'
    when 5
      'B'
    when 6
      'C'
    end
  end

  def instr_to_s(opcode, arg)
    case opcode
    when 0, 2, 5, 6, 7
      "#{@@opcodes[opcode]} #{arg_to_s(arg)}"
    when 1, 3
      "#{@@opcodes[opcode]} #{arg}"
    when 4
      'bxc'
    end
  end

  def print_reg
    puts "regA: #{@regA.to_s(2)} regB: #{@regB.to_s(2)} regC: #{@regC.to_s(2)}"
  end

  def assemble
    instructions = []
    @program.each_slice(2) do |opcode, arg|
      instructions << instr_to_s(opcode, arg)
    end
    "#{instructions.join("\n")}\n"
  end

  def simulate(log: false, string: true)
    output = []
    print_reg if log
    pc = 0

    until pc >= @program.length - 1
      opcode = @program[pc]
      arg = @program[pc + 1]
      jump = false

      case opcode
      when 0
        @regA = (@regA / 2**get_combo_operand(arg)).to_i
      when 1
        @regB ^= arg
      when 2
        @regB = get_combo_operand(arg) % 8
      when 3
        unless @regA.zero?
          pc = arg
          jump = true
        end
      when 4
        @regB ^= @regC
      when 5
        output << get_combo_operand(arg) % 8
      when 6
        @regB = (@regA / 2**get_combo_operand(arg)).to_i
      when 7
        @regC = (@regA / 2**get_combo_operand(arg)).to_i
      end

      puts instr_to_s(opcode, arg) if log
      print_reg if log
      pc += 2 unless jump
    end
    string ? output.join(',') : output
  end
end
