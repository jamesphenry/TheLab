#ifndef LAYER_H
#define LAYER_H

#include "arena.h"

typedef struct {
    int input_size;
    int output_size;
    float *weights; // Flat array of size [output_size * input_size]
    float *bias;    // Flat array of size [output_size]
} DenseLayer;

DenseLayer* layer_create(Arena *arena, int input_size, int output_size);
void layer_forward(const DenseLayer *layer, const float *inputs, float *outputs);

#endif // LAYER_H