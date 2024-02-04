// Test findMedianSortedArrays
package main

import "testing"

var tests = []struct {
	in_name  string
	in_nums1 []int
	in_nums2 []int
	out      float32
}{
	{"simple 2a", []int{1, 3}, []int{2}, 2.0},
	{"simple 2b", []int{1, 2}, []int{3, 4}, 2.5},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.in_name, func(t *testing.T) {
			result := findMedianSortedArrays(tt.in_nums1, tt.in_nums2)
			if result != tt.out {
				t.Errorf("got %v, want %v", result, tt.out)
			}
		})
	}
}
