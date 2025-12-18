.PHONY: clean

# Pattern rule to match dayXX targets (e.g. make day02)
day%: day%.ts
	tsc $<
	node $@.js
	rm $@.js

clean:
	rm -f *.js
