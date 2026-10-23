#include "neuron.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifndef DEV
struct Neuron {
    int input_count;
    float *weights;
    float bias;
    ActivationFunc activate;
};
#endif

float relu(float x) {
    return x > 0.0f ? x : 0.0f;
}

float sigmoid(float x) {
    return 1.0f / (1.0f + expf(-x));
}

float linear(float x) {
    return x;
}

Neuron* create_neuron(int input_count, ActivationFunc act) {
    if (input_count < 0) {
        return NULL;
    }

    Neuron *n = (Neuron*)malloc(sizeof(Neuron));
    if (!n) return NULL;

    n->input_count = input_count;
    n->bias = 0.0f;
    n->activate = act ? act : linear;

    if (input_count > 0) {
        n->weights = (float*)calloc(input_count, sizeof(float));
        if (!n->weights) {
            free(n);
            return NULL;
        }
    } else {
        n->weights = NULL;
    }

    return n;
}

void randomize_neuron_weights(Neuron *n, float min_val, float max_val) {
    if (!n || !n->weights) return;
    for (int i = 0; i < n->input_count; i++) {
        float scale = (float)rand() / (float)RAND_MAX;
        n->weights[i] = min_val + scale * (max_val - min_val);
    }
}

// Setter returning success status
bool neuron_set_weight(Neuron *n, int index, float val) {
    if (!n || !n->weights || index < 0 || index >= n->input_count) {
        return false;
    }
    n->weights[index] = val;
    return true;
}

// Getter using out-parameter + status code return (Pattern 1)
bool neuron_get_weight(const Neuron *n, int index, float *out_weight) {
    if (!n || !n->weights || index < 0 || index >= n->input_count || !out_weight) {
        return false; // Failure (out of bounds or invalid args)
    }
    *out_weight = n->weights[index];
    return true; // Success
}

float neuron_forward(const Neuron *n, const float *inputs) {
    if (!n || (n->input_count > 0 && (!inputs || !n->weights))) {
        return NAN;
    }

    float sum = n->bias;
    for (int i = 0; i < n->input_count; i++) {
        sum += inputs[i] * n->weights[i];
    }
    
    return n->activate(sum);
}

bool neuron_set_bias(Neuron *n, float val) {
    if (!n) {
        return false;
    }
    // Optional: add validation here if needed (e.g., isnan(val))
    n->bias = val;
    return true;
}

bool neuron_get_bias(const Neuron *n, float *out_bias) {
    if (!n || !out_bias) {
        return false;
    }
    *out_bias = n->bias;
    return true;
}

void free_neuron(Neuron *n) {
    if (n) {
        free(n->weights);
        free(n);
    }
}