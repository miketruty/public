# coursemap

## Metadata/Tags

* Year: 2020
* Month: May
* Tags: work

## Question/Problem

Use cases:

*   Read existing course template YAML into in-memory model (structs).
*   Emit lighter-weight, normalized YAML.
*   With an option, emit Qwiklabs course bundle style YAML.

## Code Organization

This ia a go CLI but I did not use an existing go CLI framework like Cobra.
See **ofcourses** for that.

*   main
    *   coursemap.go - main, with subcommands: describe, simplify, validate, and
                       yamltojson
*   test code
    *   coursemap_test.go - test against the example starter course template in
                            gcp-ondemand-content.
*   subcommands
    *   describe.go - print some details from the course YAML.
    *   parse_yaml.go - parser of course YAML.
    *   simplify.go - try to emit simpler YAML.
    *   validate.go - code to read schema and validate a doc against it.
    *   yamltojson.go - tool for converting YAML schema to JSON schema.

## Other files

*   search.md - explain notes for creating search index.

## Processes

### Validating course YAML

Run the `validate_course_templates` script to validate current contents
of `gcp-ondemand-content/course_templates`.

### Converting YAML schemas to JSON

The course bundle spec is published publicly in GitHub:
`https://github.com/CloudVLab/qwiklabs-content-bundle-spec`.

Related to this, the Qwiklabs team has created a set of schemas for
validating course YAML against the documented bundle spec.

There's a v2 bundle spec it seems. May need to update my schema.

The go library for schema validation that I'm using (they're hard to find)
requires the schema to be in JSON. So, I wrote a YAML to JSON converter.
I run the schema YAML to JSON converter infrequently as the bundle spec
doesn't change often.

### Testing Schema test capabilities

As I was testing my schema validator, I used some simple json documents in
`schematest` to check proper validation.

## Counts

Stats:
As of Wed Nov 4, 2020 I see:

| Date     | 11/04/20 | 11/04/20 |
| qlCourse | 106      | 106      |
| qlModule | 719      | 719      |
| qlLab    | 1000+    | 1000+    |
| qlQuest  | 0        | 70       |
