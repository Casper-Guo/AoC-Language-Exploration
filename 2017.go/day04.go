package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func check_anagram(word1 string, word2 string) bool {
	if len(word1) != len(word2) {
		return false
	}

	letter_freq := map[rune]int{}

	for _, i := range word1 {
		letter_freq[i]++
	}

	for letter, freq := range letter_freq {
		if strings.Count(word2, string(letter)) != freq {
			return false
		}
	}

	return true
}

func main() {
	f, err := os.Open("input04.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	part1 := 0
	part2 := 0

	for scanner.Scan() {
		line := strings.Fields(scanner.Text())
		words := map[string]bool{}
		no_repeat := true
		no_anagram := true

		for i, word1 := range line {
			_, err := words[word1]

			if no_anagram {
				for j, word2 := range line {
					if i == j {
						continue
					}
					if check_anagram(word1, word2) {
						no_anagram = false
						break
					}
				}
			}

			if err {
				no_repeat = false
				break
			} else {
				words[word1] = true
			}
		}

		if no_repeat {
			part1++
		}

		if no_anagram {
			part2++
		}
	}

	fmt.Println(part1, part2)

	return
}
