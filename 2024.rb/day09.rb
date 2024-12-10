disk_map = File.read('input09.txt').chomp
blocks = []
file_sizes = {}
file_index = {}
file_id = 0
current_index = 0
file = true
disk_map.chars.each do |char|
  size = char.to_i
  blocks += file ? [file_id] * size : [nil] * size

  if file
    file_sizes[file_id] = size
    file_index[file_id] = current_index
    file_id += 1
  end

  current_index += size
  file = !file
end

def checksum(blocks)
  checksum = 0
  blocks.each_with_index do |block, index|
    checksum += block * index unless block.nil?
  end
  checksum
end

def move_part1(blocks)
  left = 0
  right = blocks.length - 1

  while left < right
    if !blocks[left].nil?
      left += 1
    elsif blocks[right].nil?
      right -= 1
    else
      blocks[left] = blocks[right]
      blocks[right] = nil
    end
  end

  blocks
end

def move_part2(blocks, file_sizes, file_index)
  start_search = Hash.new(0)
  file_sizes.reverse_each do |file_id, size|
    (start_search[size]...file_index[file_id]).each do |window_start|
      next unless blocks[window_start...window_start + size].all?(&:nil?)

      start_search[size] = window_start + size
      (0...size).each do |offset|
        blocks[window_start + offset] = file_id
        blocks[file_index[file_id] + offset] = nil
      end
      break
    end
  end
  blocks
end

puts checksum(move_part1(blocks.clone))
puts checksum(move_part2(blocks.clone, file_sizes, file_index))
