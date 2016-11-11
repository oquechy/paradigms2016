#include <assert.h>
#include <string.h>
#include "../include/queue.h"

void queue_init(struct queue *queue)
{
	queue->head.prev = &queue->head;
	queue->head.next = &queue->head;
	queue->size = 0;
}

unsigned long queue_size(struct queue *queue)
{
	return queue->size;
}

void queue_push(struct queue *queue, struct list_node *node)
{
	list_insert(&queue->head, node);
	queue->size += 1;
}

struct list_node *queue_pop(struct queue *queue)
{
    struct list_node *node;
    assert(queue->head.prev);
	node = queue->head.prev;

	if (!queue_size(queue))
		return NULL;
	list_remove(node);
	queue->size -= 1;
	return node;
}
