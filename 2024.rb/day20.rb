require_relative 'utils'
require 'set'

grid = Grid.new(File.readlines('input20.txt', chomp: true).map(&:chars))
start = grid.find('S')[0]
finish = grid.find('E')[0]

def dfs(grid, start, finish)
  path = [start]
  current = path[-1]
  visited = Set[start]

  until current == finish
    grid.get_direct_neighbors(*current).each do |coord, content|
      return path << coord if content == 'E'
      next if content != '.' || visited.include?(coord)

      path << coord
      visited << coord
    end
    current = path[-1]
  end
end

def find_cheats(grid, path, min_saving, max_duration)
  cheats = Hash.new(0)

  path.each_with_index do |coord1, index1|
    index2 = index1 + 1
    until index2 >= path.length
      coord2 = path[index2]
      dist = grid.manhattan(*coord1, *coord2)
      if dist > max_duration
        # each move changes the distance by at most one
        # so if the current distance is larger than the max cheat duration and the gap is x
        # we can just skip to x moves later and begin checking there
        index2 += dist - max_duration
        next
      end

      saving = index2 - index1 - dist
      index2 += 1
      cheats[saving] += 1 unless saving < min_saving

    end
  end
  cheats
end

path = dfs(grid, start, finish)
puts find_cheats(grid, path, 100, 2).values.sum
puts find_cheats(grid, path, 100, 20).values.sum
