lines = File.readlines('input1.txt', chomp: true)
list1 = []
list2 = []
freq = Hash.new(0)

lines.each do |line|
  ids = line.split.map(&:to_i)
  list1 << ids[0]
  list2 << ids[1]
  freq[ids[1]] += 1
end

list1.sort!
list2.sort!

distance = 0
similarity = 0
list1.zip(list2).each do |id1, id2|
  distance += (id1 - id2).abs
  similarity += id1 * freq[id1]
end

puts distance, similarity
