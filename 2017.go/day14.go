package main

import (
	"fmt"
	"strconv"
)

func reverse(nums []int, current int, length int) {
	for i := 0; i < length/2; i++ {
		lhs := (current + i) % len(nums)
		rhs := (current + length - 1 - i) % len(nums)

		nums[lhs], nums[rhs] = nums[rhs], nums[lhs]
	}
}

func knot_hash(str string) string {
	nums := []int{}
	for i := 0; i < 256; i++ {
		nums = append(nums, i)
	}
	current := 0
	skip_size := 0

	ascii := []int{}
	for _, i := range str {
		ascii = append(ascii, int(i))
	}
	ascii = append(ascii, []int{17, 31, 73, 47, 23}...)

	// sparse hash
	for i := 0; i < 64; i++ {
		for _, length := range ascii {
			reverse(nums, current, length)
			current = (current + length + skip_size) % len(nums)
			skip_size++
		}
	}

	// dense hash
	var dense_hash string
	for i := 0; i < 16; i++ {
		output := nums[i*16]
		for j := i*16 + 1; j < (i+1)*16; j++ {
			output = output ^ nums[j]
		}
		dense := strconv.FormatInt(int64(output), 16)
		if len(dense) < 2 {
			dense = "0" + dense
		}
		dense_hash += dense
	}

	if len(dense_hash) != 32 {
		panic("Incorrect hash length")
	}

	return dense_hash
}

func validate_move(x int, y int, grid map[int]map[int]int, visited map[int]map[int]bool) bool {
	if !(x >= 0 && x < 128 && y >= 0 && y < 128) {
		return false
	}
	if _, exist := visited[x][y]; exist {
		return false
	}
	if grid[x][y] != -1 {
		return false
	}
	return true
}

func generate_moves(x int, y int, grid map[int]map[int]int, visited map[int]map[int]bool) []int {
	valid_moves := []int{}
	if validate_move(x+1, y, grid, visited) {
		valid_moves = append(valid_moves, []int{x + 1, y}...)
	}
	if validate_move(x-1, y, grid, visited) {
		valid_moves = append(valid_moves, []int{x - 1, y}...)
	}
	if validate_move(x, y+1, grid, visited) {
		valid_moves = append(valid_moves, []int{x, y + 1}...)
	}
	if validate_move(x, y-1, grid, visited) {
		valid_moves = append(valid_moves, []int{x, y - 1}...)
	}
	return valid_moves
}

func main() {
	used_squares := 0
	// free squares marked -2
	// unvisited used squares marked -1
	// squares that have been put inside a region
	// has the region number
	grid := map[int]map[int]int{}

	for i := 0; i < 128; i++ {
		str := "ugkiagan-" + strconv.Itoa(i)
		hash := knot_hash(str)

		grid[i] = map[int]int{}

		for j, hex := range hash {
			num, _ := strconv.ParseInt(string(hex), 16, 64)
			binary := fmt.Sprintf("%04b", num)
			for k, b := range binary {
				if b == '1' {
					used_squares++
					grid[i][4*j+k] = -1
				} else {
					grid[i][4*j+k] = -2
				}
			}
		}
	}
	fmt.Println(used_squares)

	// BFS
	num_regions := 0
	visited := map[int]map[int]bool{}

	for i := 0; i < 128; i++ {
		visited[i] = map[int]bool{}
		for j := 0; j < 128; j++ {
			if !validate_move(i, j, grid, visited) {
				continue
			}

			queue := []int{i, j}

			for len(queue) > 0 {
				x, y := queue[len(queue)-2], queue[len(queue)-1]
				grid[x][y] = num_regions

				if visited[x] == nil {
					visited[x] = map[int]bool{}
				}
				visited[x][y] = true

				queue = queue[:len(queue)-2]
				queue = append(queue, generate_moves(x, y, grid, visited)...)
			}
			num_regions++
		}
	}

	fmt.Println(num_regions)

	return
}
