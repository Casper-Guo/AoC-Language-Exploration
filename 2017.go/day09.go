package main

import (
	"fmt"
	"os"
)

func score_stream(stream string, outer_score int) int {
	if len(stream) == 0 {
		return outer_score
	}

	in_garbage := false
	score := 0
	// LIFO
	group_starts := []int{}

	for i := 0; i < len(stream); i++ {
		if in_garbage {
			if stream[i] == '>' {
				// end of garbage
				in_garbage = false
			} else if stream[i] == '!' {
				// skip a character
				i++
			}
		} else {
			if stream[i] == '<' {
				in_garbage = true
			} else if stream[i] == '{' {
				// beginning of a group, record the index
				group_starts = append(group_starts, i)
			} else if stream[i] == '}' {
				// end of a group (may be the end of a child group)
				start := group_starts[len(group_starts)-1] + 1
				group_starts = group_starts[:len(group_starts)-1]

				// recurse when end of the entire group is reached
				if len(group_starts) == 0 {
					score += score_stream(stream[start:i], outer_score+1)
				}
			}
		}
	}
	return score + outer_score
}

func count_non_canceled(stream string) int {
	in_garbage := false
	count := 0

	for i := 0; i < len(stream); i++ {
		if in_garbage {
			if stream[i] == '>' {
				// end of garbage
				in_garbage = false
			} else if stream[i] == '!' {
				// skip a character
				i++
				continue
			} else {
				count++
			}
		} else {
			if stream[i] == '<' {
				in_garbage = true
			}
		}
	}
	return count
}

func main() {
	f, err := os.ReadFile("input9.txt")

	if err != nil {
		panic(err)
	}

	str := string(f)
	fmt.Println(score_stream(str, 0))
	fmt.Println(count_non_canceled(str))
	return
}
