package main

import (
	"fmt"
	"os"
)

func main() {
	input, _ := os.ReadFile("input01.txt")
	solution := 0

	// part 1
	for i := 0; i < len(input)-1; i++ {
		if input[i] == input[i+1] {
			solution += int(input[i] - '0')
		}
	}

	if input[0] == input[len(input)-1] {
		solution += int(input[0] - '0')
	}

	fmt.Println(solution)

	solution = 0

	// part 2
	for idx, rune := range input {
		across_idx := (idx + (len(input) / 2)) % len(input)

		if input[idx] == input[across_idx] {
			solution += int(rune - '0')
		}
	}

	fmt.Println(solution)
}
