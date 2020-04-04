
.PHONY: dev test live clean

dev:
	python3 yonder_dev.py
	mv yonder_dev.json yonder.json

test:
	python3 yonder_test.py
	mv yonder_test.json yonder.json

live:
	python3 yonder_live.py
	mv yonder_live.json yonder.json

clean:
	rm ./*.json
