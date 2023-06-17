package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"reflect"
	"strings"
)

type Grid [][]bool
type Rule [2]Grid

func print_grid(grid Grid) {
	for _, row := range grid {
		for _, pixel := range row {
			if pixel {
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
}

func flip_vertical(grid Grid) Grid {
	size := len(grid)
	new_grid := make(Grid, size)

	for i := 0; i < size; i++ {
		new_grid[i] = make([]bool, size)
		copy(new_grid[i], grid[i])
	}

	for row := 0; row < size/2; row++ {
		new_grid[row], new_grid[size-row-1] = grid[size-row-1], grid[row]
	}
	return new_grid
}

func flip_horizontal(grid Grid) Grid {
	size := len(grid)
	new_grid := make(Grid, size)

	for i := 0; i < size; i++ {
		new_grid[i] = make([]bool, size)
		copy(new_grid[i], grid[i])
	}

	for col := 0; col < size/2; col++ {
		for row := 0; row < size; row++ {
			new_grid[row][size-col-1], new_grid[row][col] = grid[row][col], grid[row][size-col-1]
		}
	}
	return new_grid
}

func rotate(grid Grid) Grid {
	// clockwise rotation
	size := len(grid)
	new_grid := make(Grid, size)

	for i := 0; i < size; i++ {
		new_grid[i] = make([]bool, size)
		copy(new_grid[i], grid[i])
	}

	for row := 0; row < size; row++ {
		for col := 0; col < size; col++ {
			new_grid[row][col] = grid[size-col-1][row]
		}
	}

	return new_grid
}

func transform(grid Grid, rules []Rule) Grid {
	variations := []Grid{
		grid,
		flip_vertical(grid),
		flip_horizontal(grid),
	}

	for i := 0; i < 3; i++ {
		variation := variations[i]
		for j := 0; j < 3; j++ {
			variation = rotate(variation)
			variations = append(variations, variation)
		}
	}

	for _, rule := range rules {
		for _, variation := range variations {
			if reflect.DeepEqual(variation, rule[0]) {
				return rule[1]
			}
		}
	}
	panic("No match found")
}

func join(grids []Grid) Grid {
	s := math.Sqrt(float64(len(grids)))

	if s != math.Trunc(s) {
		panic("Cannot join non-square grids")
	}

	size := int(s)
	joined := Grid{}

	for i := 0; i < len(grids); i += size {
		// call every {size} subgrids a group
		// each group are placed size by size horizontally
		for j := 0; j < len(grids[0]); j++ {
			// iterate over each row in the group
			row := []bool{}
			for k := i; k < i+size; k++ {
				// collect the content of that row
				// from every subgrid in the group
				row = append(row, grids[k][j]...)
			}
			joined = append(joined, row)
		}
	}

	return joined
}

func subgrid(grid Grid, x_start, y_start, size int) Grid {
	if x_start < 0 || y_start < 0 || size < 0 {
		panic("Invalid argument")
	}

	if x_start+size > len(grid) || y_start+size > len(grid) {
		panic("Grid not big enough")
	}

	sub := Grid{}
	for y := y_start; y < y_start+size; y++ {
		sub = append(sub, grid[y][x_start:x_start+size])
	}

	return sub
}

func divide(grid Grid, rules []Rule) Grid {
	size := len(grid)
	subgrids := []Grid{}
	if size < 2 {
		return grid
	} else if size == 2 {
		return transform(grid, rules)
	} else if size == 3 {
		return transform(grid, rules)
	} else if size%2 == 0 {
		for y := 0; y < size; y += 2 {
			for x := 0; x < size; x += 2 {
				subgrids = append(subgrids, subgrid(grid, x, y, 2))
			}
		}
	} else if size%3 == 0 {
		for y := 0; y < size; y += 3 {
			for x := 0; x < size; x += 3 {
				subgrids = append(subgrids, subgrid(grid, x, y, 3))
			}
		}
	}

	for idx, subgrid := range subgrids {
		subgrids[idx] = transform(subgrid, rules)
	}

	return join(subgrids)
}

func text_to_grid(text string) Grid {
	rows := strings.Split(text, "/")
	grid := make(Grid, len(rows))

	for idx, row := range rows {
		grid[idx] = []bool{}
		for _, pixel := range row {
			if pixel == '.' {
				grid[idx] = append(grid[idx], false)
			} else {
				grid[idx] = append(grid[idx], true)
			}
		}
	}
	return grid
}

func main() {
	f, err := os.Open("input21.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)

	rules := []Rule{}
	for scanner.Scan() {
		line := scanner.Text()
		patterns := strings.Split(line, " => ")
		rules = append(rules, Rule{
			text_to_grid(patterns[0]),
			text_to_grid(patterns[1]),
		})
	}

	grid := text_to_grid(".#./..#/###")

	for i := 0; i < 18; i++ {
		grid = divide(grid, rules)
	}

	num_on := 0
	for _, row := range grid {
		for _, pixel := range row {
			if pixel {
				num_on++
			}
		}
	}

	fmt.Println(num_on)

	return
}
