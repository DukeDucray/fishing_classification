.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################

reinstall_package:
	@pip uninstall -y fishing_classification || :
	@pip install -e .

reset_local_files:
	rm -rf mlops
	mkdir -p mlops/data/
	mkdir mlops/data/raw
	mkdir mlops/data/processed
	mkdir mlops/training_outputs
	mkdir mlops/training_outputs/metrics
	mkdir mlops/training_outputs/models
	mkdir mlops/training_outputs/params
