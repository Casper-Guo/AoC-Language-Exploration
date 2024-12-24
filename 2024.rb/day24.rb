# frozen_string_literal: true

require 'set'

uncomputed = Set.new
values = {}
formulae = {}

file = File.read('input24.txt').split("\n\n")

file[0].split("\n").map { |line| values[line[..2]] = line[-1].to_i }
file[1].split("\n").each do |line|
  gate1, op, gate2, _, gate3 = line.split
  formulae[gate3] = [gate1, gate2, op]
  [gate1, gate2, gate3].each do |gate|
    uncomputed << gate unless values.include?(gate)
  end
end

until uncomputed.empty?
  uncomputed.each do |gate|
    gate1, gate2, op = formulae[gate]
    next unless values.include?(gate1) && values.include?(gate2)

    case op
    when 'AND'
      values[gate] = values[gate1] & values[gate2]
    when 'XOR'
      values[gate] = values[gate1] ^ values[gate2]
    when 'OR'
      values[gate] = values[gate1] | values[gate2]
    end
    uncomputed.delete(gate)
  end
end

checksum = 0
values.each do |key, val|
  next unless key.start_with?('z')

  checksum += (val << key[1..].to_i)
end

def backtrack(gate, formulae)
  return gate if gate.start_with?('x') || gate.start_with?('y')

  gate1, gate2, op = formulae[gate]
  "(#{backtrack(gate1, formulae)}) #{op} (#{backtrack(gate2, formulae)})"
end

puts checksum
puts backtrack('z02', formulae)
