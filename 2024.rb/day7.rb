require_relative 'utils'
require 'set'

equations = File.readlines('input7.txt').map { |line| ints(line) }

def solve_part1(equation)
  target = equation[0]
  results = Set[equation[1]]

  equation[2...equation.length].each do |num|
    add = results.map { |result| result + num }
    mul = results.map { |result| result * num }
    results = (add + mul).to_set
  end
  results.include?(target) ? target : 0
end

def solve_part2(equation)
  target = equation[0]
  results = Set[equation[1]]

  equation[2...equation.length].each do |num|
    add = results.map { |result| result + num }
    mul = results.map { |result| result * num }
    combine = results.map { |result| result * 10**(Math.log10(num).floor + 1) + num }
    results = (add + mul + combine).to_set
  end
  results.include?(target) ? target : 0
end

puts equations.map { |equation| solve_part1(equation) }.sum
puts equations.map { |equation| solve_part2(equation) }.sum
