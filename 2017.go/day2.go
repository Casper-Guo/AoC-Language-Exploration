package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	f, err := os.Open("input2.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	var numbers [][]int
	var part1, part2 int = 0, 0

	// part 1
	for scanner.Scan() {
		line := strings.Fields(scanner.Text())
		var number []int

		for _, i := range line {
			num, err := strconv.Atoi(i)

			if err != nil {
				panic(err)
			}

			number = append(number, num)
		}
		numbers = append(numbers, number)
	}

	for _, line := range numbers {
		var max, min int = -1, 1000000

		for i, num1 := range line {
			if num1 < min {
				min = num1
			}
			if num1 > max {
				max = num1
			}

			for j, num2 := range line {
				if i == j {
					continue
				}
				if num1 > num2 && num1%num2 == 0 {
					part2 += num1 / num2
				}
			}
		}
		part1 += max - min
	}
	fmt.Println(part1)
	fmt.Println(part2)
}
