package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	file, err := os.Open("input5.txt")

	if err != nil {
		panic(err)
	}

	var perline int
	var nums []int

	for {
		_, err := fmt.Fscanf(file, "%d\n", &perline)

		if err != nil {
			if err == io.EOF {
				break
			}
			panic(err)
		}

		nums = append(nums, perline)
	}

	steps := 0
	current := 0

	for current >= 0 && current < len(nums) {
		temp := nums[current]

		if temp >= 3 {
			nums[current]--
		} else {
			nums[current]++
		}
		current += temp
		steps++
	}

	fmt.Println(steps)

	return
}
