require_relative 'utils'

ints = File.readlines('input17.txt', chomp: true).map { |line| ints(line) }
computer = Computer.new(ints[-1], ints[0][0], ints[1][0], ints[2][0])
print computer.assemble
print computer.simulate
