#!/usr/bin/env bash

# when replicating this file across services, need to change the --cluster parameter in the command

environment=$1
file_path_prod="./prod_values.yml"
file_path_beta="./beta_values.yml"
file_path_qa="./coverage_values.yml"

application_name_prod=$(grep "applicationName:" "$file_path_prod" | awk '{print $2}')
application_name_beta=$(grep "applicationName:" "$file_path_beta" | awk '{print $2}')
application_name_qa=$(grep "applicationName:" "$file_path_qa" | awk '{print $2}')


if [ "$environment" == "Prod" ];
then
  echo "Production Environment "
  echo "$application_name_prod"

  iam_role_value=$(grep "iamRole:" "$file_path_prod" | awk '{print $2}')

  if [ "$iam_role_value" = "true" ];then
    eksctl create iamserviceaccount --name "$application_name_prod" --attach-role-arn arn:aws:iam::867657578464:role/"$application_name_prod" --cluster wi-prod-employer-v2 --region us-east-1 --namespace "$application_name_prod" --approve
  fi
fi


if [ "$environment" == "Beta" ];
then
  echo "Beta Environment"
  echo "$application_name_beta"

  iam_role_value=$(grep "iamRole:" "$file_path_beta" | awk '{print $2}')

  if [ "$iam_role_value" = "true" ]; then
    eksctl create iamserviceaccount --name "$application_name_beta" --attach-role-arn arn:aws:iam::867657578464:role/"$application_name_prod" --cluster wi-prod-employer-v2 --region us-east-1 --namespace "$application_name_beta" --approve
  fi

fi

if [ "$environment" == "QA" ];
then
  echo "QA Environment"
  echo "$application_name_qa"

  iam_role_value=$(grep "iamRole:" "$file_path_qa" | awk '{print $2}')

  if [ "$iam_role_value" = "true" ]; then
    eksctl create iamserviceaccount --name "$application_name_qa" --attach-role-arn arn:aws:iam::867657578464:role/"$application_name_prod" --cluster wi-prod-employer-v2 --region us-east-1 --namespace "$application_name_qa" --approve
  fi

fi