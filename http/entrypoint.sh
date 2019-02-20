#!/bin/bash
set -e

if [[ -z $BWA_FILES ]]; then
    echo "\$BWA_FILES not set"
else
<<<<<<< HEAD

  if [[   $BWA_FILES =~ ^gs://    ]]; then
    echo "using gsutil to retrieve BWA_FILES='$BWA_FILES'"
    gsutil -m cp $BWA_FILES /data/ && touch /data/ok
#  if [[   $BWA_FILES =~ ^gs://    ]]; then
#  echo "mounting bucket='$BWA_FILES'"
#  gcsfuse --implicit-dirs --only-dir /NewDatabases nano-stream1 /data && touch /data/ok
  elif [[ $BWA_FILES =~ ^http://  ||  $BWA_FILES =~ ^https:// ]]; then
    echo "using wget to retrieve BWA_FILES='$BWA_FILES'"
    wget --directory-prefix=/data/ $BWA_FILES && touch /data/ok
  else
    echo "unsupported scheme for BWA_FILES='$BWA_FILES'"
  fi

=======
    if [[ $BWA_FILES =~ ^gs:// ]]; then
        echo "using gsutil to retrieve BWA_FILES='$BWA_FILES'"
        if [[ ! -z $REQUESTER_PROJECT ]]; then
            echo "$REQUESTER_PROJECT will be billed for this operation"
            gsutil -u $REQUESTER_PROJECT -m cp $BWA_FILES /data/ && touch /data/ok
        else
            gsutil -m cp $BWA_FILES /data/ && touch /data/ok
        fi
    elif [[ $BWA_FILES =~ ^http:// || $BWA_FILES =~ ^https:// ]]; then
        echo "using wget to retrieve BWA_FILES='$BWA_FILES'"
        wget --directory-prefix=/data/ $BWA_FILES && touch /data/ok
    else
        echo "unsupported scheme for BWA_FILES='$BWA_FILES'"
    fi
    
>>>>>>> 36fb8c47cfc03c0e0966ea4674a4207e22eb38a2
fi

/usr/sbin/apache2ctl -D FOREGROUND
