TF_VAR_TARGET=codebuild
TF_ACTION=destroy

if [[ $TF_ACTION == 'destroy' ]]; then
    make destroy-auto-approve TF_TARGET=$TF_VAR_TARGET
else
    make deploy-auto-approve TF_TARGET=$TF_VAR_TARGET
fi