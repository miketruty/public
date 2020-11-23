package util

import (
	"fmt"
	"os"
	"path/filepath"
)

// FileExists does the work of looking for a file.
func FileExists(fn string) error {
	fp, err := filepath.Abs(fn)
	if err != nil {
		return err
	}

	info, err := os.Stat(fp)
	if os.IsNotExist(err) || info.IsDir() {
		return fmt.Errorf("cannot find file %s", fp)
	}
	return nil
}
