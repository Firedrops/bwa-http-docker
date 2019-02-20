# bwa-http-docker
BWA alignment via HTTP requests

Don't run this on a public IP.  The BWA CGI `bwa.cgi` script allows passing commandline args to `bwa` as a POST parameter.  You've been warned!

<<<<<<< HEAD
### Legacy
contains older attempt in which everything up to japsa is handled by a python script in a docker.
=======
## `Dockerfile`
Deprecated. Will be removed or replaced with `http.Dockerfile` version in future releases.

## `http.Dockerfile`
Supports following environment variables in runtime:
- BWA_FILES - URI to download reference files from. Supports Google Cloud Storage `gs://` scheme as well as `http://`, `https://` schemes.
- REQUESTER_PROJECT - Google Cloud Platform project ID to bill for file transfer when downoading from buckets with [requester pays](https://cloud.google.com/storage/docs/requester-pays) option enabled.
>>>>>>> 36fb8c47cfc03c0e0966ea4674a4207e22eb38a2
