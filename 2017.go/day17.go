package main

import (
	"container/list"
	"fmt"
)

func main() {
	skip := 345
	buffer := list.New()
	buffer.PushBack(0)
	current := buffer.Front()

	// part 1
	for i := 1; i < 2018; i++ {
		for j := 0; j < skip; j++ {
			current = current.Next()
			if current == nil {
				current = buffer.Front()
			}
		}
		current = buffer.InsertAfter(i, current)
	}

	for element := buffer.Front(); element != nil; element = element.Next() {
		if element.Value == 2017 {
			fmt.Println(element.Next().Value)
			break
		}
	}

	// part 2
	// the value after 0 is always the value at position 1
	// so we just need to record the last element written to position 1
	current_pos := 0
	last_write := 0
	for i := 1; i < 50000001; i++ {
		current_pos = (current_pos + skip) % i
		if current_pos == 0 {
			last_write = i
		}
		current_pos++
	}
	fmt.Println(last_write)
	return
}
