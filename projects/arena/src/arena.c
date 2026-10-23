#include "arena.h"
#include <stdlib.h>

Arena* arena_create(size_t capacity) {
    Arena *a = (Arena*)malloc(sizeof(Arena));
    if (!a) return NULL;
    a->buffer = (char*)malloc(capacity);
    if (!a->buffer) {
        free(a);
        return NULL;
    }
    a->capacity = capacity;
    a->offset = 0;
    return a;
}

void* arena_alloc(Arena *a, size_t size) {
    // Align to 8-byte boundary for safe float/pointer access
    size_t aligned_size = (size + 7) & ~7;
    if (a->offset + aligned_size > a->capacity) {
        return NULL; // Out of arena memory
    }
    void *ptr = &a->buffer[a->offset];
    a->offset += aligned_size;
    return ptr;
}

void arena_free(Arena *a) {
    if (a) {
        free(a->buffer);
        free(a);
    }
}