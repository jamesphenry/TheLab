#include <stdio.h>
#include "arena.h"
#include "layer.h"

int main(void) {
    // 1. Create an arena with 1 MB of pre-allocated memory
    Arena *arena = arena_create(1024 * 1024);
    if (!arena) {
        fprintf(stderr, "Arena creation failed\n");
        return 1;
    }

    // 2. Build layers inside the arena (e.g., Input: 4, Output: 2)
    DenseLayer *layer1 = layer_create(arena, 4, 2);
    if (!layer1) {
        fprintf(stderr, "Layer allocation failed\n");
        arena_free(arena);
        return 1;
    }

    // Set sample weights & biases directly (data-oriented flat access)
    layer1->bias[0] = 0.1f;
    layer1->bias[1] = -0.2f;
    for (int i = 0; i < 8; i++) {
        layer1->weights[i] = 0.5f; // Quick fill for testing
    }

    // 3. Run forward pass
    float inputs[4] = {1.0f, 0.5f, -1.0f, 2.0f};
    float outputs[2];

    layer_forward(layer1, inputs, outputs);

    printf("Layer Outputs -> [0]: %f, [1]: %f\n", outputs[0], outputs[1]);

    // 4. Wipe the entire network memory instantly (no individual free calls)
    arena_free(arena);
    return 0;
}