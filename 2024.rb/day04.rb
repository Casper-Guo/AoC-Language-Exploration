# frozen_string_literal: true

require_relative 'utils'

grid = Grid.new(File.readlines('input04.txt', chomp: true).map(&:chars))

delta_row = [-1, 0, 1]
delta_col = [-1, 0, 1]

xmas_count = 0
x_mas_count = 0

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
