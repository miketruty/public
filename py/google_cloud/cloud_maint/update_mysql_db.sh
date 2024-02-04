#!/usr/bin/env zsh

# Handle the latest TestRail MySQL data (zip) download.

# Check for exactly one argument (the file path)
if [[ $# -ne 1 ]]; then
  echo "Error: Please provide file path to testrail-export.zip as an argument."
  exit 1
fi

download_zip_path="$1"

if [[ ! -f "$download_zip_path" ]]; then
  echo "Error: File \"$download_zip_path\" does not exist."
  exit 1
fi

echo "The file \"$download_zip_path\" exists..."

# ----------------------------------------
# 1. Extract the zip which creates a directory structure.
# ----------------------------------------
download_zip_dir="${download_zip_path:h}"
zip_file="${download_zip_path:t}"
dumps_dir="$HOME/dumps"  # Target directory

if [[ "$download_zip_dir" != "$dumps_dir" ]]; then
  mv "$download_zip_path" "$dumps_dir"
fi

pushd "$dumps_dir" > /dev/null

dumps_zip_path="$dumps_dir/$zip_file"
if [[ ! -f "$dumps_zip_path" ]]; then
  echo "Error: File \"$dumps_zip_path\" does not exist."
  exit 1
fi

# Check if exactly one directory matches the pattern
unzipped_path=$(echo $dumps_dir/2024*) > /dev/null
if [[ $#unzipped_path -gt 0 ]]; then
  echo "Error: already an unzipped directory in $dumps_dir"
  popd
  exit 1
fi

#  unzip the file
echo "Unzipping $dumps_zip_path..."
unzip "$dumps_zip_path"

# ----------------------------------------
# 2. Import to the local MySQL DB
# ----------------------------------------
unzipped_path=$(echo $dumps_dir/2024*) > /dev/null

if [[ $#unzipped_path -eq 0 ]]; then
  echo "$unzipped_path"
  echo "Error: cannot identify one unzipped directory in $dumps_dir"
  popd
  exit 1
fi

unzipped_dir="${unzipped_path:t}"
echo "Found unzipped directory: $unzipped_dir in $unzipped_path"

# Import the schema
unzipped_schema_path=$(echo $unzipped_path/databases/testrail-mysql-struct-dexcom-2024*.sql) > /dev/null 2>&1
if [[ $#unzipped_schema_path -eq 0 ]]; then
  echo "Error: cannot identify unzipped schema file in $unzipped_dir"
  popd
  exit 1
fi
echo "Importing/updating $unzipped_schema_path..."

mysql --defaults-file="$HOME/.my.cnf.root" --protocol=tcp --host=localhost --user=root --port=3306 --default-character-set=utf8 --comments --database=testrail  < "$unzipped_schema_path"

#  Import the data
unzipped_data_path=$(echo $unzipped_path/databases/testrail-mysql-data-dexcom-2024*.sql) > /dev/null 2>&1
if [[ $#unzipped_data_path -eq 0 ]]; then
  echo "Error: cannot identify unzipped data file in $unzipped_dir"
  popd
  exit 1
fi

echo "Importing/updating $unzipped_data_path..."
mysql --defaults-file="$HOME/.my.cnf.root" --protocol=tcp --host=localhost --user=root --port=3306 --default-character-set=utf8 --comments --database=testrail  < "$unzipped_data_path"

# ----------------------------------------
# 3. Zip and send files to our GCS bucket.
#    gcloud sql *can* handle gzipped files,
#    saving us storage, time copying, everyone wins!
# ----------------------------------------
gzip $unzipped_schema_path
gzip $unzipped_data_path

gzipped_schema_path="${unzipped_schema_path}.gz"
gzipped_data_path="${unzipped_data_path}.gz"

gcs_bucket="gs://dev-us-5g-vnvtestdata-1_dumps"

echo "Copying gzipped files to $gcs_bucket..."
gsutil cp -r "${gzipped_schema_path}" "$gcs_bucket"
gsutil cp -r "${gzipped_data_path}" "$gcs_bucket"

popd

# ----------------------------------------
# 4. Send our vnvdata SQL files to our GCS bucket.
#    They're just schema, small, so no need to gzip.
# ----------------------------------------
script_dir=$(dirname $0)
pushd "$script_dir" > /dev/null
pushd "../tddash/queries" > /dev/null
gsutil cp ./create_table_requirements.sql "$gcs_bucket"
gsutil cp ./create_vnvdata_db.sql "$gcs_bucket"
popd
popd


# ----------------------------------------
# 5. Now convince Cloud SQL to import the schema and data.
# ----------------------------------------
# get the name of the files only from the full paths.
gzipped_schema_file="${gzipped_schema_path:t}"
gzipped_data_file="${gzipped_data_path:t}"

gcloud -q sql import sql testrail-mysqldb "$gcs_bucket/$gzipped_schema_file" --database=testrail
gcloud -q sql import sql testrail-mysqldb "$gcs_bucket/$gzipped_data_file" --database=testrail

echo "Removing unzipped files under $unzipped_path..."
rm -rf $unzipped_path

echo Done.
