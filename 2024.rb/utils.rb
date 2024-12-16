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
