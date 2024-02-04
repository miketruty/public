// Test longestSubstring
package main

import "testing"

var tests = []struct {
	inName string
	in     string
	out    int
}{
	{"simple 0", "", 0},
	{"simple 1a", "aaa", 1},
	{"simple 1b", "a", 1},
	{"simple 1c", "", 0},
	{"simple 2a", "aaabbbb", 2},
	{"simple 3a", "abccbbb", 3},
	{"simple 3b", "aaababc", 3},
	{"simple 3c", "aaabccc", 3},
}

func TestLengthOfLongestSubstrings(t *testing.T) {
	for _, tt := range tests {
		t.Run(tt.inName, func(t *testing.T) {
			result := lengthOfLongestSubstring(tt.in)
			if result != tt.out {
				t.Errorf("%s got %v, want %v", tt.inName, result, tt.out)
			}
		})
	}
}
