// Utility functions for exporting csvs
package main

import (
	"encoding/csv"
	"hash/fnv"
	"io"
	"log"
)

func fingerprint(b []byte) uint64 {
	hash := fnv.New64a()
	hash.Write(b)
	return hash.Sum64()
}

func csvOut(w io.Writer, r []string) {
	cw := csv.NewWriter(w)
	if err := cw.Write(r); err != nil {
		log.Fatal(err)
	}
	cw.Flush()
	if err := cw.Error(); err != nil {
		log.Fatal(err)
	}
}
