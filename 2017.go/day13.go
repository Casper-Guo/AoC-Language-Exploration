package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func scanner_pos(wall_range, time int) int {
	// scanner position at the beginning of time seconds
	cycle_length := 2 * (wall_range - 1)
	cycle_pos := time % cycle_length
	if cycle_pos <= wall_range {
		return cycle_pos
	} else {
		return wall_range - (cycle_pos - wall_range)
	}
}

func main() {
	f, err := os.Open("input13.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)

	firewalls := map[int]int{}

	for scanner.Scan() {
		line := strings.Split(scanner.Text(), ": ")
		depth, _ := strconv.Atoi(line[0])
		wall_range, _ := strconv.Atoi(line[1])
		firewalls[depth] = wall_range
	}

	severity := 0
	for depth, wall_range := range firewalls {
		if scanner_pos(wall_range, depth) == 0 {
			severity += depth * wall_range
		}
	}

	fmt.Println(severity)

	safe_passage := false
	time := 1

	for !safe_passage {
		safe_passage = true
		for depth, wall_range := range firewalls {
			if scanner_pos(wall_range, depth+time) == 0 {
				safe_passage = false
				break
			}
		}
		time++
	}

	fmt.Println(time - 1)

	return
}
