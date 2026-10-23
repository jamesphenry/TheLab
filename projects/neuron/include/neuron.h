#ifndef NEURON_H
#define NEURON_H

#include <stddef.h>
#include <stdbool.h>

typedef float (*ActivationFunc)(float);

// Conditional transparency: full struct exposed if DEV is defined, 
// otherwise opaque (incomplete type) in release mode.
#ifdef DEV
struct Neuron {
    int input_count;
    float *weights;
    float bias;
    ActivationFunc activate;
};
typedef struct Neuron Neuron;
#else
typedef struct Neuron Neuron;
#endif

// Standard activation functions
float relu(float x);
float sigmoid(float x);
float linear(float x);

// Lifecycle and utility functions
Neuron* create_neuron(int input_count, ActivationFunc act);
void randomize_neuron_weights(Neuron *n, float min_val, float max_val);
float neuron_forward(const Neuron *n, const float *inputs);
void free_neuron(Neuron *n);

// Status-code based getters and setters (Pattern 1)
bool neuron_set_weight(Neuron *n, int index, float val);
bool neuron_get_weight(const Neuron *n, int index, float *out_weight);
bool neuron_set_bias(Neuron *n, float val);
bool neuron_get_bias(const Neuron *n, float *out_bias);

#endif // NEURON_H