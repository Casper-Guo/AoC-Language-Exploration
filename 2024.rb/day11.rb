require_relative 'utils'

stones = ints(File.read('input11.txt', chomp: true))
stones_freq = Hash.new(0)
stones.map { |stone| stones_freq[stone] += 1 }

def blink(stone)
  if stone.zero?
    [1]
  elsif ((Math.log10(stone).floor + 1) % 2).zero?
    str = stone.to_s
    [str[...str.length / 2], str[str.length / 2..]].map(&:to_i)
  else
    [stone * 2024]
  end
end

def blink_all(stones_freq)
  new_freq = Hash.new(0)
  stones_freq.each_pair do |stone, freq|
    blink(stone).map { |new_stone| new_freq[new_stone] += freq }
  end
  new_freq
end

25.times do
  stones_freq = blink_all(stones_freq)
end
puts stones_freq.values.sum


50.times do
  stones_freq = blink_all(stones_freq)
end
puts stones_freq.values.sum
