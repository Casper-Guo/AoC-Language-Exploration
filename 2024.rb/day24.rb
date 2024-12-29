# frozen_string_literal: true

require 'set'

uncomputed = Set.new
values = {}
formulae = {}

file = File.read('input24.txt').split("\n\n")

file[0].split("\n").map { |line| values[line[..2]] = line[-1].to_i }
file[1].split("\n").each do |line|
  gate1, op, gate2, _, gate3 = line.split
  formulae[gate3] = [gate1, op, gate2]
  [gate1, gate2, gate3].each do |gate|
    uncomputed << gate unless values.include?(gate)
  end
end

until uncomputed.empty?
  uncomputed.each do |gate|
    gate1, op, gate2 = formulae[gate]
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

output = 0
values.each do |key, val|
  next unless key.start_with?('z')

  output += (val << key[1..].to_i)
end

puts output

$simplifications = {}
def simplify(gate, formulae)
  return $simplifications[gate] if $simplifications.include?(gate)
  return gate if gate.start_with?('x') || gate.start_with?('y')

  gate1, op, gate2 = formulae[gate]
  # basic cases
  simplification = case formulae[gate].join(' ')
                   when /[x|y](\d{2}) XOR [x|y](\d{2})/
                     raise "#{gate} - Incorrect configuration" if $1 != $2

                     "S#{$1}"
                   when /[x|y](\d{2}) AND [x|y](\d{2})/
                     raise "#{gate} - Incorrect configuration" if $1 != $2

                     $1 == '00' ? "C#{$1}" : "c#{$1}"
                   else
                     "(#{simplify(gate1, formulae)}) #{op} (#{simplify(gate2, formulae)})"
                   end

  # two rules for simplifying gates that output the intermediate value for the carry calculation
  if /\(S(\d{2})\) AND \(C(\d{2})\)/ =~ simplification
    raise "#{gate} - Incorrect configuration" if ($1.to_i - 1) != $2.to_i

    simplification = "s#{$1}"
  end
  if /\(C(\d{2})\) AND \(S(\d{2})\)/ =~ simplification
    raise "#{gate} - Incorrect configuration" if ($1.to_i + 1) != $2.to_i

    simplification = "s#{$2}"
  end

  # rule for simplifying gates that output the final carry value
  if /\(c(\d{2})\) OR \(s(\d{2})\)/ =~ simplification || /\(s(\d{2})\) OR \(c(\d{2})\)/ =~ simplification
    raise "#{gate} - Incorrect configuration" if $1 != $2

    simplification = "C#{$1}"
  end

  $simplifications[gate] = simplification
  simplification
end
