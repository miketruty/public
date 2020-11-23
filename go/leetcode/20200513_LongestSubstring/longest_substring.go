// Given a string, find the length of the longest substring without repeating
// characters.
//
// Example 1:
//
// Input: "abcabcbb"
// Output: 3
// Explanation: The answer is "abc", with the length of 3.
//
// Example 2:
//
// Input: "bbbbb"
// Output: 1
// Explanation: The answer is "b", with the length of 1.
//
// Example 3:
//
// Input: "pwwkew"
// Output: 3
// Explanation: The answer is "wke", with the length of 3.
//              Note that the answer must be a substring, "pwke" is a
//              subsequence and not a substring.
package main

import "fmt"

// NOTE: I did a bunch of exploring to use bit-masks to track the characters
//       efficiently. In the end I decided that there are actually more than
//       26 characters (upper, lower, numbers) so it was more work to set up
//       a mess of consts and a map, etc. The efficient alternative/approach
//       is to just use a set to capture characters used.

// NOTE: This is a pretty cool demo of using a map as a set. Notice the value is
// an efficient empty string which consumes 0 bytes and is aliased with
// "exists".

// lengthFromHere returns the length of the longest sequence of unique
// characters starting/including the first character; substrings are not
// considered.
func lengthFromHere(s string) int {
	var exists = struct{}{}
	seen := make(map[rune]struct{})

	for i, c := range s {
		if _, ok := seen[c]; ok {
			return i
		}
		seen[c] = exists
	}

	return len(s)
}

// lengthOfLongestSubstring returns the length of the longest string of unique
// characters found.
func lengthOfLongestSubstring(s string) int {
	result := 0
	longestStart := 0

	for i := 0; i < len(s); i++ {
		newResult := lengthFromHere(s[i:])
		if newResult > result {
			result = newResult
			longestStart = i
		}
		if result >= len(s)-i {
			break
		}
	}

	fmt.Printf("In %s, longest substring of %d was %s.\n",
		s, result, s[longestStart:longestStart+result])
	return result
}

func main() {
	fmt.Println("lengthOfLongestSubstring: try 'go test -test.v'")
}
