#!/usr/bin/env bash

# Build on staging,
#   ./build.sh staging namespace build-number
#
# Build on production,
#   ./build.sh production build-timestamp

set -e # Script fails if docker build fails (has edge cases)

if test -z "$1"
then
  echo "Please Enter A Build Flavour"
  exit
fi

if test "$1" != "staging" && test "$1" != "production" && test "$1" != "productionK8s"
then
  echo "Please Enter Correct Build Flavour"
  exit
fi

if test "$1" = "staging"
then
    if test -z "$2"
    then
    echo "Please Enter Namespace"
    exit
    fi
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 472738512112.dkr.ecr.us-east-1.amazonaws.com
    docker build --file ./app/DockerfileStag -t wi-job-notification-ms:staging-"$2"-"$3" ./app
    docker tag wi-job-notification-ms:staging-"$2"-"$3" 472738512112.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:staging-"$2"-"$3"
    docker push 472738512112.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:staging-"$2"-"$3"
elif test "$1" = "productionK8s"
then
    # K8 deployment via new-Jenkins
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 867657578464.dkr.ecr.us-east-1.amazonaws.com
    docker build --file ./app/DockerfileProd -t wi-job-notification-ms:"$2" -t wi-job-notification-ms:latest ./app
    docker tag wi-job-notification-ms:"$2" 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:"$2"
    docker push 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:"$2"
    docker tag wi-job-notification-ms:latest 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:latest
    docker push 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:latest

  # ASG deployment via old-Jenkins
  else
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 867657578464.dkr.ecr.us-east-1.amazonaws.com
    docker build --file ./app/DockerfileProd -t wi-job-notification-ms ./app
    docker tag wi-job-notification-ms:latest 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:latest
    docker push 867657578464.dkr.ecr.us-east-1.amazonaws.com/application/wi-job-notification-ms:latest

    cp ./build/docker-compose.yml.prod.api ./build/docker-compose.yml
    sed -i -e "s|__CONSUL_TOKEN__|${3}|g" ./build/docker-compose.yml
    aws s3 cp ./build/docker-compose.yml s3://workindia-terraform/wi-job-notification-ms/prod/api/us-east-1/
    rm ./build/docker-compose.yml

    cp ./build/init.sh.template ./build/init.sh
    chmod u+x ./build/init.sh
    sed -i -e 's|__REGION_NAME__|us-east-1|g;s|__BUCKET_PATH__|s3://workindia-terraform/wi-job-notification-ms/prod/api/us-east-1/|g' ./build/init.sh
    aws s3 cp ./build/init.sh s3://workindia-terraform/wi-job-notification-ms/prod/api/us-east-1/
    rm ./build/init.sh

    aws s3 sync --delete ./build/config s3://workindia-terraform/wi-job-notification-ms/prod/api/us-east-1/config
fi
