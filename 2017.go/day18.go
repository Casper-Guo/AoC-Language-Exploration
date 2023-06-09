package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
	"time"
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
	idx int) (map[string]int, int, int) {
	// returns the new registers
	// the value that's been set/transmitted
	// the idx of the next instruction
	switch tokens[0] {
	case "snd":
		return registers, registers_get(tokens[1], registers), idx + 1
	case "set":
		val := registers_get(tokens[2], registers)
		registers[tokens[1]] = val
		return registers, val, idx + 1
	case "add":
		val := registers_get(tokens[2], registers)
		registers[tokens[1]] += val
		return registers, registers[tokens[1]], idx + 1
	case "mul":
		val := registers_get(tokens[2], registers)
		registers[tokens[1]] *= val
		return registers, registers[tokens[1]], idx + 1
	case "mod":
		val := registers_get(tokens[2], registers)
		registers[tokens[1]] %= val
		return registers, registers[tokens[1]], idx + 1
	case "rcv":
		if registers_get(tokens[1], registers) != 0 {
			return registers, 0, math.MaxInt
		} else {
			return registers, 0, idx + 1
		}
	case "jgz":
		if registers_get(tokens[1], registers) > 0 {
			idx += registers_get(tokens[2], registers)
		} else {
			idx += 1
		}
		return registers, 0, idx
	default:
		panic("Unknown instruction")
	}
}

func part2(instructions []string, id int, out, in chan int) int {
	registers := map[string]int{"p": id}
	idx := 0
	num_sends := 0
	for idx < len(instructions) {
		tokens := strings.Split(instructions[idx], " ")
		switch tokens[0] {
		case "snd":
			select {
			case out <- registers_get(tokens[1], registers):
				num_sends++
				fmt.Println("Send ", registers_get(tokens[1], registers), " from ", id)
			case <-time.After(1 * time.Second):
				return num_sends
			}
			idx++
		case "rcv":
			select {
			case registers[tokens[1]] = <-in:
				fmt.Println("Received ", registers[tokens[1]], " at ", id)
			case <-time.After(1 * time.Second):
				return num_sends
			}
			idx++
		default:
			registers, _, idx = execute(tokens, registers, idx)
		}
	}
	return num_sends
}

func main() {
	f, err := os.Open("input18.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	registers := map[string]int{}
	instructions := []string{}

	for scanner.Scan() {
		instructions = append(instructions, scanner.Text())
	}

	// part 1
	idx := 0
	last_transmitted := 0

	for idx < len(instructions) {
		tokens := strings.Split(instructions[idx], " ")
		if tokens[0] == "snd" {
			registers, last_transmitted, idx = execute(tokens, registers, idx)
		} else {
			registers, _, idx = execute(tokens, registers, idx)
		}
	}

	fmt.Println(last_transmitted)

	// part 2
	channel0 := make(chan int, 10000)
	channel1 := make(chan int, 10000)
	go part2(instructions, 0, channel0, channel1)
	fmt.Println(part2(instructions, 1, channel1, channel0))

	return
}
