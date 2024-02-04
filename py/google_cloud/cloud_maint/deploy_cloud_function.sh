# Deploy example Cloud Function - helloworld
pushd /Users/mxt0623/src/github.com/GoogleCloudPlatform/python-docs-samples/functions/helloworld
gcloud functions deploy dexcom-vnv-testrail-webhook \
    --gen2 --runtime=python312 \
    --region=us-west1 --source=. \
    --entry-point=hello_get \
    --trigger-http
popd
