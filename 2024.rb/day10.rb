# frozen_string_literal: true

require_relative 'utils'
require 'set'

grid = Grid.new(File.readlines('input10.txt', chomp: true).map { |line| line.chars.map(&:to_i) })
$trailhead_scores = {}
$trailhead_ratings = Hash.new(0)

def backtrack(grid, start_coord, current_coord)
  if grid.at(*current_coord).zero?
    ($trailhead_scores[current_coord] ||= Set.new) << start_coord
    $trailhead_ratings[current_coord] += 1
    return
  end

  grid.get_direct_neighbors(*current_coord).each do |next_coord, next_height|
    backtrack(grid, start_coord, next_coord) if next_height == grid.at(*current_coord) - 1
  end
end

grid.coords.each do |coord|
  backtrack(grid, coord, coord) if grid.at(*coord) == 9
end

puts $trailhead_scores.values.map(&:length).sum
puts $trailhead_ratings.values.sum
