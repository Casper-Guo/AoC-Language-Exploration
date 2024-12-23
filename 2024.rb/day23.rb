# frozen_string_literal: true

require 'set'

edges = File.readlines('input23.txt', chomp: true).map { |line| line.split('-') }
adjacency_matrix = Hash.new { |h, key| h[key] = Set.new }
vertices = Set.new
t_vertices = Set.new

edges.each do |edge|
  v1, v2 = edge
  vertices << v1 << v2
  t_vertices << v1 if v1.start_with?('t')
  t_vertices << v2 if v2.start_with?('t')

  adjacency_matrix[v1] <<= v2
  adjacency_matrix[v2] <<= v1
end

$maximal_cliques = []
def Bron_Kerbosch(r, p, x, neighbors, max_clique_size) # rubocop:disable Naming/MethodParameterName
  if p.empty? && x.empty?
    $maximal_cliques << r if r.length > max_clique_size
    return r.length
  end

  p.each do |v|
    max_clique_size = [
      Bron_Kerbosch(
        r + [v],
        p & neighbors[v],
        x & neighbors[v],
        neighbors,
        max_clique_size
      ),
      max_clique_size
    ].max
    p.delete(v)
    x << v
  end

  max_clique_size
end

triangles = Set.new
edges.each do |edge|
  v1, v2 = edge
  shared = adjacency_matrix[v1] & adjacency_matrix[v2]
  shared.each do |v3|
    triangle = [v1, v2, v3]
    triangles << Set.new(triangle) if triangle.any? { |vertex| t_vertices.include?(vertex) }
  end
end
puts triangles.length

max_clique_size = Bron_Kerbosch(Set.new, vertices, Set.new, adjacency_matrix, 1)
puts $maximal_cliques.keep_if { |clique| clique.length == max_clique_size }[0].sort.join(',')
