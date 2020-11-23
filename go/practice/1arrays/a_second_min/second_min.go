// Write an efficient C program to find smallest and second smallest element in an array.k
//
// INPUT FORMAT
//   []int
//
// OUTPUT FORMAT
//   (int, int, error)
//
// SAMPLE INPUT
//   1, 10, 2, 9, 3, 8, 4, 7, 5, 6
//
// SAMPLE OUTPUT
//   1, 2
//
package main

import (
	"fmt"
)

// ProblemName is the package-level label of the coding problem.
const ProblemName = "second smallest"

// secondSmallest finds the smallest and second-smallest ints in an
// array of ints. It returns an error if passed an array of less than
// 2 ints. It handles negative ints.
func secondSmallest(a []int) (int, int, error) {
	if len(a) < 2 {
		return 0, 0, fmt.Errorf("input must be >= 2 ints")
	}

	var s1, s2 int

	if a[0] < a[1] {
		s1 = a[0]
		s2 = a[1]
	} else {
		s1 = a[1]
		s2 = a[0]
	}

	for _, num := range a[2:] {
		if num < s1 {
			s2 = s1
			s1 = num
		} else if num < s2 {
			s2 = num
		}
	}

	return s1, s2, nil
}

func printTry() {
	fmt.Printf("%s in go: try 'go test'.\n", ProblemName)
}

func main() {
	printTry()
}
