.PHONY: all, clean

CCFLAGS = -Wall -Wextra -Wvla -Werror -g -lm -std=c99

all: libhashmap.a libhashmap_tests.a
clean:
	rm *.o *.a

libhashmap.a: hashmap.o
	ar rcs libhashmap.a hashmap.o

libhashmap_tests.a: test_suite.o hashmap.o test_pairs.h
	ar rcs libhashmap_tests.a test_suite.o hashmap.o

hashmap.o: hashmap.c vector.o pair.o hashmap.h hash_funcs.h
	gcc $(CCFLAGS) -c $<

vector.o: vector.c vector.h
	gcc $(CCFLAGS) -c $<

pair.o: pair.c pair.h
	gcc $(CCFLAGS) -c $<