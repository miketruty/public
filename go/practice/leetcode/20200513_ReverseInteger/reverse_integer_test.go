// Test reverse
package main

import "testing"

var tests = []struct {
	inName string
	in     int32
	out    int32
}{
	{"simple 1a", 0, 0},
	{"simple 1b", 1, 1},
	{"simple 1c", -1, -1},
	{"simple 2a", 23, 32},
	{"simple 2b", 91, 19},
	{"simple 2c", -91, -19},
	{"simple 3a", 123, 321},
	{"simple 3b", -123, -321},
	{"simple 3c", 120, 21},
	{"simple 3d", -320, -23},
	{"nearmax", 1463847412, 2147483641},
	{"min", -1 << 31, 0},
	{"max", 1<<31 - 1, 0},
}

func TestExampleProblem(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			result := reverse(tt.in)
			if result != tt.out {
				t.Errorf("%s got %v, want %v", tt.inName, result, tt.out)
			}
		})
	}
}
