package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func execute(command, programs string) string {
	switch command[0] {
	case 's':
		steps, _ := strconv.Atoi(command[1:])
		rotate := len(programs) - steps
		programs = programs[rotate:] + programs[:rotate]
	case 'x':
		sep := strings.Index(command, "/")
		lhs, _ := strconv.Atoi(command[1:sep])
		rhs, _ := strconv.Atoi(command[sep+1:])

		if lhs > rhs {
			lhs, rhs = rhs, lhs
		} else if lhs == rhs {
			return programs
		}
		programs = programs[:lhs] + string(programs[rhs]) + programs[lhs+1:rhs] + string(programs[lhs]) + programs[rhs+1:]
	case 'p':
		lhs := strings.Index(programs, string(command[1]))
		rhs := strings.Index(programs, string(command[3]))
		programs = execute(fmt.Sprintf("x%v/%v", lhs, rhs), programs)
	}

	return programs
}

func dance(commands []string, programs string) string {
	for _, command := range commands {
		programs = execute(command, programs)
	}
	return programs
}

func main() {
	f, err := os.ReadFile("input16.txt")

	if err != nil {
		panic(err)
	}

	commands := strings.Split(string(f), ",")
	programs := "abcdefghijklmnop"

	// part 1
	part1 := dance(commands, programs)
	fmt.Println(part1)

	// part 2
	tortoise := dance(commands, programs)
	hare := dance(commands, dance(commands, programs))

	for tortoise != hare {
		tortoise = dance(commands, tortoise)
		hare = dance(commands, dance(commands, hare))
	}

	tortoise = programs
	for tortoise != hare {
		tortoise = dance(commands, tortoise)
		hare = dance(commands, hare)
	}

	cycle_length := 1
	hare = dance(commands, tortoise)
	for tortoise != hare {
		hare = dance(commands, hare)
		cycle_length++
	}

	part2 := programs
	for i := 0; i < 1000000000%cycle_length; i++ {
		part2 = dance(commands, part2)
	}
	fmt.Println(part2)
	return
}
