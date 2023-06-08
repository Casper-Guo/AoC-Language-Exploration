package main

import (
	"fmt"
)

func judge(a, b int) bool {
	a_binary := fmt.Sprintf("%b", a)
	b_binary := fmt.Sprintf("%b", b)

	a_start := len(a_binary) - 16
	if a_start < 0 {
		a_start = 0
	}
	b_start := len(b_binary) - 16
	if b_start < 0 {
		b_start = 0
	}

	return a_binary[a_start:] == b_binary[b_start:]
}

func main() {
	var a_factor, b_factor, a_init, b_init int = 16807, 48271, 703, 516

	// part 1
	count := 0
	for i := 0; i < 40000000; i++ {
		a_init *= a_factor
		b_init *= b_factor
		a_init = a_init % 2147483647
		b_init = b_init % 2147483647

		if judge(a_init, b_init) {
			count++
		}
	}
	fmt.Println(count)

	// part 2
	count = 0
	a_init = 703
	b_init = 516
	for i := 0; i < 5000000; i++ {
		for a_init%4 != 0 {
			a_init *= a_factor
			a_init = a_init % 2147483647
		}

		for b_init%8 != 0 {
			b_init *= b_factor
			b_init = b_init % 2147483647
		}

		if judge(a_init, b_init) {
			count++
		}
		a_init *= a_factor
		b_init *= b_factor
		a_init = a_init % 2147483647
		b_init = b_init % 2147483647
	}
	fmt.Println(count)
	return
}
