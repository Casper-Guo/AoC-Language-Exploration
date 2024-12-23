# frozen_string_literal: true

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

  # part1
  # prev = {}
  # part 2
  prev = Hash.new(Set.new)

  known_cost = Hash.new(2**64 - 1)
  known_cost[[start, [0, 1]]] = 0

  while discovered.any?
    current, from_direction = discovered.pop
    return [prev, known_cost] if current == finish

    get_neighbors(grid, current).each do |next_coord, to_direction|
      cost = known_cost[[current, from_direction]] + (from_direction == to_direction ? 1 : 1001)

      # part 1
      next if cost >= known_cost[[next_coord, to_direction]]
      # part 2
      next if cost > known_cost[[next_coord, to_direction]]

      # part 1
      # prev[[next_coord, to_direction]] = [current, from_direction]
      # part 2
      prev[[next_coord, to_direction]] = if cost < known_cost[[next_coord, to_direction]]
                                           Set[[current, from_direction]]
                                         else
                                           prev[[next_coord, to_direction]] << [current, from_direction]
                                         end

      known_cost[[next_coord, to_direction]] = cost

      begin
        discovered.push([next_coord, to_direction], cost + grid.manhattan(*next_coord, *finish))
      rescue ArgumentError # if key is already in the PQ
        discovered.decrease_key([next_coord, to_direction], cost + grid.manhattan(*next_coord, *finish))
      end
    end
  end
end

# draw the least cost path onto the grid
# only compatible with part 1 version of A*
def show_path(grid, prev, start, finish)
  # each key is a coordinate, direction tuple
  current = finish

  until current[0] == start
    previous = prev[current]
    # current[1] is the direction taken from previous[0] to current[0]
    grid[previous[0]] = DELTA_TO_CHAR[current[1]]
    current = previous
  end
  grid
end

def backtrack(grid, prev, start, finish)
  visited = Set.new
  return Set[start] if finish[0] == start

  visited << finish[0]
  prev[finish].each do |previous|
    visited |= backtrack(grid, prev, start, previous)
  end

  visited
end

prev, cost = A_star(grid, start, finish)
final_key, min_cost = cost.filter { |key, _| key[0] == finish }.to_a[0]
puts min_cost
puts backtrack(grid, prev, start, final_key).size
