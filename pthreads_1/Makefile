CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -Werror -ansi -pedantic
LDFLAGS ?= -lpthread
BIN = walk

all: $(BIN)

walk: walk.o atomic.o barrier.o
	$(CC) walk.o atomic.o barrier.o	$(LDFLAGS) -o $(BIN)

walk.o: main.c
	$(CC) -c main.c $(CFLAGS) -o walk.o

atomic.o: atomic.c
	$(CC) -c atomic.c $(CFLAGS) -o atomic.o

barrier.o: barrier.c
	$(CC) -c barrier.c $(CFLAGS) -o barrier.o

clean:
	rm *.o walk

.PHONY: clean
