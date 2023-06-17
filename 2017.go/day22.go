package main

import (
	"bufio"
	"fmt"
	"os"
)

type Direction int
type NodeStatus int

const (
	North Direction = iota
	East
	South
	West
)

const (
	Clean NodeStatus = iota
	Weakened
	Infected
	Flagged
)

func convert_coordinates(x, y, size int) (int, int) {
	// convert coordinates from (0, 0) at top left
	// y increases downards
	// to (0, 0) at center, y increases upwards
	return x - (size / 2), (size / 2) - y
}

func turn_right(direction Direction) Direction {
	switch direction {
	case North:
		return East
	case East:
		return South
	case South:
		return West
	case West:
		return North
	default:
		panic("Invalid direction")
	}
}

func turn_left(direction Direction) Direction {
	switch direction {
	case North:
		return West
	case East:
		return North
	case South:
		return East
	case West:
		return South
	default:
		panic("Invalid direction")
	}
}

func reverse_direction(direction Direction) Direction {
	switch direction {
	case North:
		return South
	case East:
		return West
	case South:
		return North
	case West:
		return East
	default:
		panic("Invalid direction")
	}
}

func move_one(x, y int, direction Direction) (int, int) {
	switch direction {
	case North:
		return x, y + 1
	case East:
		return x + 1, y
	case South:
		return x, y - 1
	case West:
		return x - 1, y
	default:
		panic("Invalid direction")
	}
}

func update1(x, y int, direction Direction, infected bool) (int, int, Direction) {
	if infected {
		direction = turn_right(direction)
	} else {
		direction = turn_left(direction)
	}
	x, y = move_one(x, y, direction)
	return x, y, direction
}

func update2(x, y int, direction Direction, status NodeStatus) (int, int, Direction) {
	switch status {
	case Clean:
		direction = turn_left(direction)
	case Weakened:
	case Infected:
		direction = turn_right(direction)
	case Flagged:
		direction = reverse_direction(direction)
	default:
		panic("Invalid NodeStatus")
	}
	x, y = move_one(x, y, direction)
	return x, y, direction
}

func main() {
	f, err := os.Open("input22.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)

	lines := []string{}

	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	size := len(lines)
	grid1 := map[[2]int]bool{}
	grid2 := map[[2]int]NodeStatus{}

	for y, line := range lines {
		for x, node := range line {
			shift_x, shift_y := convert_coordinates(x, y, size)
			if node == '#' {
				grid1[[2]int{shift_x, shift_y}] = true
				grid2[[2]int{shift_x, shift_y}] = Infected
			} else {
				grid1[[2]int{shift_x, shift_y}] = false
				grid2[[2]int{shift_x, shift_y}] = Clean
			}
		}
	}

	current_x, current_y := 0, 0
	current_direction := North
	num_bursts, infection_bursts := 0, 0

	// part 1
	for num_bursts < 10000 {
		infected, check := grid1[[2]int{current_x, current_y}]
		if check {
			grid1[[2]int{current_x, current_y}] = !infected
		} else {
			infected = false
			grid1[[2]int{current_x, current_y}] = true
		}
		// fmt.Println(current_x, current_y, infected)
		current_x, current_y, current_direction = update1(
			current_x,
			current_y,
			current_direction,
			infected,
		)
		if !infected {
			infection_bursts++
		}
		num_bursts++
	}

	fmt.Println(infection_bursts)

	// part 2
	current_x, current_y = 0, 0
	current_direction = North
	num_bursts, infection_bursts = 0, 0

	for num_bursts < 10000000 {
		status, check := grid2[[2]int{current_x, current_y}]
		if check {
			grid2[[2]int{current_x, current_y}] = NodeStatus((status + 1) % 4)
		} else {
			status = Clean
			grid2[[2]int{current_x, current_y}] = Weakened
		}
		// fmt.Println(current_x, current_y, infected)
		current_x, current_y, current_direction = update2(
			current_x,
			current_y,
			current_direction,
			status,
		)
		if status == Weakened {
			infection_bursts++
		}
		num_bursts++
	}

	fmt.Println(infection_bursts)

	return
}
