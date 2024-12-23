# frozen_string_literal: true

require 'set'

def check_order(update, rules)
  update.each_cons(2) do |i, j|
    return false if rules[i].nil? || !rules[i].include?(j)
  end
  true
end

def fix_update(update, rules)
  update.sort { |a, b| !rules[a].nil? && rules[a].include?(b) ? 1 : -1 }
end

sections = File.read('input05.txt').split("\n\n").map { |section| section.split("\n") }
parsed_rules = sections[0].map { |rule| rule.split('|') }
updates = sections[1].map { |update| update.split(',') }
rules = {}

parsed_rules.each do |first, second|
  (rules[first] ||= Set.new) << second
end

puts updates.map { |update| check_order(update, rules) ? update[update.length.fdiv(2)].to_i : 0 }.sum
puts updates.map { |update|
  if check_order(update, rules)
    0
  else
    fixed = fix_update(update, rules)
    fixed[fixed.length.fdiv(2)].to_i
  end
}.sum
