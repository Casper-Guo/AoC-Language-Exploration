# frozen_string_literal: true

require_relative 'utils'

instructions = File.readlines('input21.txt', chomp: true)

# Static class for day 21 numpad layout
class Numpad < Grid
  def initialize
    super([
      %w[7 8 9],
      %w[4 5 6],
      %w[1 2 3],
      [nil, '0', 'A']
    ])
    @index = {}
    coords.each do |coord|
      @index[at(*coord)] = coord
    end
  end

  def find(item)
    @index[item]
  end
end

# Static class for day 21 direction pad layout
class DPad < Grid
  def initialize
    super([
      [nil, '^', 'A'],
      ['<', 'v', '>']
    ])
    @index = {}
    coords.each do |coord|
      @index[at(*coord)] = coord
    end
  end

  def find(item)
    @index[item]
  end
end

NUMPAD = Numpad.new
D_PAD = DPad.new

# translate a instruction to direction pad press sequences
def numpad_to_dpad(instruction, numpad)
  presses = []
  # always starts at A
  current = [3, 2]
  null_row, null_col = [3, 0]

  instruction.each do |button|
    button_coord = numpad.find(button)
    current_row, current_col = current
    button_row, button_col = button_coord
    drow = button_row - current_row
    dcol = button_col - current_col

    # generate moves in the following order: < over v over ^ = > whenever possible
    left_first = !(current_row == null_row && button_col == null_col)
    down_first = !(current_col == null_col && button_row == null_row)

    dcol.abs.times { presses << '<' } if left_first && dcol.negative?
    drow.times { presses << 'v' } if down_first
    dcol.times { presses << '>' }
    drow.abs.times { presses << '^' } if drow.negative?

    # if we were on row 3, must wait for ^ before <
    dcol.abs.times { presses << '<' } if !left_first && dcol.negative?
    # if we were on column 0, must wait for > before v
    drow.times { presses << 'v' } unless down_first

    presses << 'A'
    current = button_coord
  end

  presses
end

def dpad_to_numpad(instruction, numpad)
  presses = []
  # always starts at A
  current = [3, 2]
  instruction.each do |press|
    if press == 'A'
      presses << numpad.at(*current)
      next
    end
    current = numpad.move_one(*current, *CHAR_TO_DELTA[press])
  end

  presses
end

# translate a sequence of direction pad presses to presses on the higher level direction pad
# default to starting at A
def dpad_to_dpad(instruction, d_pad, current: [0, 2])
  presses = []

  instruction.each do |button|
    button_coord = d_pad.find(button)
    current_row, current_col = current
    button_row, button_col = button_coord
    drow = button_row - current_row
    dcol = button_col - current_col

    # generate moves in the following order: < over v over ^ = > whenever possible
    # null button is at [0, 0] so checking for it can be done with zero?
    left_first = !(current_row.zero? && button_col.zero?)

    dcol.abs.times { presses << '<' } if left_first && dcol.negative?
    drow.times { presses << 'v' }
    dcol.times { presses << '>' }

    # if we were on row 0, must wait for v before <
    dcol.abs.times { presses << '<' } if !left_first && dcol.negative?
    drow.abs.times { presses << '^' } if drow.negative?

    presses << 'A'
    current = button_coord
  end

  presses
end

def reverse_dpad_to_dpad(instruction, dpad)
  presses = []
  # always starts at A
  current = [0, 2]
  instruction.each do |press|
    if press == 'A'
      presses << dpad.at(*current)
      next
    end
    current = dpad.move_one(*current, *CHAR_TO_DELTA[press])
  end

  presses
end

# current configures where the arm of robot over the first numpad is aiming
# all other robots still start at A
def get_seq(instruction, d_pad, num_dpads, current: [0, 2])
  instruction = dpad_to_dpad(instruction, d_pad, current: current)
  (num_dpads - 2).times do
    instruction = dpad_to_dpad(instruction, d_pad)
  end
  instruction
end

num_dpads = 3
complexity = 0

instructions.each do |instruction|
  code = ints(instruction)[0]
  instruction = numpad_to_dpad(instruction.chars, NUMPAD)
  complexity += code * get_seq(instruction, D_PAD, num_dpads).length
end

puts complexity

d_keys = ['^', 'A', '<', 'v', '>']
seq_lengths = {}

d_keys.product(d_keys).each do |seq|
  first, second = seq
  start = D_PAD.find(first)
  seq_lengths[seq] = get_seq([second], D_PAD, 14, current: start).length
end

complexity = 0

instructions.each do |instruction|
  code = ints(instruction)[0]
  instruction = numpad_to_dpad(instruction.chars, NUMPAD)
  instruction = ['A'] + get_seq(instruction, D_PAD, 13)
  complexity += code * instruction.each_cons(2).map {|seq| seq_lengths[seq] }.sum
end

puts complexity
