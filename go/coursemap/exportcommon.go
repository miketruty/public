// export common utility functions
package main

import (
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strconv"
	"strings"
)

const subCourse = "qlCourse"
const subModule = "qlModule"
const subLab = "qlLab"
const subQuest = "qlQuest"

func csvRecordOut(w io.Writer, uid, title, subtitle, speakers, desc, updated, link, tags, badge, vid string) {
	/*
	   FIELD_UNIQUE_ID,   generated
	   FIELD_TITLE,       .Title
	   FIELD_EVENT,       "learning"
	   FIELD_VIEW_COUNT,  0
	   FIELD_SUBTITLE,    ""
	   FIELD_DURATION,    0
	   FIELD_SPEAKERS,    ""
	   FIELD_DESC,        .Description
	   FIELD_PUB_DATE,    today as "2019-04-10 14:10:00"
	   FIELD_SLIDES_LINK, "https://google.qwiklabs.com"
	   FIELD_TAGS,        "tags" // indexed but not shown
	   FIELD_IMAGE,       .Badge // badge doesn't work - just stub this.
	   FIELD_VIDEO_ID,    ""
	   FIELD_SESSION_ID,  ""
	*/

	record := []string{
		uid,
		title,
		"learning",
		"0",
		subtitle,
		"0",
		speakers,
		desc,
		updated,
		link, // slide link
		tags,
		"/static/logo_google_cloud.svg",
		vid,
		"",
	}

	csvOut(w, record)
}

func buildUid(title string) string {
	// FIELD_UNIQUE_ID,
	// I'd prefer to use the course name for unique id,
	// but for expediency lets generate one from the title.
	return strconv.FormatUint(fingerprint([]byte(title)), 10)
}

func buildSub(subtitle string, level int) string {
	s := strconv.Itoa(level)
	if level == 0 {
		s = "Introductory"
	} else if level == 1 {
		s = "Fundamental"
	} else if level == 2 {
		s = "Intermediate"
	} else if level == 3 {
		s = "Advanced"
	} else if level == 4 {
		s = "Expert"
	}

	return subtitle + " Level: " + s
}

func runGitLogFile(fn string) (string, error) {
	if err := os.Chdir(filepath.Dir(fn)); err != nil {
		return "", fmt.Errorf("cannot cd for %s: %s", fn, err)
	}

	// strip output downto the date, in format: 2020-05-01 12:43:56
	gargs := []string{"log", "-1", "--format=%cd", "--date=format:%Y-%m-%d %H:%M:%S", "."}
	cmdOut, err := exec.Command("git", gargs...).Output()
	if err != nil {
		return "", fmt.Errorf("error with git %s: %s", strings.Join(gargs, " "), err)
	}

	return string(cmdOut), nil
}

func buildUpdated(y string) string {
	s, err := runGitLogFile(y)
	if err != nil {
		fmt.Println(err)
	}
	return strings.TrimSpace(s)
}

func buildYamlLink(y string) string {
	// Create a GitHub link from a full file path.

	var s string
	if i := strings.Index(y, "/course_templates/"); i != -1 {
		s = strings.Replace(y, "/course_templates/", "/blob/master/course_templates/", 1)
	}

	if len(s) == 0 {
		if i := strings.Index(y, "/learning_paths/"); i != -1 {
			s = strings.Replace(y, "/learning_paths/", "/blob/master/learning_paths/", 1)
		}
	}

	if len(s) == 0 {
		if i := strings.Index(y, "/labs/"); i != -1 {
			s = strings.Replace(y, "/labs/", "/blob/master/labs/", 1)
		}
	}

	// Yank directory info prior to github.com
	i := strings.Index(s, "github.com")
	if i == -1 {
		return ""
	}

	return "https://" + s[i:]
}

func buildStepLabLink(lab string) string {
	// Create a GitHub link from an abridged module step lab link.
	// labs in module steps from course templates and spl quest templates:
	//   course_templates: gcp-training-content/CBL140-ClusterViaConsole-3
	//   learning_paths: gcp-spl-content/gsp664-ServiceMesh-SingleCluster

	var s string
	if len(s) == 0 {
		if i := strings.Index(lab, "gcp-training-content/"); i == 0 {
			s = strings.Replace(lab, "gcp-training-content/", "github.com/CloudVLab/gcp-training-content/blob/master/labs/", 1)
		}
	}

	if len(s) == 0 {
		if i := strings.Index(lab, "gcp-spl-content/"); i == 0 {
			s = strings.Replace(lab, "gcp-spl-content/", "github.com/CloudVLab/gcp-spl-content/blob/master/labs/", 1)
		}
	}

	// Yank directory info prior to github.com
	i := strings.Index(s, "github.com")
	if i == -1 {
		return ""
	}

	return "https://" + s[i:]
}
