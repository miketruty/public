// Test twoSum
package main

import (
	"testing"
)

var tests = []struct {
	inName   string
	inNums   []int
	inTarget int
	out      []int
}{
	{"simple 2a", []int{0, 1}, 1, []int{0, 1}},
	{"simple 2b", []int{1, 0}, 1, []int{0, 1}},
	{"simple 3a", []int{1, 2, 3}, 3, []int{0, 1}},
	{"simple 3b", []int{1, 2, 3}, 5, []int{1, 2}},
	{"simple 3c", []int{1, 2, 3}, 4, []int{0, 2}},
	{"simple 4a", []int{3, 2, 1, 0}, 5, []int{0, 1}},
	{"simple 4b", []int{3, 2, 1, 0}, 3, []int{0, 3}},
	{"simple 4c", []int{3, 2, 1, 0}, 1, []int{2, 3}},
	{"simple 4c", []int{3, 2, 1, 0}, 4, []int{0, 2}},
	{"simple 4d", []int{3, 2, 1, 0}, 2, []int{1, 3}},
	{"negs 2a", []int{-3, -2, -1, 0}, -5, []int{0, 1}},
	{"negs 2b", []int{-3, -2, -1, 0}, -3, []int{0, 3}},
	{"negs 2b", []int{-3, -2, -1, 0}, -2, []int{1, 3}},
}

func outEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, v := range a {
		if v != b[i] {
			return false
		}
	}
	return true
}

func TestTwoSum(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			result := twoSum(tt.inNums, tt.inTarget)
			if !outEqual(result, tt.out) {
				t.Errorf("%s got %v, want %v", tt.inName, result, tt.out)
			}
		})
	}
}
