file = File.read('input3.txt')
matches1 = file.scan(/mul\(([0-9]{1,3}),([0-9]{1,3})\)/)
result1 = 0

matches1.each do |match|
  result1 += match.map(&:to_i).inject(&:*)
end

result2 = 0
matches2 = file.scan(/do\(\)|don't\(\)|mul\([0-9]{1,3},[0-9]{1,3}\)/)
enabled = true
matches2.each do |match|
  case match
  when /do\(\)/
    enabled = true
  when /don't\(\)/
    enabled = false
  else
    # guarenteed that there is only to be one match
    # so access the first element
    result2 += enabled ? match.scan(/mul\(([0-9]{1,3}),([0-9]{1,3})\)/)[0].map(&:to_i).inject(&:*) : 0
  end
end

puts result1
puts result2
