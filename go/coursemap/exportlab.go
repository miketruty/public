// xcourse (export course to csv) subcommand.
package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

func validateLab(c *QwiklabsLabYaml) error {
	if c.SchemaVersion != 1 && c.SchemaVersion != 2 {
		return fmt.Errorf("This is not a supported SchemaVersion!")
	}

	if c.DefaultLocale != "en" {
		return fmt.Errorf("Only en is a supported DefaultLocale at this time.")
	}
	return nil
}

func buildLabDesc(description string, duration int) string {
	return fmt.Sprintf("%s\n\nDuration: %d.", description, duration)
}

func buildLabSub(subtitle string, level string, y string) string {
	if strings.Index(y, "gcp-spl-content") != -1 {
		return subtitle + " Level: " + level + " SPL"
	}
	return subtitle + " Level: " + level + " lab"
}

// coursemapExportLab exports details from the lab template to csv.
func coursemapExportLab(y string) int {
	result := 0

	qlLab := parseLabYaml(readFile(y))
	if err := validateLab(qlLab); err != nil {
		log.Fatal(fmt.Sprintf("Error with %s: %s", y, err))
	}

	speakers := ""
	badge := "" // the badge icons are visible from the app so stub this
	vid := ""

	// qlCourse.Resources) - Not yet used

	csvRecordOut(os.Stdout, buildUid(qlLab.Title), qlLab.Title, buildLabSub(subLab, qlLab.Level, y), speakers, buildLabDesc(qlLab.Description, qlLab.Duration), buildUpdated(y), buildYamlLink(y), strings.Join(qlLab.Tags, ","), badge, vid)

	return result
}
