package main

import (
	"fmt"
)

func judge(a, b int) bool {
	last16_a := a & 0xFFFF
	last16_b := b & 0xFFFF

	return last16_a == last16_b
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
