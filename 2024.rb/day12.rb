# frozen_string_literal: true

require_relative 'utils'
require 'set'

grid = Grid.new(File.readlines('input12.txt', chomp: true).map(&:chars))
visited = Set.new

# Number of corners equal number of sides
def calc_price(grid, current_coord)
  area = 0
  total_perimeter = 0
  total_sides = 0
  plot_type = grid.at(*current_coord)
  plot_coords = Set.new
  to_visit = [current_coord]

  until to_visit.empty?
    current_coord = to_visit.pop
    next if plot_coords.include?(current_coord)

    area += 1
    plot_coords << current_coord
    neighbors = grid.get_direct_neighbors(*current_coord, all: true)

    # 1 for non-matching neighbors, and vice versa
    # perimeter length of this grid is the number of non-matching neighbors (including boundary)
    total_perimeter += neighbors.map { |_, neighbor_plant| neighbor_plant == plot_type ? 0 : 1 }.sum

    neighbors.each do |neighbor_coord, plant_type|
      to_visit << neighbor_coord if plant_type == plot_type
    end
    total_sides += calc_corners(grid, current_coord, plot_type)
  end

  [area * total_perimeter, area * total_sides, plot_coords]
end

def calc_corners(grid, coord, plot_type)
  # 1 for matching neighbors, and vice versa
  direct_neighbors = grid.get_direct_neighbors(*coord, all: true).map do |_, neighbor_plant|
    neighbor_plant == plot_type ? 1 : 0
  end
  adj_neighbors = grid.get_adjacent_neighbors(*coord, all: true).map do |_, neighbor_plant|
    neighbor_plant == plot_type ? 1 : 0
  end

  case direct_neighbors.sum
  when 0
    4 # no matching neighbors, so has all 4 corners
  when 1
    2 # one matching neighbor, so 2 corners
  when 2
    case direct_neighbors
    when [0, 0, 1, 1]
      2 - adj_neighbors[5] # SW may be corner
    when [1, 0, 0, 1]
      2 - adj_neighbors[7] # NW may be corner
    when [1, 1, 0, 0]
      2 - adj_neighbors[1] # NE may be corner
    when [0, 1, 1, 0]
      2 - adj_neighbors[3] # SE may be corner
    else # opposite neighbors, no corners
      0
    end
  when 3
    case direct_neighbors
    when [1, 1, 1, 0]
      2 - (adj_neighbors[1] + adj_neighbors[3]) # NE and SE may be corners
    when [1, 1, 0, 1]
      2 - (adj_neighbors[1] + adj_neighbors[7]) # NW and NE may be corners
    when [1, 0, 1, 1]
      2 - (adj_neighbors[5] + adj_neighbors[7]) # NW and SW may be corners
    when [0, 1, 1, 1]
      2 - (adj_neighbors[3] + adj_neighbors[5]) # SW and SE may be corners
    end
  when 4
    8 - adj_neighbors.sum # four matching neighbors, any diagonal neighbor that is non-matching produces a corner
  end
end

total_price = 0
total_discounted_price = 0
grid.coords.each do |coord|
  next if visited.include?(coord)

  price, discounted_price, plot_coords = calc_price(grid, coord)
  total_price += price
  total_discounted_price += discounted_price
  visited |= plot_coords
end

puts total_price, total_discounted_price
