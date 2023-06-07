package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func find(parents []int, current int) int {
	if current == parents[current] {
		return current
	}

	parents[current] = find(parents, parents[current])
	return parents[current]
}

func union(parents []int, x int, y int) []int {
	parents[find(parents, x)] = find(parents, y)
	return parents
}

func main() {
	f, err := os.Open("input12.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	graph := [][]int{}

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), " <-> ")
		current, _ := strconv.Atoi(line[0])
		connections := strings.Split(line[1], ", ")

		graph = append(graph, []int{})

		for _, i := range connections {
			connection, _ := strconv.Atoi(i)
			graph[current] = append(graph[current], connection)
		}
	}

	parent := []int{}

	for i := 0; i < len(graph); i++ {
		parent = append(parent, i)
	}

	for current, connections := range graph {
		for _, connection := range connections {
			parent = union(parent, current, connection)
		}
	}

	group_zero := 0
	distinct_groups := map[int]bool{}

	for _, current := range parent {
		current_parent := find(parent, current)
		distinct_groups[current_parent] = true
		if current_parent == find(parent, 0) {
			group_zero++
		}
	}

	fmt.Println(group_zero, len(distinct_groups))

	return
}
