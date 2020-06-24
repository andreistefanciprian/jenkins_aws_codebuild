TF_VAR_TARGET=static
TF_ACTION=destroy

if [[ $TF_ACTION == 'destroy' ]]; then
    make destroy TF_EXTRA_OPS=-auto-approve TF_TARGET=$TF_VAR_TARGET
else
    make deploy TF_TARGET=$TF_VAR_TARGET
fi