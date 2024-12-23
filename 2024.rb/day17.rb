# frozen_string_literal: true

require_relative 'utils'
require 'set'

ints = File.readlines('input17.txt', chomp: true).map { |line| ints(line) }
computer = Computer.new(ints[-1], ints[0][0], ints[1][0], ints[2][0])
print "#{computer.simulate}\n"

def reverse_search(computer, target, index: 1, current: 0)
  return Set[current] if index > target.length

  current <<= 3
  quines = Set.new
  (0..7).each do |i|
    computer.regA = current + i
    next unless computer.simulate(string: false) == target[-index..]

    quines |= reverse_search(
      computer,
      target,
      index: index + 1,
      current: current + i
    )
  end

  quines
end

puts reverse_search(computer, ints[-1]).min
