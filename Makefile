dev:
	docker compose -f docker/docker-compose.yml up -d

gui:
	FLASK_ENV=development FLASK_APP=week1 flask run --port 3000

ltr-end-to-end:
	./ltr-end-to-end.sh -y \
		-m 0 \
		-c quantiles \
		-s /Users/dwinston/Dropbox/repos/dwinston/search_with_machine_learning_course \
		-o /Users/dwinston/ltr_output \
		-a /Users/dwinston/datasets/search_with_ml/train.csv


run-test-queries-and-analysis:
	python week1/utilities/build_ltr.py \
		--xgb_test /Users/dwinston/ltr_output/test.csv \
		--train_file /Users/dwinston/ltr_output/train.csv \
		--output_dir /Users/dwinston/ltr_output \
		--xgb_test_num_queries 200 \
		--xgb_main_query_weight 0 \
		--xgb_rescore_query_weight 1 \
		&& python week1/utilities/build_ltr.py \
		--analyze \
		--output_dir /Users/dwinston/ltr_output