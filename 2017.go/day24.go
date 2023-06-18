package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Component [2]int

func find_strength(components []Component) int {
	strength := 0
	for _, component := range components {
		strength += component[0] + component[1]
	}
	return strength
}

func find_eligible(lhs int, components map[Component]bool) map[Component]bool {
	ret := map[Component]bool{}
	for component := range components {
		if (component[0] == lhs) || (component[1] == lhs) {
			ret[component] = true
		}
	}
	return ret
}

func optimize(lhs int, components map[Component]bool, bridge []Component) (int, int) {
	eligible_components := find_eligible(lhs, components)
	if len(eligible_components) == 0 {
		return find_strength(bridge), len(bridge)
	}

	max_strength := -1
	min_length := len(bridge)

	for eligible := range eligible_components {
		remaining := map[Component]bool{}
		for component := range components {
			remaining[component] = true
		}
		delete(remaining, eligible)

		var new_lhs int
		if eligible[0] == lhs {
			new_lhs = eligible[1]
		} else if eligible[1] == lhs {
			new_lhs = eligible[0]
		} else {
			panic("Invalid connection")
		}

		strength, length := optimize(new_lhs, remaining, append(bridge, eligible))

		// part 1
		// if strength > max_strength {
		// 	max_strength = strength
		// }

		// part 2
		// if a longer bridge is found
		// its strength become the new max
		if length > min_length {
			min_length = length
			max_strength = strength
		} else if length == min_length {
			// update the max length only if the new bright
			// is at least as long as the current longest
			if strength > max_strength {
				max_strength = strength
			}
		}

		// omitted:
		// if a bridge is stronger but shorter, it is not considered
	}

	// fmt.Println(bridge, max_strength, min_length)

	return max_strength, min_length
}

func main() {
	f, err := os.Open("input24.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	components := map[Component]bool{}

	for scanner.Scan() {
		line := scanner.Text()
		ports := strings.Split(line, "/")
		port1, _ := strconv.Atoi(ports[0])
		port2, _ := strconv.Atoi(ports[1])
		components[Component{port1, port2}] = true
	}

	fmt.Println(optimize(0, components, []Component{}))

	return
}
