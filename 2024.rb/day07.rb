require_relative 'utils'

equations = File.readlines('input07.txt').map { |line| ints(line) }

def solve_part1(equation)
  target = equation[0]
  results = [equation[1]]

  equation[2...equation.length].each do |num|
    add = results.map { |result| result + num }
    mul = results.map { |result| result * num }
    results = add + mul
  end
  results.include?(target) ? target : 0
end

def solve_part2(equation)
  target = equation[0]
  results = [equation[1]]

  equation[2...equation.length].each do |num|
    add = results.map { |result| result + num }
    mul = results.map { |result| result * num }
    combine = results.map { |result| result * 10**(Math.log10(num).floor + 1) + num }
    results = add + mul + combine
  end
  results.include?(target) ? target : 0
end

puts equations.map { |equation| solve_part1(equation) }.sum
puts equations.map { |equation| solve_part2(equation) }.sum
