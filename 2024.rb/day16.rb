require_relative 'utils'
require 'set'
require 'pairing_heap'

NEIGHBOR_DELTA = [[-1, 0], [0, 1], [1, 0], [0, -1]].freeze
grid = Grid.new(File.readlines('input16.txt', chomp: true).map(&:chars))
start = grid.find('S')[0]
finish = grid.find('E')[0]

def get_neighbors(grid, coord)
  neighbors = []
  NEIGHBOR_DELTA.each do |delta|
    next_coord = grid.move_one(*coord, *delta)
    # can get rid of the inbound? check becauase of the boundary of walls
    neighbors << [next_coord, delta] if grid.at(*next_coord) != '#'
  end
  neighbors
end

def A_star(grid, start, finish)
  discovered = PairingHeap::MinPriorityQueue.new
  discovered.push([start, [0, 1]], grid.manhattan(*start, *finish))

  prev = {}
  known_cost = Hash.new(2**64 - 1)
  known_cost[[start, [0, 1]]] = 0

  while discovered.any?
    current, from_direction = discovered.pop
    return [prev, known_cost] if current == finish

    get_neighbors(grid, current).each do |next_coord, to_direction|
      cost = known_cost[[current, from_direction]] + (from_direction == to_direction ? 1 : 1001)
      next unless cost < known_cost[[next_coord, to_direction]]

      prev[[next_coord, to_direction]] = [current, from_direction]
      known_cost[[next_coord, to_direction]] = cost

      begin
        discovered.push([next_coord, to_direction], cost + grid.manhattan(*next_coord, *finish))
      rescue ArgumentError # if key is already in the PQ
        discovered.decrease_key([next_coord, to_direction], cost + grid.manhattan(*next_coord, *finish))
      end
    end
  end
  raise 'Cannot find path'
end

# draw the least cost path onto the grid
# todo: fix
# def show_path(grid, prev, start, finish)
#   current = finish

#   until current == start
#     previous = prev[current]
#     direction = DELTA_TO_CHAR[grid.get_direction(*previous, *current)]
#     grid[previous] = direction
#     current = previous
#     print current, "\n"
#   end
#   grid
# end

_, cost = A_star(grid, start, finish)
puts cost.keep_if { |key, _| key[0] == finish }.map { |_, val| val }.min
