package main

import (
	"fmt"
	"math"
	"os"
	"strings"
)

func calc_steps(x, y float64) float64 {
	x = math.Abs(x)
	y = math.Abs(y)
	var num_steps float64 = 0

	if y >= x {
		num_steps += x / 0.5
		num_steps += y - x
	} else {
		num_steps += y / 0.5
		num_steps += (x - y) / 0.5
	}

	return num_steps
}

func main() {
	f, err := os.ReadFile("input11.txt")

	if err != nil {
		panic(err)
	}

	directions := strings.Split(string(f), ",")
	var x, y, max_steps float64 = 0, 0, -1

	for _, direction := range directions {
		switch direction {
		case "n":
			y++
		case "s":
			y--
		case "nw":
			y += 0.5
			x -= 0.5
		case "ne":
			x += 0.5
			y += 0.5
		case "sw":
			y -= 0.5
			x -= 0.5
		case "se":
			y -= 0.5
			x += 0.5
		}
		max_steps = math.Max(max_steps, calc_steps(x, y))
	}

	fmt.Println(calc_steps(x, y), max_steps)
}
