TF_TARGET=
TF_PLAN_FILE=$(TF_TARGET)-tf.tfplan
TF_EXEC=docker-compose run terraform
TF_EXTRA_OPS=

all: plan

clean:
	@rm -rf .terraform

get:
	$(TF_EXEC) get .
	$(TF_EXEC) fmt

init: clean get
	$(TF_EXEC) init $(TF_TARGET)

plan: init
	$(TF_EXEC) plan -out=$(TF_PLAN_FILE) $(TF_TARGET)

deploy: plan
	$(TF_EXEC) apply $(TF_PLAN_FILE) && rm $(TF_PLAN_FILE)

destroy: init
	$(TF_EXEC) destroy $(TF_EXTRA_OPS) $(TF_TARGET)
