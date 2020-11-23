// Test isPalindrome
package main

import "testing"

var tests = []struct {
	inName string
	in     int
	out    bool
}{
	{"simple 1a", 0, true},
	{"simple 1b", 1, true},
	{"simple 1c", -1, false},
	{"simple 1d", 9, true},
	{"simple 2a", -99, false},
	{"simple 2b", 10, false},
	{"simple 2c", 11, true},
	{"simple 2d", 99, true},
	{"simple 3a", -323, false},
	{"simple 3b", 323, true},
	{"simple 3c", 999, true},
	{"simple 3d", 998, false},
	{"simple 3e", 110, false},
	{"simple 3f", -101, false},
	{"simple 4a", 1221, true},
	{"simple 4b", 1001, true},
	{"simple 5a", 10201, true},
	{"simple 5b", 21211, false},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			result := isPalindrome(tt.in)
			if result != tt.out {
				t.Errorf("%s got %v, want %v", tt.inName, result, tt.out)
			}
		})
	}
}
