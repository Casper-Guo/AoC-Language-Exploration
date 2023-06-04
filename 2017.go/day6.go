package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"math"
)

func reallocate(memory_banks [16]int) [16]int{
	max_blocks := math.MinInt
	max_idx := -1

	for idx, bank := range memory_banks {
		if bank > max_blocks {
			max_blocks = bank
			max_idx = idx
		}
	}
	memory_banks[max_idx] = 0
	full_cycles := max_blocks / len(memory_banks)
	remaining := max_blocks % len(memory_banks)

	for idx, _ := range memory_banks {
		memory_banks[idx] += full_cycles
	}

	for i := 0; i < remaining; i++ {
		idx := (max_idx + 1 + i) % len(memory_banks)
		memory_banks[idx]++
	}

	return memory_banks
}


func main() {
	f, err := os.ReadFile("input6.txt")

	if err != nil {
		panic(err)
	}

	line := strings.Fields(string(f))
	var memory_banks [16]int

	for idx, bank := range line {
		num_blocks, _ := strconv.Atoi(bank)
		memory_banks[idx] = num_blocks
	}

	// the naive algorithm requires storing all previous states
	// Instead, Floyd's cylcle-finding algorithm (tortoise and hare)
	tortoise := memory_banks
	hare := memory_banks

	for {
		tortoise = reallocate(tortoise)
		hare = reallocate(reallocate(hare))

		if tortoise == hare {
			break
		}
	}

	mu := 0
	tortoise = memory_banks
	for {
		if tortoise == hare {
			break
		}
		tortoise = reallocate(tortoise)
		hare = reallocate(hare)
		mu++
	}

	lambda := 1
	hare = reallocate(tortoise)

	for {
		if tortoise == hare {
			break
		}
		hare = reallocate(hare)
		lambda++
	}

	fmt.Println(mu, lambda)

	return
}