#include <assert.h>
#include <string.h>
#include "../include/queue.h"

void queue_init(struct queue *queue)
{
	queue->head.prev = &queue->head;
	queue->head.next = &queue->head;
	atomicint_init(&queue->size, 0);
}

unsigned long queue_size(struct queue *queue)
{
	return (unsigned long)atomicint_get(&queue->size);
}

void queue_push(struct queue *queue, struct list_node *node)
{
	list_insert(&queue->head, node);
	atomicint_add(&queue->size, 1);
}

struct list_node *queue_pop(struct queue *queue)
{
    struct list_node *node;
    assert(queue->head.prev);
	node = queue->head.prev;

	if (!queue_size(queue))
		return NULL;
	list_remove(node);
	atomicint_add(&queue->size, -1);
	return node;
}
