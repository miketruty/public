# Frequently used commands.

## App related

### Deploy app

```
$ cd src
$ gcloud app deploy app.yaml --project gcp-next-reviewdeo
$ gcloud app deploy app.yaml --project google.com:cloud-next-library
$ gcloud app deploy app.yaml --project google.com:cloud-next-library --no-promote
```

### Follow logging

```
$ gcloud app logs tail -s default
```

## Data file related

### Download steps for curated csvs.

*   Download csv
*   Move to data/input/gcpnext2019_session_metadata_2019xxxx.csv
*   Edit and remove header row

### (optional) Remove the existing new_metadata_.csv.

```
$  rm ./data/output/new_metadata_20170410.csv
```

### Create new json files from curated csv.

```
$  rm ./metadata/arch/arch*
$  mv ./metadata/next2019 /tmp
$  mkdir ./metadata/next2019
$ ./create_metadata_files.py -c /tmp/solutions.csv -t arch
$ ./create_metadata_files.py -c /tmp/next2019.csv -t video
$ ./create_metadata_files.py -c ./data/input/gcpnext2019_session_metadata_20190305.csv -t video
```

### Copy the new metadata.

```
$  mv /tmp/reviewdeoYID8YQ/arch* ./metadata/arch/
$  mv /tmp/reviewdeoXXXXXX/* ./metadata/next2019
```

#### I had to move the flat json files into a directory structure.

*   Use vim macros to create a directory for each.
*   Also had to rm cl_data.json

### Cleanup the metadata working dir.

```
$  rm -rf /tmp/reviewdeoYID8YQ/
```

### Create new csv from metadata+files.

```
$ ./assemble_new_metadata_file.py -o ./data/input/curated_video_data.csv -j ./metadata
$ ./assemble_new_metadata_file.py -o ./data/input/last_good_data.csv -j ./metadata
$ ./assemble_new_metadata_file.py -o ./data/input/gcpnext2018_session_metadata_20180812_curated.csv -j ./metadata/
```

### Save the new csv.

```
$  mv /tmp/new_metaFZfl7N.csv ./data/output/new_metadata_20170410.csv
```

### Setup for local testing.

```
$  unlink video_data.csv
$  ln -s ./new_metadata2019_20190305.csv ./src/data/video_data.csv
$  cd src
$  dev_appserver.py ./app.yaml

-http://localhost:8080
-Admin > reset
```

#### Deploy/push video metadata file to prod.

```
$ gsutil cp ./data/new_metadata_20170410.csv gs://cloud-next-library.google.com.a.appspot.com/video_data.csv
$ gsutil cp ./data/output/new_metadata2019_20190410.csv gs://cloud-next-library.google.com.a.appspot.com/video_data.csv
```

### View video metadata file access permissions.

```
$ gsutil acl get gs://gcp-next-reviewdeo.appspot.com/video_data.csv
$ gsutil acl get gs://cloud-next-library.google.com.a.appspot.com/video_data.csv
```

## Procedure for deploying updated metadata using coursemap parsing

1.  Parse the yaml files and create updated metadata files
    from `~/src/github.com/miketruty/spas/go/coursemap`.

    ```
    ./gen_coursemodulelab_csvs.sh
    ```

    This creates files in `/tmp`:

    ```
    /tmp/2020xxyy_coursesmodules.csv
    /tmp/2020xxyy_labs.csv
    /tmp/2020xxyy_spls.csv
    /tmp/2020xxyy_quests.csv
    ```

2.  Copy generated files and concat into one large metadata file
    from `~/src/google3/cloud-next-library/data/output`.


    ```
    ./combine_next_coursesmodulessplslabs.sh
    ```

    This creates the file `new_metadata2020_2020xxyy.csv`.

3.  Copy metadata to prod bucket.

    ```
    gsutil cp ./new_metadata2020_2020xxyy.csv gs://cloud-next-library.google.com.a.appspot.com/video_data.csv
    ```

4.  Re-ingest metadata to index from
    [goto/cloud-courses](http://goto/cloud-courses)

    *   Hamburger menu > Admin Tasks
    *   __Reset Metadata Index__

5.  Test update after about 3minutes from
    [goto/cloud-courses](http://goto/cloud-courses)

    *   Check courses
    *   Check modules
    *   Check quests
    *   Check SPLs
    *   Check labs

## Not a frequently used command but worth remembering.

### Enable audit-logging for the application

With audit-logging enabled, can notice users who violate any IAP rules.
[References](https://cloud.google.com/iap/docs/audit-log-howto).

__Prefer__ using the Console UI to this gcloud way.

The gcloud way:

Add this to the policy:

```
auditConfigs:
- auditLogConfigs:
  - logType: ADMIN_READ
  - logType: DATA_READ
  - logType: DATA_WRITE
  service: allServices
```

Use the following commands:

```
 gcloud projects get-iam-policy google.com:cloud-next-library > policy.yaml
 <add policy>
 gcloud projects set-iam-policy google.com:cloud-next-library policy.yaml
```

### Add PubSub notification when metadata file changed.

```
$ gsutil notification create -e OBJECT_FINALIZE \
  -t "projects/gcp-next-reviewdeo/topics/metadata-file-updated" \
  -f json gs://gcp-next-reviewdeo.appspot.com/
```

### Check your PubSub notification.

```
$ gsutil notification list gs://gcp-next-reviewdeo.appspot.com/
```
