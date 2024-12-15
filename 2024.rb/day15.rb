require_relative 'utils'
require 'set'

grid, instructions = File.read('input15.txt').split("\n\n")
instructions = instructions.gsub("\n", '').chars
grid_part1 = Grid.new(grid.split("\n").map(&:chars))

grid_part2 = []
grid_part1.grid.each do |row|
  row_part2 = []
  row.each do |char|
    case char
    when '#'
      row_part2 << '#' << '#'
    when 'O'
      row_part2 << '[' << ']'
    when '.'
      row_part2 << '.' << '.'
    when '@'
      row_part2 << '@' << '.'
    end
  end
  grid_part2 << row_part2
end
grid_part2 = Grid.new(grid_part2)

def gps_sum(grid, box)
  grid.coords.map { |row, col| grid.at(row, col) == box ? 100 * row + col : 0 }.sum
end

# if the box can be pushed, modify the grid and return true
# else, return false
# coord is the coordinate of the first box getting pushed
def push_box_part1(grid, box_coord, move)
  current_coord = box_coord
  # first coordinate after the sequence of boxes
  current_coord = grid.move_one(*current_coord, *move) while grid.at(*current_coord) == 'O'
  case grid.at(*current_coord)
  when '.'
    grid[current_coord] = 'O'
    grid[box_coord] = '.'
    true
  when '#'
    false
  end
end

def push_horizontal_boxes(grid, box_coord, move)
  current_coord = box_coord
  boxes = []
  box_edge = grid.at(*box_coord)
  while grid.at(*current_coord) == box_edge
    # collect boxes
    boxes << current_coord << grid.move_one(*current_coord, *move)
    current_coord = grid.move_n(*current_coord, *move, 2)
  end

  case grid.at(*current_coord)
  when '.'
    # update boxes locations
    (boxes + [current_coord]).reverse.each_cons(2) do |to, from|
      grid[to] = grid[from]
    end
    grid[box_coord] = '.'
    true
  when '#'
    false
  end
end

# find the other edge of the box
def augment_box(grid, coord)
  row, col = coord
  if grid.at(row, col) == ']'
    [row, col - 1]
  elsif grid.at(row, col) == '['
    [row, col + 1]
  end
end

def collect_vertical_boxes(grid, box_coord, move)
  boxes = Set.new
  current_row = Set.new([box_coord, augment_box(grid, box_coord)])

  until current_row.empty?
    next_row = Set.new
    current_row.each do |coord|
      next_coord = grid.move_one(*coord, *move)

      case grid.at(*next_coord)
      when '#'
        # one of the boxes is against the wall
        # this push is invalid
        return false
      when '[', ']'
        next_row << next_coord << augment_box(grid, next_coord)
      end
    end

    boxes |= current_row
    current_row = next_row
  end
  boxes
end

# assumes that the move is either up or down
# and that the push is valid
def shift_boxes(grid, boxes, move)
  # take advantage of the fact that Ruby set maintains insertion order
  # e.g. when we are pushing down, we want to modify lowest row first
  # these will be inserted at the end
  boxes.reverse_each do |from|
    to = grid.move_one(*from, *move)
    grid[to] = grid[from]
    grid[from] = '.'
  end
end

def push_box_part2(grid, box_coord, move)
  return push_horizontal_boxes(grid, box_coord, move) if [[0, 1], [0, -1]].include?(move)

  boxes = collect_vertical_boxes(grid, box_coord, move)
  return false unless boxes

  shift_boxes(grid, boxes, move)
  true
end

current_part1 = grid_part1.find('@')[0]
current_part2 = grid_part2.find('@')[0]
instructions.each do |instruction|
  move = CHAR_TO_DELTA[instruction]

  next_part1 = grid_part1.move_one(*current_part1, *move)
  grid_part1[current_part1] = '.'
  case grid_part1.at(*next_part1)
  when '.'
    current_part1 = next_part1
  when 'O'
    current_part1 = next_part1 if push_box_part1(grid_part1, next_part1, move)
  end
  grid_part1[current_part1] = '@'

  next_part2 = grid_part2.move_one(*current_part2, *move)
  grid_part2[current_part2] = '.'
  case grid_part2.at(*next_part2)
  when '.'
    current_part2 = next_part2
  when '[', ']'
    current_part2 = next_part2 if push_box_part2(grid_part2, next_part2, move)
  end
  grid_part2[current_part2] = '@'
end

puts gps_sum(grid_part1, 'O')
puts gps_sum(grid_part2, '[')
