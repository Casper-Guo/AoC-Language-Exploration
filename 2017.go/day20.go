// input manually processed to csv
package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func one_step(particle []float64) []float64 {
	for i := 3; i < 6; i++ {
		particle[i] += particle[i+3]
	}
	for i := 0; i < 3; i++ {
		particle[i] += particle[i+3]
	}
	return particle
}

func comp_particles(lhs, rhs []float64) bool {
	// return true if lhs is equally as close
	// or closer to the origin than rhs in the long run
	lhs_a := math.Abs(lhs[6]) + math.Abs(lhs[7]) + math.Abs(lhs[8])
	rhs_a := math.Abs(rhs[6]) + math.Abs(rhs[7]) + math.Abs(rhs[8])

	if lhs_a < rhs_a {
		return true
	} else if rhs_a < lhs_a {
		return false
	}

	lhs_v := math.Abs(lhs[3]) + math.Abs(lhs[4]) + math.Abs(lhs[5])
	rhs_v := math.Abs(rhs[3]) + math.Abs(rhs[4]) + math.Abs(rhs[5])

	if lhs_v < rhs_v {
		return true
	} else if rhs_v < lhs_v {
		return false
	}

	lhs_i := math.Abs(lhs[0]) + math.Abs(lhs[1]) + math.Abs(lhs[2])
	rhs_i := math.Abs(rhs[0]) + math.Abs(rhs[1]) + math.Abs(rhs[2])

	return lhs_i <= rhs_i
}

func main() {
	f, err := os.Open("input20.txt")

	if err != nil {
		panic(err)
	}

	scanner := bufio.NewScanner(f)
	scanner.Split(bufio.ScanLines)
	particles := [][]float64{}
	particle_dict := map[int][]float64{}

	for scanner.Scan() {
		line := scanner.Text()
		vals_str := strings.Split(line, ",")
		vals_float := []float64{}

		for _, val_str := range vals_str {
			val, _ := strconv.ParseFloat(val_str, 64)
			vals_float = append(vals_float, val)
		}

		particles = append(particles, vals_float)
	}

	// part 1
	nearest_idx := 0
	nearest_particle := particles[0]
	particle_dict[0] = particles[0]

	for idx, particle := range particles[1:] {
		if comp_particles(particle, nearest_particle) {
			nearest_idx = idx + 1
			nearest_particle = particle
		}
		particle_dict[idx+1] = particle
	}

	fmt.Println(nearest_idx, nearest_particle)

	// part 2
	positions := map[[3]float64][]int{}
	max_iter := 0

	for max_iter < 10000 {
		positions = map[[3]float64][]int{}

		for idx, particle := range particle_dict {
			next_pos := one_step(particle)
			particle_dict[idx] = next_pos

			position := [3]float64{next_pos[0], next_pos[1], next_pos[2]}

			if val, check := positions[position]; check {
				positions[position] = append(val, idx)
			} else {
				positions[position] = []int{idx}
			}
		}

		for _, indices := range positions {
			if len(indices) > 1 {
				for _, idx := range indices {
					delete(particle_dict, idx)
				}
			}
		}

		max_iter++
	}

	fmt.Println(len(particle_dict))

	return
}
