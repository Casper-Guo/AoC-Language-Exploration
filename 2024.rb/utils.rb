# Utility class for grids/matrices etc.
# Assumes the input is rectangular

def ints(line)
  line.scan(/\d+/).map(&:to_i)
end

class Grid
  attr_accessor :grid, :num_rows, :num_cols

  @@neighbor_delta = [[1, 0], [-1, 0], [0, 1], [0, -1]]
  @@adj_delta = [[1, 1], [-1, -1], [1, -1], [-1, 1]] + @@neighbor_delta

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
    @grid.to_s
  end

  def inbound?(row, col)
    row.between?(0, @num_rows - 1) && col.between?(0, @num_cols - 1)
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

  def get_direct_neighbors(row, col)
    neighbors = []
    @@neighbor_delta.each do |drow, dcol|
      neighbor = [row + drow, col + dcol]
      neighbors << [neighbor, at(*neighbor)] if inbound?(*neighbor)
    end
    neighbors
  end

  def get_adjacent_neighbors(row, col)
    neighbors = []
    @@adj_delta.each do |drow, dcol|
      neighbor = [row + drow, col + dcol]
      neighbors << [neighbor, at(*neighbor)] if inbound?(*neighbor)
    end
    neighbors
  end
end
