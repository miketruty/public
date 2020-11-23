// Test ProblemName
package main

import (
	"testing"
)

type tupleResult struct {
	first     int
	expectErr bool
}

var tests = []struct {
	inName string
	in     []int
	out    tupleResult
}{
	{"simple 0 elems", []int{}, tupleResult{0, true}},
	{"simple 1 elems", []int{0}, tupleResult{0, true}},
	{"simple 3a", []int{3, 3, 3, 3, 2}, tupleResult{2, false}},
	{"simple 5a", []int{-1, 2, -1, 3, 2}, tupleResult{3, false}},
	{"simple 6a", []int{9, 4, 9, 6, 7, 4}, tupleResult{6, false}},
	{"nononrepeating", []int{1, 9, 3, 4, 4, 3, 9, 1, 1, 4}, tupleResult{0, true}},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			nr, err := firstNonrepeating(tt.in)
			result := tupleResult{nr, err != nil}
			if result != tt.out {
				t.Errorf("got %v, want %v", result, tt.out)
			}
		})
	}
}

// Example functions are documentation.
// They demonstrate proper output of execution.
// They're run just like Tests as well, and printed with godoc package docs.
func ExamplePrint() {
	printTry()
	// Output: first nonrepeating in go: try 'go test'.
}
