# frozen_string_literal: true

require 'set'

edges = File.readlines('input23.txt', chomp: true).map { |line| line.split('-') }
adjacency_matrix = Hash.new { |h, key| h[key] = Set.new }
t_vertices = Set.new

edges.each do |edge|
  v1, v2 = edge
  t_vertices << v1 if v1.start_with?('t')
  t_vertices << v2 if v2.start_with?('t')

  adjacency_matrix[v1] <<= v2
  adjacency_matrix[v2] <<= v1
end

triangles = Set.new
edges.each do |edge|
  v1, v2 = edge
  shared = adjacency_matrix[v1] & adjacency_matrix[v2]
  shared.each do |v3|
    vertices = [v1, v2, v3]
    triangles << Set.new(vertices) if vertices.any? { |vertex| t_vertices.include?(vertex) }
  end
end

puts triangles.length
