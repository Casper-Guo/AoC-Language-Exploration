# Utility class for grids/matrices etc.
# Assumes the input is rectangular
class Grid
  attr_accessor :grid, :num_rows, :num_cols

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
    "#{@grid}"
  end

  def check_inbound(row, col)
    row.between?(0, @num_rows - 1) && col.between?(0, @num_cols - 1)
  end

  def at(row, col)
    check_inbound(row, col) ? @grid[row][col] : nil
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
end