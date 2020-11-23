// xcourse (export course to csv) subcommand.
package main

import (
	"fmt"
	"log"
	"os"
	"strings"
)

func validateCourse(c *QwiklabsCourseYaml) error {
	if c.EntityType != "CourseTemplate" {
		return fmt.Errorf("This is not a CourseTemplate!")
	}

	if c.SchemaVersion != 1 {
		return fmt.Errorf("This is not a supported SchemaVersion!")
	}

	if c.DefaultLocale != "en" {
		return fmt.Errorf("Only en is a supported DefaultLocale at this time.")
	}
	return nil
}

func buildCourseDesc(c *QwiklabsCourseYaml) string {
	d := []string{}
	d = append(d, c.Description)
	d = append(d, c.Objectives)

	lab_i := 1

	for i, m := range c.Modules {
		d = append(d, fmt.Sprintf("  Module %d. %s", i, m.Title))
		d = append(d, fmt.Sprintf("    %s", m.Description))
		d = append(d, fmt.Sprintf("    %s", m.Objectives))
		for _, s := range m.Steps {
			for _, a := range s.ActivityOptions {
				if a.Type == "lab" {
					d = append(d, fmt.Sprintf("    Lab %d. %s", lab_i, buildStepLabLink(a.ID)))
					lab_i++
				}
			}
		}
		if lab_i > 1 {
			d = append(d, "\n")
		}
	}
	return strings.Join(d, "\n")
}

func buildModuleDesc(m Module) string {
	d := []string{}
	lab_i := 1
	d = append(d, fmt.Sprintf(m.Description))
	d = append(d, fmt.Sprintf(m.Objectives))
	for _, s := range m.Steps {
		for _, a := range s.ActivityOptions {
			if a.Type == "lab" {
				d = append(d, fmt.Sprintf("    Lab %d. %s", lab_i, buildStepLabLink(a.ID)))
				lab_i++
			}
		}
	}
	if lab_i > 1 {
		d = append(d, "\n")
	}
	return strings.Join(d, "\n")
}

// coursemapExportCourse exports details from the course template to csv.
func coursemapExportCourse(y string) int {
	result := 0

	qlCourse := parseCourseYaml(readFile(y))
	if err := validateCourse(qlCourse); err != nil {
		log.Fatal(fmt.Sprintf("Error with %s: %s", y, err))
	}

	speakers := ""
	tags := ""
	vid := ""

	// qlCourse.Resources) - Not yet used

	csvRecordOut(os.Stdout, buildUid(qlCourse.Title), qlCourse.Title, buildSub(subCourse, qlCourse.Level), speakers, buildCourseDesc(qlCourse), buildUpdated(y), buildYamlLink(y), tags, qlCourse.Badge, vid)

	for i, m := range qlCourse.Modules {
		title := fmt.Sprintf("%s: Module %d - %s", qlCourse.Title, i, m.Title)
		csvRecordOut(os.Stdout, buildUid(qlCourse.Title+m.Title), title, buildSub(subModule, qlCourse.Level), speakers, buildModuleDesc(m), buildUpdated(y), buildYamlLink(y), tags, qlCourse.Badge, vid)
	}

	return result
}
