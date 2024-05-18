include .env

all: prep package_model synth deploy

prep:
	bash -e scripts/setup.sh

update_notice:
	bash -e scripts/update_notice.sh

package_model:
	source .venv/bin/activate && cd ./model_endpoint/runtime/serving_api && tar czvf ../../docker/serving_api.tar.gz custom_lambda_utils requirements.txt serving_api.py

cdk_bootstrap:
	source .venv/bin/activate && cdk bootstrap aws://$(CDK_DEFAULT_ACCOUNT)/$(DEPLOYMENT_REGION) 

synth:
	source .venv/bin/activate && cdk synth

deploy:
	source .venv/bin/activate && cdk deploy

destroy:
	source .venv/bin/activate && cdk destroy

clean: 
	rm -r .venv/ cdk.out/
