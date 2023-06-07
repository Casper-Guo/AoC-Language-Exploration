package main

import (
	"fmt"
	"math"
)

func grid_get(grid map[int]map[int]int, x int, y int) int {
	if grid[x] != nil {
		num, err := grid[x][y]
		if err {
			return num
		}
	}
	return 0
}

func grid_set(grid map[int]map[int]int, x int, y int, value int) int {
	if grid[x] == nil {
		grid[x] = map[int]int{y: value}
	} else {
		grid[x][y] = value
	}

	return value
}

func sum_neighbor(grid map[int]map[int]int, x int, y int) int {
	return grid_get(grid, x-1, y) + grid_get(grid, x+1, y) +
		grid_get(grid, x, y-1) + grid_get(grid, x, y+1) +
		grid_get(grid, x-1, y-1) + grid_get(grid, x-1, y+1) +
		grid_get(grid, x+1, y+1) + grid_get(grid, x+1, y-1)
}

func main() {
	input := 368078

	// part 1
	// the 0th ring is 1...1
	// the 1st ring is 2...9
	// the 2nd ring is 10...25
	// first find which ring we are on
	ring := int(math.Floor(math.Sqrt(float64(input))))

	if ring%2 == 0 {
		// ring identifies the root of the perfect square
		// that sits at the end of the last ring
		// e.x. input = 117, ring = 9
		// because 9^2 < 117 < 11^2
		ring -= 1
	} else {
		if ring*ring == input {
			// input is an odd perfect square
			// and sits at the end of its ring
			fmt.Println("Steps needed: ", math.Floor(float64(ring)/2)*2)
			return
		}
	}

	// number at the start of the current ring
	// always odd perfect square + 1
	ring_start := int(math.Pow(float64(ring), 2) + 1)

	// x and y coordinates of the current ring start
	start_x := int(ring/2 + 1)
	start_y := int(-(ring / 2))

	// number at the start of the next ring
	next_ring_start := math.Pow(float64(ring+2), 2)

	// each ring can be evenly divided into 4 edges
	edge_size := (int(next_ring_start) - ring_start + 1) / 4

	// how many steps is input away from the ring_start
	// if we follow the ring
	total_steps := input - ring_start

	/*    1
		----|
		|   |
	  2	|   | 0
		|   |<-- ring_start
		|----!<-- next_ring_start
		  3
	*/
	edge := total_steps / edge_size

	// how many steps away from the start of the edge
	edge_steps := total_steps % edge_size
	var input_x, input_y int

	switch edge {
	case 0:
		input_y = start_y + edge_steps
		input_x = start_x
	case 1:
		input_y = start_y + edge_size - 1
		input_x = start_x - edge_steps - 1
	case 2:
		input_x = start_x - edge_size
		input_y = start_y + edge_size - 2 - edge_steps
	case 3:
		input_x = start_x - edge_size + 1 + edge_steps
		input_y = start_y - 1
	default:
		panic("Invalid edge orientation")
	}

	fmt.Println("Steps needed: ", math.Abs(float64(input_x))+math.Abs(float64(input_y)))

	// part 2
	var current_x, current_y, edge_length int = 1, 0, 1
	grid := map[int]map[int]int{}
	current_value := grid_set(grid, 0, 0, 1)

	for current_value < input {
		// edge 0
		for i := 0; i < edge_length; i++ {
			current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
			current_y += 1
		}
		current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
		current_x -= 1

		// edge 1
		for i := 0; i < edge_length; i++ {
			current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
			current_x -= 1
		}
		current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
		current_y -= 1

		// edge 2
		for i := 0; i < edge_length; i++ {
			current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
			current_y -= 1
		}
		current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
		current_x += 1

		// edge 3
		for i := 0; i < edge_length; i++ {
			current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
			current_x += 1
		}
		current_value = grid_set(grid, current_x, current_y, sum_neighbor(grid, current_x, current_y))
		current_x += 1

		edge_length += 2
	}

	fmt.Println(current_value)

	return
}
