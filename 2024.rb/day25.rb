# frozen_string_literal: true

require_relative 'utils'

schematics = File.read('input25.txt').split("\n\n")
locks = []
keys = []

schematics.each do |schema|
  grid = Grid.new(schema.split("\n").map(&:chars))
  schema_number = 0
  (0...grid.num_cols).each_with_index do |col, col_index|
    # least significant three bits is first column
    schema_number += ((grid.get_col(col).count('#') - 1) << (col_index * 3))
  end
  if grid[[0, 0]] == '#'
    locks << schema_number
  else
    keys << schema_number
  end
end

def check_match(lock, key)
  (0...5).each do |col|
    # deal with trailing zero bits by lshift 5 the same amount
    return 0 if ((lock & (0b111 << (col * 3))) + (key & (0b111 << (col * 3)))) > (5 << (col * 3))
  end
  1
end

puts locks.product(keys).map { |lock, key| check_match(lock, key) }.sum
