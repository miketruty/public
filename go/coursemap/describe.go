// describe subcommand.
package main

import "fmt"

// coursemapDescribeCourse prints information about the coursemap template file.
func coursemapDescribeCourse(y string) int {
	result := 0
	lab_i := 1

	// TODO(truty): let's do some REAL YAML parsing now!!
	//              problably need a struct def for the base course bundle yaml
	//              schema.
	qlconfig := parseCourseYaml(readFile(y))

	fmt.Println("----------------------------------------")
	fmt.Printf("entity_type:\n%s\n", qlconfig.EntityType)
	fmt.Println("----------------------------------------")
	fmt.Printf("schema_version:\n%d\n", qlconfig.SchemaVersion)
	fmt.Println("----------------------------------------")
	fmt.Printf("default_locale:\n%s\n", qlconfig.DefaultLocale)
	fmt.Println("----------------------------------------")
	fmt.Printf("badge:\n%s\n", qlconfig.Badge)
	fmt.Println("----------------------------------------")
	fmt.Printf("title:\n%s\n", qlconfig.Title)
	fmt.Println("----------------------------------------")
	fmt.Printf("description:\n%s\n", qlconfig.Description)
	fmt.Println("----------]------------------------------")
	fmt.Printf("level:\n%d\n", qlconfig.Level)
	fmt.Println("----------------------------------------")
	fmt.Printf("objectives:\n%s\n", qlconfig.Objectives)
	fmt.Println("----------------------------------------")
	for _, r := range qlconfig.Resources {
		fmt.Printf("  Resource: %s, %s, %s, %s.\n", r.Type, r.ID, r.Title, r.URI)
	}
	fmt.Println("----------------------------------------")
	for i, m := range qlconfig.Modules {
		fmt.Printf("  Module %d. %s.\n", i, m.Title)
		fmt.Printf("    %s.\n", m.Description)
		fmt.Printf("    %s.\n", m.Objectives)
		for _, s := range m.Steps {
			for _, a := range s.ActivityOptions {
				if a.Type == "lab" {
					fmt.Printf("    Lab %d. %s.\n", lab_i, buildStepLabLink(a.ID))
					lab_i++
				}
			}
		}
	}
	fmt.Println("----------------------------------------")

	return result
}

// coursemapDescribeLab prints information about the lab template file.
func coursemapDescribeLab(y string) int {
	result := 0

	// TODO(truty): let's do some REAL YAML parsing now!!
	//              problably need a struct def for the base course bundle yaml
	//              schema.
	qlconfig := parseLabYaml(readFile(y))

	fmt.Println("----------------------------------------")
	fmt.Printf("schema_version:\n%d\n", qlconfig.SchemaVersion)
	fmt.Println("----------------------------------------")
	fmt.Printf("title:\n%s\n", qlconfig.Title)
	fmt.Println("----------------------------------------")
	fmt.Printf("description:\n%s\n", qlconfig.Description)
	fmt.Println("----------------------------------------")
	fmt.Printf("default_locale:\n%s\n", qlconfig.DefaultLocale)
	fmt.Println("----------------------------------------")
	fmt.Printf("duration:\n%d\n", qlconfig.Duration)
	fmt.Println("----------------------------------------")
	fmt.Printf("max duration:\n%d\n", qlconfig.MaxDuration)
	fmt.Println("----------------------------------------")
	fmt.Printf("level:\n%s\n", qlconfig.Level)
	fmt.Println("----------------------------------------")
	fmt.Printf("tags[]:\n%v\n", qlconfig.Tags)
	fmt.Println("----------------------------------------")
	fmt.Printf("tagline:\n%s\n", qlconfig.Tagline)
	fmt.Println("----------------------------------------")
	fmt.Printf("resources[]:\n%v\n", qlconfig.Resources)
	fmt.Println("----------------------------------------")
	fmt.Printf("environment resources[]:\n%v\n", qlconfig.EnvironmentResources)
	fmt.Println("----------------------------------------")
	fmt.Printf("assessment:\n%s\n", qlconfig.Assessment)
	fmt.Println("----------------------------------------")
	/*
		fmt.Println("----------------------------------------")
		fmt.Printf("badge:\n%s\n", qlconfig.Badge)
		fmt.Println("----------------------------------------")
		fmt.Printf("objectives:\n%s\n", qlconfig.Objectives)
		fmt.Println("----------------------------------------")
		fmt.Printf("modules[]:\n%v\n", qlconfig.Modules)
		fmt.Println("----------------------------------------")
	*/

	return result
}
