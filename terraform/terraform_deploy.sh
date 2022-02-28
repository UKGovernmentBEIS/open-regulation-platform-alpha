PROJECT_ROOT=`pwd`/..
WORKSPACE="staging"
FORCE_DEPLOY=""
VERSION="1.0.0"
ARTIFACT_BUCKET="orp-build-outputs"
ARG_ERRORS=0

show_help() {
    echo "ORP Terraform deployment script, deploys an ORP system using Terraform and"
    echo "previously generated build artifacts. You must export AWS_PROFILE before running this"
    echo "script."
    echo ""
    echo "USAGE:"
    echo "    ./terraform_deploy.sh [-w WORKSPACE] [-v VERSION] [-s SQITCH_VERSION] [-a ARTIFACT_BUCKET] [-f]"
    echo ""
    echo "OPTIONAL ARGUMENTS:"
    echo "    -w WORKSPACE"
    echo "        The name of the Terraform workspace to deploy (default = staging)"
    echo "    -v VERSION"
    echo "        The version for this deployment (default = 1.0.0"
    echo "    -a ARTIFACT_BUCKET"
    echo "        The S3 bucket where build artifacts are stored (default = orp-build-outputs)"
    echo "    -f"
    echo "        Force deployment of the Terraform plan without prompting for confirmation"
    exit 1
}

while getopts "h?w::v::a::f" opt; do
    case "$opt" in
    h|\?)
        show_help
        ;;
    w)
        WORKSPACE=$OPTARG
        ;;
    v)
        VERSION=$OPTARG
        ;;
    a)
        ARTIFACT_BUCKET=$OPTARG
        ;;
    f)
        FORCE_DEPLOY="-auto-approve"
        ;;
    esac
done

if [ "$WORKSPACE" = "" ]; then
    echo "ERROR: You must define a value for WORKSPACE"
    ARG_ERRORS=1
fi

if [ "$AWS_PROFILE" = "" ]; then
    echo "ERROR: You must export AWS_PROFILE before running this script"
    ARG_ERRORS=1
fi

if [ "$ARG_ERRORS" = "1" ]; then
    show_help
fi

if [ ! -z "$(git status --porcelain)" ]; then
    echo "ERROR: Working directory is not clean, commit all changes before running this script"
    exit 1
fi

echo "============================================================================================="
echo "Initialising Terraform Workspace"
echo "============================================================================================="
terraform init -backend-config="bucket=$ARTIFACT_BUCKET"

terraform workspace select $WORKSPACE > /dev/null 2>&1
if [ "$?" = "1" ]; then
    terraform workspace new $WORKSPACE
fi

set -euo pipefail

echo "============================================================================================="
echo "Applying Terraform configuration"
echo "============================================================================================="
terraform apply -var-file=$WORKSPACE.tfvars -var base_name=orp-$WORKSPACE -var version_tag=$VERSION $FORCE_DEPLOY -var artifact_bucket=$ARTIFACT_BUCKET

# echo "============================================================================================="
# echo "Reapplying Terraform configuration to remove deployment access"
# echo "============================================================================================="
# terraform apply -var-file=$WORKSPACE.tfvars -var base_name=orp-$WORKSPACE -var version_tag=$VERSION $FORCE_DEPLOY -var artifact_bucket=$ARTIFACT_BUCKET -var lockdown_access=true
