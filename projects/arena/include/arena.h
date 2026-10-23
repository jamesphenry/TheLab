#ifndef ARENA_H
#define ARENA_H

#include <stddef.h>

typedef struct {
    char *buffer;
    size_t capacity;
    size_t offset;
} Arena;

Arena* arena_create(size_t capacity);
void* arena_alloc(Arena *a, size_t size);
void arena_free(Arena *a);

#endif // ARENA_H