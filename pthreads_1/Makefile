CFLAGS = -Wall -Wextra -Werror -ansi -pedantic -fsanitize=thread -g
LDFLAGS = -lpthread
CC = gcc

TARGET=pqsort

_OBJ = linkedlist.o queue.o squeue.o wsqueue.o thread_pool.o $(TARGET).o
OBJ = $(patsubst %,bin/%,$(_OBJ))

_DEPS = linkedlist.h queue.h squeue.h wsqueue.h thread_pool.h
DEPS = $(patsubst %,include/%,$(_DEPS))

$(TARGET): bin $(OBJ)
	$(CC) $(OBJ) $(CFLAGS) $(LDFLAGS) -o $@

bin:
	mkdir -p $@

bin/%.o: src/%.c $(DEPS)
	$(CC) -c $(CFLAGS) $< -o $@

.PHONY: clean

clean:
	rm -rf bin $(TARGET)
