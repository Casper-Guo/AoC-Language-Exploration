file = File.read('input3.txt')
result1 = file.scan(/mul\(([0-9]{1,3}),([0-9]{1,3})\)/).sum { |num1, num2| num1.to_i * num2.to_i }

cleaned = file.gsub(/don't\(\).*?do\(\)/m, '')
result2 = cleaned.scan(/mul\(([0-9]{1,3}),([0-9]{1,3})\)/).sum { |num1, num2| num1.to_i * num2.to_i }

puts result1
puts result2
