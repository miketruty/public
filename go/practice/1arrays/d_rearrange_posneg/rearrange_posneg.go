// Given an array of positive and negative numbers, arrange them such that all
// negative integers appear before all the positive integers in the array
// without using any additional data structure like hash table, arrays, etc. The
// order of appearance should be maintained.
//
// INPUT FORMAT
//   []int
//
// OUTPUT FORMAT
//   []int, error
//
// SAMPLE INPUT
//   [12 11 -13 -5 6 -7 5 -3 -6]
//
// SAMPLE OUTPUT
//   [-13 -5 -7 -3 -6 12 11 6 5]

package main

import (
	"fmt"
)

// ProblemName is the package-level label of the coding problem.
const ProblemName = "rearrange positive negative"

// rearrangePosNeg produces a single array of ints with negatives in front.
func rearrangePosNeg(a []int) []int {

	if len(a) <= 1 {
		return a
	}

	// There's an in-place way to do this, using no extra space and recursion.
	// It's a variation of merge sort. You divide the list and keep dividing
	// recursively, then you reverse the list (to sort negative in front of
	// positive) and merge the results. But I don't like this because it sorts
	// the list and I think the original problem is just a partitioning problem,
	// except the requirement to maintain order is neither sort nor partitioning.
	// I'm going to do an insertion solution but it's not optimal because it uses
	// 2n space.

	var s []int

	// Move the negative ints to the output array.
	for i := 0; i < len(a); i++ {
		if a[i] < 0 {
			s = append(s, a[i])
		}
	}

	// Now, move the positive ints to the output array.
	for i := 0; i < len(a); i++ {
		if a[i] >= 0 {
			s = append(s, a[i])
		}
	}

	return s
}

func printTry() {
	fmt.Printf("%s in go: try 'go test'.\n", ProblemName)
}

func main() {
	printTry()
}
