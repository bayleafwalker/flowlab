.PHONY: verify sample clean

verify:
	./scripts/verify.sh

sample:
	./scripts/run-sample.sh

clean:
	rm -rf reports/sample .test-output
