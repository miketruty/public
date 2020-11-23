// xcourse (export course to csv) subcommand.
package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

func validateQuest(c *QwiklabsQuestYaml) error {
	if c.EntityType != "LearningPath" {
		return fmt.Errorf("this is not a LearningPath")
	}

	if c.SchemaVersion != 1 {
		return fmt.Errorf("this is not a supported SchemaVersion")
	}

	if c.DefaultLocale != "en" {
		return fmt.Errorf("only en is a supported DefaultLocale at this time")
	}
	return nil
}

func buildQuestDesc(c *QwiklabsQuestYaml) string {
	d := []string{}
	d = append(d, c.Description)
	d = append(d, c.Objectives)

	labNum := 1

	for i, m := range c.Modules {
		d = append(d, fmt.Sprintf("  Module %d. %s", i, m.Title))
		d = append(d, fmt.Sprintf("    %s", m.Description))
		for _, s := range m.Steps {
			for _, a := range s.ActivityOptions {
				if a.Type == "lab" {
					d = append(d, fmt.Sprintf("    Lab %d. %s", labNum, buildStepLabLink(a.ID)))
					labNum++
				}
			}
		}
		if labNum > 1 {
			d = append(d, "\n")
		}
	}
	return strings.Join(d, "\n")
}

// coursemapExportLab exports details from the lab template to csv.
func coursemapExportQuest(y string) int {
	result := 0

	qlQuest := parseQuestYaml(readFile(y))
	if err := validateQuest(qlQuest); err != nil {
		log.Fatal(fmt.Sprintf("Error with %s: %s", y, err))
	}

	speakers := ""
	badge := "" // the badge icons are visible from the app so stub this
	vid := ""

	csvRecordOut(os.Stdout, buildUid(qlQuest.Title), qlQuest.Title, buildSub(subQuest, qlQuest.Level), speakers, buildQuestDesc(qlQuest), buildUpdated(y), buildYamlLink(y), strings.Join(qlQuest.Tags, ","), badge, vid)

	return result
}
