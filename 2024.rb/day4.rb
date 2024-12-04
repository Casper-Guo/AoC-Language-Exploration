lines = File.readlines('input4.txt', chomp: true)
lines = lines.map(&:chars)

# Utility class for grids/matrices etc.
# Assumes the input is rectangular
class Grid
  attr_accessor :num_rows, :num_cols

  def initialize(grid)
    @grid = grid
    @num_rows = grid.length
    @num_cols = grid[0].length
  end

  def check_inbound(row, col)
    row.between?(0, @num_rows - 1) && col.between?(0, @num_cols - 1)
  end

  def at(row, col)
    check_inbound(row, col) ? @grid[row][col] : nil
  end
end

delta_row = [-1, 0, 1]
delta_col = [-1, 0, 1]

xmas_count = 0
x_mas_count = 0
grid = Grid.new(lines)

(0...grid.num_rows).each do |row|
  (0...grid.num_cols).each do |col|
    if grid.at(row, col) == 'X'
      delta_row.each do |drow|
        delta_col.each do |dcol|
          next if drow.zero? && dcol.zero?

          string = (0...4).map { |i| grid.at(row + i * drow, col + i * dcol) }.join
          xmas_count += 1 if string == 'XMAS'
        end
      end
    elsif grid.at(row, col) == 'A'
      diag1 = (-1..1).map { |i| grid.at(row + i, col + i) }.join
      diag2 = (-1..1).map { |i| grid.at(row + i, col - i) }.join

      x_mas_count += 1 if (diag1 == 'MAS' || diag1.reverse == 'MAS') && (diag2 == 'MAS' || diag2.reverse == 'MAS')
    end
  end
end

puts xmas_count, x_mas_count
