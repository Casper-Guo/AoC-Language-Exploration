input = File.read('input19.txt').split("\n\n")
prefixes = input[0].strip.split(', ')
designs = input[1].split("\n")

$num_ways = { '' => 1 }
def count_possible(prefixes, design)
  return $num_ways[design] if $num_ways.include?(design)

  $num_ways[design] = prefixes.sum do |prefix|
    design.start_with?(prefix) ? count_possible(prefixes, design[prefix.length..]) : 0
  end

  $num_ways[design]
end

# populate $num_ways memo
part2 = designs.map { |design| count_possible(prefixes, design) }.sum
puts designs.map { |design| $num_ways[design].zero? ? 0 : 1 }.sum
puts part2
