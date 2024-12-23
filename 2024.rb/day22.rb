# frozen_string_literal: true

require 'set'

seeds = File.readlines('input22.txt', chomp: true).map(&:to_i)
sales = Hash.new(0)
secret_sum = 0

def next_secret(secret)
  secret = (secret ^ (secret << 6)) & 0xFFFFFF
  secret = (secret ^ (secret >> 5)) & 0xFFFFFF
  (secret ^ (secret << 11)) & 0xFFFFFF
end

seeds.each do |seed|
  seen = Set.new
  diffs = 0

  4.times do
    old_price = seed % 10
    seed = next_secret(seed)
    new_price = seed % 10
    # adjust range from (-9, 9) to (0, 18)
    diffs = (diffs << 5) + (new_price - old_price + 9)
  end

  seen << diffs
  sales[diffs] += seed % 10

  1996.times do
    old_price = seed % 10
    seed = next_secret(seed)
    new_price = seed % 10

    # take lowest 15 bits
    diffs = ((diffs & 0x7FFF) << 5) + (new_price - old_price + 9)
    sales[diffs] += new_price unless seen.include?(diffs)
    seen << diffs
  end
  secret_sum += seed
end

puts secret_sum
puts sales.values.max
