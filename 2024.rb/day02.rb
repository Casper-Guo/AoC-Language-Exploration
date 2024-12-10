lines = File.readlines('input02.txt', chomp: true)
lines = lines.map { |line| line.split.map(&:to_i) }

def safety_check(report)
  return 1 if report.length == 1

  increasing = report[0] < report[1]

  report.each_cons(2) do |level1, level2|
    return 0 unless (1..3).include?((level1 - level2).abs)

    return 0 if increasing && level1 > level2
    return 0 if !increasing && level1 < level2
  end
  1
end

def tolerant_safety_check(report)
  return 1 if report.length <= 2 || safety_check(report) == 1

  (0...report.length).each do |i|
    return 1 if safety_check(report[0...i] + report[(i + 1)..]) == 1
  end

  0
end

puts lines.map { |line| safety_check(line) }.sum
puts lines.map { |line| tolerant_safety_check(line) }.sum
