# frozen_string_literal: true

require_relative 'utils'

# x1, y1, x2, y2, target_x, target_y in order
machines = File.read('input13.txt').split("\n\n").map { |machine| ints(machine) }

def validate_solution(sol_x, sol_y, part2: false)
  tol = 0.001
  int_x = sol_x.round
  int_y = sol_y.round
  return 0 unless (sol_x - int_x).abs < tol && (sol_y - int_y).abs < tol

  return (3 * int_x + int_y) if part2

  int_x.between?(0, 100) && int_y.between?(0, 100) ? 3 * int_x + int_y : 0
end

def matrix_inverse(machine, part2: false)
  if part2
    machine[4] += 10_000_000_000_000
    machine[5] += 10_000_000_000_000
  end

  det = (machine[0] * machine[3] - machine[1] * machine[2]).to_f
  return 0 if det.zero?

  sol_x = (1 / det) * (machine[4] * machine[3] - machine[5] * machine[2])
  sol_y = (1 / det) * (machine[4] * -machine[1] + machine[5] * machine[0])
  validate_solution(sol_x, sol_y, part2: part2)
end

puts machines.map { |machine| matrix_inverse(machine) }.sum
puts machines.map { |machine| matrix_inverse(machine, part2: true) }.sum
