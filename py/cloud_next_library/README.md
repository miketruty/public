# gcp-next-reviewdeo

## Useful scripts:

### Processing metadata csv files downloaded from Drive

*   create_metadata_files.py
    *   Generate many smaller metadata files from single curated metadata csv.
    *   Allows individual owners to edit their own metadata.
    *   *Expects NO HEADER row.*
    *   Creates one JSON file for each content entity with name using category
        (next, arch, ...) + video_id.
    *   Writes json files to tempdir.
    *   Also produces `cl_data.json` which includes text for the cl description.
    *   These kept in `data/reviewdeo`
    *   Example1: `./create_metadata_files.py -c
        /tmp/gcpnext2018_session_metadata.csv -t video`
    *   Example1: `./create_metadata_files.py -c /tmp/solutions.csv -t arch`

### Move created files under data dir.

*   move the created files to a working directory.
    *   `mv /tmp/reviewdeoXXX/ ./data/reviewdeo`

### Export data dir files to metadata files (as individual CLs).

*   export_reviews.py
    *   `./export_reviews_all_truty.py -r ./data/reviewdeo/`
    *   Uses a file, `cl_data.json`, under the `data/reviewdeo` directory.
    *   `cl_data.json` includes details for CL description.
    *   General workflow
        *   Foreach video_id
            *   git create branch
            *   copy file from review directory (`data/reviewdeo`) to final
                metadata directory (`metadata`).
            *   git add file
            *   git commit file
            *   Git5 export the file/cl
            *   Git5 mail
            *   (optional) Git5 drop

### Submit google3 CLs

*   submit_updates.py
    *   Uses a `branchlist` file.
    *   Submit CLs checked out earlier with `export_reviews.py`.
    *   General workflow
        *   Foreach branch
            *   git checkout branch
            *   Git5 sync
            *   Git5 submit
            *   git checkout master
            *   Git5 sync (merge change to master)
            *   git delete non-master branch

### Building final metadata csv file for deployment

*   assemble_new_metadata_file.py

    *   Starts with the latest hand curated metadata file, from drive.
    *   Adds all the smaller, individual metadata file data to one large output
        csv.
    *   Allows you to notice changes since last publish.
    *   Example: `./assemble_new_metadata_file.py -o ./data/new_metadata_x.csv
        -j ./metadata`

### Misc scripts

*   retrieve_youtube_metadata.py
    *   Use YouTube data API and fixed set of playlists of Next videos.
    *   Used for gathering data for videos from: next2016, next2017.
    *   To show where published metadata is incorrect.
    *   Creates output file yt_meta\*csv with current metadata.
    *   Enable YouTube Data API v3
        *   GCP Console > APIs & Services > Enable APIs and Services
        *   YouTube Data API v3
        *   Enable API
        *   You may need to wait 3-4min for propagation.
    *   Requires an API key:
        *   GCP Console > APIs & Services > Credentials
        *   Create API Key
        *   Copy key for command line use
    *   Requires Python API client:

    ```
    sudo apt-get install python3-pip
    sudo pip3 install virtualenv
    virtualenv -p /usr/bin/python2.7 venv
    source venv/bin/activate
    pip install --upgrade google-api-python-client
    find ./venv/ -iname 'googleapiclient*'
    find ./venv/ -iname 'apiclient*'
    ```

    *   Run the command:
        *   `python ./retrieve_youtube_metadata.py -k [API_KEY]`
    *   Deactivate virtualenv
        *   `deactivate`
    *   Use the file file created under /tmp/yt_metaxxx.
*   compare_csvs.py
    *   For comparing 2 csv files where the first field of every file is a
        video_id.
    *   The sets of video_ids of each csv file are compared.
    *   Diff result is printed.

### Getting dev_appserver.py to work

*   dev_appserver.py just works out of the box fine on corp gLinux. Needed
    extensions are auto-installed.
*   Work around a bug finding files in GCS:
    *   `cp ../data/output/new_metaxxx.csv ./data/video_data.csv`
*   The following used for gLaptop:

    *   Install local developer extensions.
    `sudo apt-get install google-cloud-sdk-app-engine-python google-cloud-sdk-app-engine-python-extras google-cloud-sdk-datastore-emulator`
    *   dev_appserver.py is used for running App Engine on your local machine.
    *   dev_appserver.py requires python2.7
    *   The usual fix is `export CLOUDSDK_PYTHON=/usr/bin/python2.7`
    *   But this doesn't work.
    *   So I edited dev_appserver.py:
    *   change `/usr/bin/env python` to `/usr/bin/env python2`
    *   Run it: `/usr/lib/google-cloud-sdk/bin/dev_appserver.py app.yaml`
    *   Note: the datastore is empty.
