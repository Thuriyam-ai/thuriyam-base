# Run tests based on the environment
#
# For local,
#   ./runtest.sh local
# For staging,
#   ./runtest.sh stag
# For production,
#   ./runtest.sh prod

if test "$1" = "local"
then
    newman run job-notification.postman_collection.json -e local.postman_environment.json --reporters cli,junit --reporter-junit-export "newman/report.xml"

elif test "$1" = "stag"
then
    newman run job-notification.postman_collection.json -e stag.postman_environment.json --reporters cli,junit --reporter-junit-export "newman/report.xml"

elif test "$1" = "prod"
then
    newman run job-notification.postman_collection.json -e prod.postman_environment.json --reporters cli,junit --reporter-junit-export "newman/report.xml"

fi