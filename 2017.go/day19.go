package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type Direction int

const (
	North Direction = iota
	East
	South
	West
)

func (d Direction) String() string {
	return [...]string{"North", "East", "South", "West"}[d]
}

func grid_get(x, y int, grid []string) string {
	if x < 0 || y < 0 || y >= len(grid) || x >= len(grid[y]) {
		return "!"
	}
	return string(grid[y][x])
}

func immediate_next_move(d Direction, x, y int) (int, int) {
	switch d {
	case West:
		return x - 1, y
	case East:
		return x + 1, y
	case North:
		return x, y - 1
	case South:
		return x, y + 1
	default:
		panic("Invalid direction")
	}
}

func possible_next_moves(d Direction, x, y int) ([]int, []int) {
	switch d {
	case West:
		return []int{x, x, x - 1}, []int{y + 1, y - 1, y}
	case East:
		return []int{x, x, x + 1}, []int{y + 1, y - 1, y}
	case North:
		return []int{x + 1, x - 1, x}, []int{y, y, y - 1}
	case South:
		return []int{x + 1, x - 1, x}, []int{y, y, y + 1}
	default:
		panic("Invalid direction")
	}
}

func make_move(d Direction, x int, y int, grid []string) (Direction, int, int) {
	if grid_get(x, y, grid) == "+" {
		possible_x, possible_y := possible_next_moves(d, x, y)

		for i := 0; i < 3; i++ {
			next_x, next_y := possible_x[i], possible_y[i]
			next := grid_get(next_x, next_y, grid)
			if next != "!" && next != " " {
				if next_x == x {
					if next_y == y+1 {
						return South, next_x, next_y
					} else {
						return North, next_x, next_y
					}
				} else {
					if next_x == x+1 {
						return East, next_x, next_y
					} else {
						return West, next_x, next_y
					}
				}
			}
		}
	} else {
		x, y := immediate_next_move(d, x, y)
		return d, x, y
	}
	panic("End not reached but no valid move found.")
}

func check_end(d Direction, x, y int, grid []string) bool {
	next_x, next_y := possible_next_moves(d, x, y)

	for i := 0; i < 3; i++ {
		x, y := next_x[i], next_y[i]
		next := grid_get(x, y, grid)
		if next != "!" && next != " " {
			return false
		}
	}
	return true
}

func main() {
	f, err := os.Open("input19.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	var grid []string

	for scanner.Scan() {
		line := scanner.Text()
		grid = append(grid, line)
	}

	current_y := 0
	current_x := strings.Index(grid[0], "|")
	var current_direction = South
	num_steps := 0

	for !check_end(current_direction, current_x, current_y, grid) {
		current := grid_get(current_x, current_y, grid)
		if current[0] >= 65 && current[0] <= 90 {
			fmt.Print(current)
		}
		// fmt.Println(current_x, current_y, current_direction, current)
		current_direction, current_x, current_y = make_move(current_direction,
			current_x,
			current_y,
			grid)
		num_steps++
	}

	fmt.Println(grid_get(current_x, current_y, grid))
	fmt.Println(num_steps + 1)
	return
}
