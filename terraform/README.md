# AWS Instance Deployment

To set-up an EC2 instance on AWS, with the relevant security groups, load balancer, target groups, etc, you need to run the following commands from the terraform/ directory:

1) Create a `tfvars` file (you can use the staging.tfvars.template file as an example)
    - The domain used in this tfvars file must already be set up on AWS
    - The artifact bucket used in this tfvars file must already be set up on AWS
2) `export AWS_PROFILE=orp-admin-role`
3) Ensure you have both the relevant `id_rsa.pub` and `id_rsa` files in the top level of the ORP directory. These cannot be pulled from Git
4) run `./terraform_deploy.sh -w NAME_OF_WORKSPACE -a ARTIFACT_BUCKET`
    - The workspace argument is the name of the infrastructure stack
    - If you run this without passing through a -w argument, the default workspace is staging
    - The artifact bucket will store the terraform outputs, this needs to be created before running terraform_deploy

To destroy the terraform stack, simply run:

`terraform destroy -var-file=TFVARS-FILE-NAME.tfvars -var base_name=NAME_OF_WORKSPACE -var version_tag=VERSION_NUMBER`

terraform_deploy.sh will run a terraform script that will look something like this:
`terraform apply -var-file=staging.tfvars -var base_name=orp-staging -var version_tag=1.0.0 -var artifact_bucket=orp-staging-build-outputs`

This will then kick off main.tf:
- Establishes orp-build-outputs as the S3 bucket to hold state
- Creates EC2 networking module
- Creates EC2 instance
- Creates Application Load Balancer module

Once the above has completed:
1) Docker will be installed
2) The repo will be pulled from git
3) The deployment script will run to create the docker stack

To access the instance:

`ssh -i "orp-staging.pem" admin@PUBLIC_IPV4_DNS`
The Public IPv4 DNS will be output at the end of the deployment

To start the Streamlit demo:

1) SSH into the EC2 instance - `ssh -i "orp-staging.pem" admin@PUBLIC_IPV4_DNS`
2) `cd orp_alpha/api_demo/`
3) `./demo_installs.sh -a ADDRESS`, for example `./demo_installs.sh -a 18.135.121.158` (Run in a tmux session if you wish to leave the demo up and navigate around the instance)
4) To view the streamlit demo, go to the public IP address and add the relevant port, for example `18.135.121.158:8051`