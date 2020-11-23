// Given two sorted arrays, merge them in a sorted manner.
//
// INPUT FORMAT
//   []int, []int
//
// OUTPUT FORMAT
//   []int, error
//
// SAMPLE INPUT
//   arr1[] = { 1, 3, 4, 5}, arr2[] = {2, 4, 6, 8}
//
// SAMPLE OUTPUT
//   arr3[] = {1, 2, 3, 4, 4, 5, 6, 8}
//
// SAMPLE INPUT
//   arr1[] = { 5, 8, 9}, arr2[] = {4, 7, 8}
//
// SAMPLE OUTPUT
//   arr3[] = {4, 5, 7, 8, 8, 9}

package main

import (
	"fmt"
)

// ProblemName is the package-level label of the coding problem.
const ProblemName = "merge two arrays"

// mergeTwoArrays produces a single sorted array of ints from 2 sorted arrays.
func mergeTwoArrays(a []int, b []int) ([]int, error) {

	if len(a) == 0 {
		return b, nil
	}
	if len(b) == 0 {
		return a, nil
	}

	var i, j int
	var result []int
	for i < len(a) && j < len(b) {
		if a[i] < b[j] {
			result = append(result, a[i])
			i++
		} else {
			result = append(result, b[j])
			j++
		}
	}
	if i < len(a) {
		result = append(result, a[i:]...)
	} else if j < len(b) {
		result = append(result, b[j:]...)
	}

	return result, nil
}

func printTry() {
	fmt.Printf("%s in go: try 'go test'.\n", ProblemName)
}

func main() {
	printTry()
}
