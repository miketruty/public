// Test ProblemName
package main

import (
	"testing"
)

type tupleResult struct {
	smallest  int
	second    int
	expectErr bool
}

var tests = []struct {
	inName string
	in     []int
	out    tupleResult
}{
	{"simple 0 elems", []int{}, tupleResult{0, 0, true}},
	{"simple 1 elems", []int{0}, tupleResult{0, 0, true}},
	{"simple 3a", []int{0, 1, 2}, tupleResult{0, 1, false}},
	{"simple 3b", []int{-1, 0, 1}, tupleResult{-1, 0, false}},
	{"simple 3c", []int{-99, -22, -34}, tupleResult{-99, -34, false}},
	{"simple 3c", []int{99, 22, -77}, tupleResult{-77, 22, false}},
	{"simple 4a", []int{99, 22, -77, 100}, tupleResult{-77, 22, false}},
	{"reversed 10", []int{99, 82, 77, 60, 56, 48, 31, 20, 12, 7}, tupleResult{7, 12, false}},
	{"equal4a", []int{2, 3, 3, 4}, tupleResult{2, 3, false}},
	{"equal4b", []int{2, 3, 3, 2}, tupleResult{2, 2, false}},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			s1, s2, err := secondSmallest(tt.in)
			result := tupleResult{s1, s2, err != nil}
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
	// Output: second smallest in go: try 'go test'.
}
