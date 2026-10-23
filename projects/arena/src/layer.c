#include "layer.h"
#include <math.h>

DenseLayer* layer_create(Arena *arena, int input_size, int output_size) {
    // Allocate the layer struct from the arena
    DenseLayer *layer = (DenseLayer*)arena_alloc(arena, sizeof(DenseLayer));
    if (!layer) return NULL;

    layer->input_size = input_size;
    layer->output_size = output_size;

    // Allocate contiguous blocks for weights and biases in the same arena
    layer->weights = (float*)arena_alloc(arena, output_size * input_size * sizeof(float));
    layer->bias = (float*)arena_alloc(arena, output_size * sizeof(float));

    if (!layer->weights || !layer->bias) {
        return NULL;
    }

    return layer;
}

void layer_forward(const DenseLayer *layer, const float *inputs, float *outputs) {
    for (int o = 0; o < layer->output_size; o++) {
        float sum = layer->bias[o];
        const float *row_weights = &layer->weights[o * layer->input_size];
        
        // Inner loop is completely linear and cache-friendly
        for (int i = 0; i < layer->input_size; i++) {
            sum += inputs[i] * row_weights[i];
        }
        
        // Simple ReLU activation example
        outputs[o] = sum > 0.0f ? sum : 0.0f;
    }
}