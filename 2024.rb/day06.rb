require_relative 'utils'
require 'set'

$grid = Grid.new(File.readlines('input6.txt', chomp: true).map(&:chars))
$visited = {}
$directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
direction_index = 0
start_coord = $grid.find('^')[0]
current_coord = $grid.find('^')[0]
obstructions = Set.new

def move_once(current_coord, direction_index)
  current_row, current_col = current_coord
  next_row = current_row + $directions[direction_index][0]
  next_col = current_col + $directions[direction_index][1]

  while $grid.at(next_row, next_col) == '#'
    direction_index = (direction_index + 1) % 4
    next_row = current_row + $directions[direction_index][0]
    next_col = current_col + $directions[direction_index][1]
  end

  [[next_row, next_col], direction_index]
end

def detect_cycle(current_coord, direction_index)
  path = {}
  while $grid.inbound?(*current_coord)
    next_coord, direction_index = move_once(current_coord, direction_index)
    return true if $visited[current_coord]&.include?(direction_index) || path[current_coord]&.include?(direction_index)

    (path[current_coord] ||= Set.new) << direction_index
    current_coord = next_coord
  end
  false
end

while $grid.inbound?(*current_coord)
  next_coord, direction_index = move_once(current_coord, direction_index)
  ($visited[current_coord] ||= Set.new) << direction_index

  # if the next coordinate has been visited before
  # then we must have tried using it as an obstruction already
  if !$visited.key?(next_coord) && $grid.inbound?(*next_coord)
    original = $grid[next_coord]
    $grid[next_coord] = '#'
    obstructions << next_coord if detect_cycle(current_coord, direction_index)
    $grid[next_coord] = original
  end
  current_coord = next_coord
end

puts $visited.length
puts obstructions.include?(start_coord) ? obstructions.length - 1 : obstructions.length
