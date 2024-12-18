require_relative 'utils'
require 'set'
require 'pairing_heap'

failures = File.readlines('input18.txt', chomp: true).map { |line| ints(line) }

def setup_grid(width, height: nil, fill: '.')
  height = width if height.nil?
  # this is clunky but avoids Ruby making array copies while referencing
  # the same underlying array
  grid = []
  height.times { grid << [fill] * width }
  Grid.new(grid)
end

def corrupt_grid(grid, failures, num_failures, fail_fill: '#')
  failures[...num_failures].each do |failure|
    # need to reverse because X coordinate is first
    grid[failure.reverse] = fail_fill
  end
end

def A_star(grid, start, finish)
  discovered = PairingHeap::MinPriorityQueue.new
  discovered.push(start, grid.manhattan(*start, *finish))

  prev = {}
  known_cost = Hash.new(2**64 - 1)
  known_cost[start] = 0

  while discovered.any?
    current = discovered.pop
    return [prev, known_cost] if current == finish

    grid.get_direct_neighbors(*current).each do |next_coord, element|
      cost = known_cost[current] + 1
      next if element == '#' || cost >= known_cost[next_coord]

      prev[next_coord] = current
      known_cost[next_coord] = cost

      begin
        discovered.push(next_coord, cost + grid.manhattan(*next_coord, *finish))
      rescue ArgumentError # if key is already in the PQ
        discovered.decrease_key(next_coord, cost + grid.manhattan(*next_coord, *finish))
      end
    end
  end
  raise 'No path available!'
end

# draw the least cost path onto the grid
def show_path(grid, prev, start, finish)
  current = finish
  grid[finish] = 'O'

  until current == start
    previous = prev[current]
    grid[previous] = 'O'
    current = previous
  end
  grid
end

def binary_search(failures, width, height: nil, left: nil, right: nil)
  height = width if height.nil?
  left = 0 if left.nil?
  right = failures.length if right.nil?

  grid = setup_grid(width, height: height)
  start = [0, 0]
  finish = [grid.num_rows - 1, grid.num_cols - 1]

  return left if left == right

  middle = (left + right) / 2
  begin
    corrupt_grid(grid, failures, middle)
    A_star(grid, start, finish)
    return binary_search(failures, width, height: height, left: middle + 1, right: right)
  rescue RuntimeError
    return binary_search(failures, width, height: height, left: left, right: middle - 1)
  end
  -1
end

dim = 71
num_failures = 1024
grid = setup_grid(dim)
corrupt_grid(grid, failures, num_failures)
start = [0, 0]
finish = [grid.num_rows - 1, grid.num_cols - 1]
_, cost = A_star(grid, start, finish)
min_length = cost[finish]
puts min_length
blocker_index = binary_search(failures, dim, left: num_failures) - 1
print failures[blocker_index]
