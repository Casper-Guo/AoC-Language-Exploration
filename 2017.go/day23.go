package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func registers_get(target string, registers map[string]int) int {
	if val, err := strconv.Atoi(target); err == nil {
		return val
	} else {
		return registers[target]
	}
}

func execute(tokens []string,
	registers map[string]int,
	idx int) (map[string]int, int) {
	val := registers_get(tokens[2], registers)
	switch tokens[0] {
	case "set":
		registers[tokens[1]] = val
		return registers, idx + 1
	case "sub":
		registers[tokens[1]] -= val
		return registers, idx + 1
	case "mul":
		registers[tokens[1]] *= val
		return registers, idx + 1
	case "jnz":
		if registers_get(tokens[1], registers) != 0 {
			idx += registers_get(tokens[2], registers)
		} else {
			idx += 1
		}
		return registers, idx
	default:
		panic("Unknown instruction")
	}
}

func main() {
	f, err := os.Open("input23.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	registers := map[string]int{
		"a": 1,
		"b": 0,
		"c": 0,
		"d": 0,
		"e": 0,
		"f": 0,
		"g": 0,
		"h": 0,
	}
	instructions := []string{}

	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}

	// part 1
	idx := 0
	num_mul := 0

	for idx < len(instructions) {
		tokens := strings.Split(instructions[idx], " ")
		if tokens[0] == "mul" {
			num_mul += 1
		}
		registers, idx = execute(tokens, registers, idx)
	}

	fmt.Println(num_mul)

	// part 2
	// initialize b to 107900, c to 124900
	num_composites := 0
	b, c := 107900, 124901

	for b < c {
		for i := 2; i < int(math.Ceil(math.Sqrt(float64(b)))); i++ {
			if b%i == 0 {
				num_composites++
				break
			}
		}
		b += 17
	}
	fmt.Println(num_composites)
}
