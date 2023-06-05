package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func reverse(nums []int, current int, length int) {
	for i := 0; i < length/2; i++ {
		lhs := (current + i) % len(nums)
		rhs := (current + length - 1 - i) % len(nums)

		nums[lhs], nums[rhs] = nums[rhs], nums[lhs]
	}
}

func main() {
	f, err := os.ReadFile("input10.txt")

	if err != nil {
		panic(err)
	}

	str := string(f)

	skip_size := 0
	current := 0
	nums := []int{}

	for i := 0; i < 256; i++ {
		nums = append(nums, i)
	}

	// part 1
	lengths_str := strings.Split(str, ",")
	lengths := []int{}

	for _, i := range lengths_str {
		length, _ := strconv.Atoi(i)
		lengths = append(lengths, length)
	}

	for _, length := range lengths {
		if length <= len(nums) {
			reverse(nums, current, length)
		}
		current = (current + length + skip_size) % len(nums)
		skip_size++
	}

	fmt.Println(nums[0] * nums[1])

	// part 2
	nums = nil
	for i := 0; i < 256; i++ {
		nums = append(nums, i)
	}
	current = 0
	skip_size = 0

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

	fmt.Println(dense_hash)

	return
}
