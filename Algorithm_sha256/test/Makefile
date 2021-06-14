CC=gcc
clflag= -g -c

lib_objects=../sha256/constants.o \
			../sha256/hash.o \
			../sha256/sha256.o \
			../sha256/types.o 

test_objects= test_sha256.o
tests= test_sha256

all: clean $(tests)
	echo "############# All Tests Passed ##############"

%.o:%.c
	$(CC) $(clflag) -o $@ $<

test_sha256: $(test_objects) $(lib_objects)
	$(CC) $(cflag) $(lib_objects) test_sha256.o -o test_sha256
	./test_sha256
	rm test_sha256

clean:
	-rm $(lib_objects)
	-rm $(test_objects)
