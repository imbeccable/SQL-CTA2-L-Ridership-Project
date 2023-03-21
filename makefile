###############################################################################
# For testing
###############################################################################
TEST_IN = $(wildcard tests/in/*.txt)
TEST_OUT = $(TEST_IN:tests/in/%=tests/out/%)
TEST_EXP = $(TEST_IN:tests/in/test%.txt=tests/expected/answers%.txt)

tests: $(TEST_OUT) $(TEST_EXP)

tests/expected/%: tests/in/%
	echo "HMMMMMMM"

tests/out/%: tests/in/% main.py
	mkdir -p tests/out
	python main.py < $< > $@

comp_test%: tests/out/test%.txt tests/expected/answers%.txt
	diff --color='always' tests/out/test$*.txt tests/expected/answers$*.txt