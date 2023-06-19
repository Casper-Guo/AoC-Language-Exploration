package main

import (
	"container/list"
	"fmt"
)

type State int

const (
	A State = iota
	B
	C
	D
	E
	F
)

func print_tape(tape *list.List) {
	for e := tape.Front(); e != nil; e = e.Next() {
		fmt.Print(e.Value)
	}
	fmt.Println()
}

func move_cursor(cursor *list.Element, tape *list.List, left bool) *list.Element {
	if left {
		if cursor == tape.Front() {
			cursor = tape.PushFront(0)
		} else {
			cursor = cursor.Prev()
		}
	} else {
		if cursor == tape.Back() {
			cursor = tape.PushBack(0)
		} else {
			cursor = cursor.Next()
		}
	}
	return cursor
}

func turing_machine(state State, cursor *list.Element, tape *list.List) (State, *list.Element, *list.List) {
	switch state {
	case A:
		if cursor.Value == 0 {
			cursor.Value = 1
			state = B
			cursor = move_cursor(cursor, tape, false)
		} else {
			cursor.Value = 0
			state = F
			cursor = move_cursor(cursor, tape, false)
		}
	case B:
		if cursor.Value == 0 {
			cursor = move_cursor(cursor, tape, true)
		} else {
			cursor.Value = 1
			state = C
			cursor = move_cursor(cursor, tape, true)
		}
	case C:
		if cursor.Value == 0 {
			cursor.Value = 1
			state = D
			cursor = move_cursor(cursor, tape, true)
		} else {
			cursor.Value = 0
			cursor = move_cursor(cursor, tape, false)
		}
	case D:
		if cursor.Value == 0 {
			cursor.Value = 1
			state = E
			cursor = move_cursor(cursor, tape, true)
		} else {
			state = A
			cursor = move_cursor(cursor, tape, false)
		}
	case E:
		if cursor.Value == 0 {
			cursor.Value = 1
			state = F
			cursor = move_cursor(cursor, tape, true)
		} else {
			cursor.Value = 0
			state = D
			cursor = move_cursor(cursor, tape, true)
		}
	case F:
		if cursor.Value == 0 {
			cursor.Value = 1
			state = A
			cursor = move_cursor(cursor, tape, false)
		} else {
			cursor.Value = 0
			state = E
			cursor = move_cursor(cursor, tape, true)
		}
	default:
		panic("Invalid state")
	}
	return state, cursor, tape
}

func main() {
	tape := list.New()
	tape.PushFront(0)
	cursor := tape.Front()
	state := A
	steps := 0

	for steps < 12425180 {
		state, cursor, tape = turing_machine(state, cursor, tape)
		steps++
	}

	checksum := 0
	for i := tape.Front(); i != nil; i = i.Next() {
		if i.Value == 1 {
			checksum++
		}
	}

	fmt.Println(checksum)

	return
}
