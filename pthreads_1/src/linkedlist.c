#include <assert.h>
#include "../include/linkedlist.h"

void list_insert(struct list_node *node, struct list_node *new)
{
    assert(new);
    assert(node);
    assert(node->next);
    assert(node->next->prev);

    new->prev = node;
    new->next = node->next;
    node->next->prev = new;
    node->next = new;
}

void list_remove(struct list_node *node)
{
    assert(node);
    assert(node->next);
    assert(node->prev);
    assert(node->prev->next);
    assert(node->next->prev);
    node->prev->next = node->next;
    node->next->prev = node->prev;
}
