// Find the first non-repeating element in a given array of integers.
//
// INPUT FORMAT
//   []int
//
// OUTPUT FORMAT
//   int, error
//
// SAMPLE INPUT
//   9, 4, 9, 6, 7, 4
//
// SAMPLE OUTPUT
//   6
//
package main

import (
	"fmt"
)

// ProblemName is the package-level label of the coding problem.
const ProblemName = "first nonrepeating"

// firstNonrepeating finds the first element of the array which is not
// repeated later in the array.
func firstNonrepeating(a []int) (int, error) {
	if len(a) < 2 {
		return 0, fmt.Errorf("input must be >= 2 ints")
	}

	counts := make(map[int]int)
	for _, v := range a {
		counts[v]++
	}

	for _, v := range a {
		if counts[v] == 1 {
			return v, nil
		}
	}

	return 0, fmt.Errorf("Could not find any non-repeating ints.")
}

func printTry() {
	fmt.Printf("%s in go: try 'go test'.\n", ProblemName)
}

func main() {
	printTry()
}
