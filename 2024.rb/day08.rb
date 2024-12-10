require_relative 'utils'
require 'set'

# return a 3D array containing the part1 antinodes and part2 antinodes
def analyze_freq(grid, freq)
  antennas = grid.find(freq)
  antinodes_part1 = []
  antinodes_part2 = []

  antennas.combination(2).each do |antenna1, antenna2|
    antinodes_part1 += analyze_antennas_part1(grid, antenna1, antenna2)
    antinodes_part2 += analyze_antennas_part2(grid, antenna1, antenna2)
  end

  [antinodes_part1, antinodes_part2]
end

# return a 2D array of up to 2 coordinates
def analyze_antennas_part1(grid, antenna1, antenna2)
  row1, col1 = antenna1
  row2, col2 = antenna2
  drow = row2 - row1
  dcol = col2 - col1
  antinode1 = [row2 + drow, col2 + dcol]
  antinode2 = [row1 - drow, col1 - dcol]

  [antinode1, antinode2].keep_if { |antinode| grid.inbound?(*antinode) }
end

# return a 2D array of coordinates
def analyze_antennas_part2(grid, antenna1, antenna2)
  row1, col1 = antenna1
  row2, col2 = antenna2
  drow = row2 - row1
  dcol = col2 - col1
  antinodes = []

  multiplier = 0
  while grid.inbound?(row2 + drow * multiplier, col2 + dcol * multiplier)
    antinodes << [row2 + drow * multiplier, col2 + dcol * multiplier]
    multiplier += 1
  end

  multiplier = 1
  while grid.inbound?(row2 - drow * multiplier, col2 - dcol * multiplier)
    antinodes << [row2 - drow * multiplier, col2 - dcol * multiplier]
    multiplier += 1
  end

  antinodes
end

freqs = Set.new(File.read('input08.txt').chars) - ['.', "\n"]
grid = Grid.new(File.readlines('input08.txt', chomp: true).map(&:chars))

# this is a 4D array!
freq_antinodes = freqs.map { |freq| analyze_freq(grid, freq) }

# extract the part 1 solutions
# and flatten one level so we can collect all the antinodes for different frequencies
antinodes_part1 = Set.new(freq_antinodes.map { |freq| freq[0] }.flatten(1))
antinodes_part2 = Set.new(freq_antinodes.map { |freq| freq[1] }.flatten(1))

puts antinodes_part1.length, antinodes_part2.length
