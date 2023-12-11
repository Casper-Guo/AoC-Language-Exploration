package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

func tree_weight(root string,
	tree map[string][]string,
	weights map[string]int,
	tree_weights map[string]int) int {
	if tree[root][0] == "" {
		return weights[root]
	}

	total_weight, err := tree_weights[root]

	if !err {
		total_weight = 0
		for _, node := range tree[root] {
			total_weight += tree_weight(node, tree, weights, tree_weights)
		}

		total_weight += weights[root]
		tree_weights[root] = total_weight
	}

	return total_weight
}

func check_balance(root string,
	tree map[string][]string,
	weights map[string]int,
	tree_weights map[string]int) bool {
	if len(tree[root]) <= 2 {
		// if only one child, then has to be balanced
		// if only two children, then impossible to determine
		// the single child node that is imbalanced
		return true
	}

	child_weights := map[int][]string{}

	for _, child := range tree[root] {
		child_weight := tree_weight(child, tree, weights, tree_weights)
		child_weights[child_weight] = append(child_weights[child_weight], child)
	}

	if len(child_weights) > 1 {
		for key, val := range child_weights {
			if len(val) == 1 {
				fmt.Println("Imbalanced node: ", key)
				fmt.Println("The weight is: ", weights[val[0]])
			} else {
				fmt.Println("The other weights are: ", key)
			}
		}
	}

	return len(child_weights) == 1
}

func main() {
	f, err := os.Open("input7.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	programs := map[string]bool{}
	weights := map[string]int{}
	tree := map[string][]string{}

	for scanner.Scan() {
		line := strings.Fields(scanner.Text())

		program := line[0]
		weight, _ := strconv.Atoi(line[1][1 : len(line[1])-1])
		weights[program] = weight

		// check if it is leaf node
		if len(line) > 2 {
			_, err := programs[program]
			childs := []string{}

			if !err {
				// might be bottom
				// add to map
				programs[program] = true
			}

			for _, i := range line[3:] {
				i = strings.ReplaceAll(i, ",", "")
				childs = append(childs, i)
				programs[i] = false
				tree[program] = childs
			}
		} else {
			tree[program] = []string{""}
		}
	}

	// part 1
	for key, value := range programs {
		if value {
			fmt.Println(key)
		}
	}

	// part 2
	// record tree weights to avoid repeated computation
	tree_weights := map[string]int{}
	for node := range tree {
		if !check_balance(node, tree, weights, tree_weights) {
			break
		}
	}

	return
}
