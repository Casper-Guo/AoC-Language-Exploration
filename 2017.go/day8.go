package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func condition(comp_register string, comp string, comp_amt int, registers map[string]int) bool {
	switch comp {
	case "<":
		return registers[comp_register] < comp_amt
	case ">":
		return registers[comp_register] > comp_amt
	case ">=":
		return registers[comp_register] >= comp_amt
	case "<=":
		return registers[comp_register] <= comp_amt
	case "==":
		return registers[comp_register] == comp_amt
	case "!=":
		return registers[comp_register] != comp_amt
	default:
		panic("Invalid comparison operator")

	}
}

func execute(line []string, registers map[string]int) int {
	target := line[0]
	inc := line[1] == "inc"
	amt, _ := strconv.Atoi(line[2])
	comp_register := line[4]
	comp := line[5]
	comp_amt, _ := strconv.Atoi(line[6])

	if condition(comp_register, comp, comp_amt, registers) {
		if inc {
			registers[target] += amt
		} else {
			registers[target] -= amt
		}
	}

	return registers[target]
}

func main() {
	f, err := os.Open("input8.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	registers := map[string]int{}

	highest_seen := math.MinInt

	for scanner.Scan() {
		line := strings.Fields(scanner.Text())
		new_value := execute(line, registers)

		if new_value > highest_seen {
			highest_seen = new_value
		}
	}

	max_value := math.MinInt
	for _, val := range registers {
		if val > max_value {
			max_value = val
		}
	}

	fmt.Println(max_value, highest_seen)
}
