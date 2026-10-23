#define DEV 1
#include <stdio.h>
#include "neuron.h"

int main(void) {
    Neuron *neuron = create_neuron(3, relu);
    if (!neuron) return 1;

    // Encapsulated state modification
    neuron_set_bias(neuron, 0.1f);
    neuron_set_weight(neuron, 0, 0.5f);

    float current_bias = 0.0f;
    if (neuron_get_bias(neuron, &current_bias)) {
        printf("Current bias: %f\n", current_bias);
    }

    free_neuron(neuron);
    return 0;
}