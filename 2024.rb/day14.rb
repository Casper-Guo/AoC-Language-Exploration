# frozen_string_literal: true

require_relative 'utils'
require 'set'

robots = File.readlines('input14.txt', chomp: true).map { |line| ints(line) }
width = 101
height = 103
iter = 100

def get_position(robot, width, height, iter)
  p0, p1, v0, v1 = robot
  [(p0 + iter * v0) % width, (p1 + iter * v1) % height]
end

# quadrants numbered as follows
# 0 1
# 2 3
def safety_factor(positions, width, height)
  quadrant_count = [0] * 4
  positions.each do |position|
    p0, p1 = position
    next if p0 == width / 2 || p1 == height / 2

    if p0 < width / 2
      quadrant_count[p1 < height / 2 ? 0 : 2] += 1
    else
      quadrant_count[p1 < height / 2 ? 1 : 3] += 1
    end
  end
  quadrant_count.inject(:*)
end

def display(robots, width, height, iter)
  puts iter
  positions = Set.new(robots.map { |robot| get_position(robot, width, height, iter) })

  height.times do |p0|
    width.times do |p1|
      print positions.include?([p0, p1]) ? '#' : '.'
    end
    print "\n"
  end
end

positions = robots.map { |robot| get_position(robot, width, height, iter) }
puts safety_factor(positions, width, height)

display(robots, width, height, 7037)
