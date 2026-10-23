# 1. What is an artificial neuron?

![The Essential Guide to Neural Network Architectures](https://images.openai.com/static-rsc-4/m5bmlnmwYlNW5SqO1EvkssPH17OQWqJE0KeLCKlZtOfR-X5HDVd7UDcK1JLn0AtnmFGXDqUNmwWuy4o7-f1FVX2foHRf_n22G1oTjX9OfqLLHT9C6lYu62_3iE9hT0OD2FkZk9xTie0JqFgh-Rn-FhCYQ8ez24xMVf-TTxIsETk?purpose=inline)

[v7labs.com](https://www.v7labs.com/blog/neural-network-architectures-guide?utm_source=chatgpt.com)

An artificial neuron is a small mathematical function. It takes inputs, combines them using adjustable numbers called weights, adds a bias, and passes the result through an activation function.

The basic process is:

Inputs

\(x_1, x_2, x_3\)

Weighted sum

\(z = x_1w_1 + x_2w_2 + x_3w_3 + b\)

Activation function

\(y = f(z)\)

Output

\(y\)

Let's unpack that without assuming any neural-network knowledge.

## 2. Inputs: ordinary numbers

Imagine we want a neuron to receive two inputs:

- \(x_1 = 1.0\)
    
- \(x_2 = 0.5\)
    

These are just floating-point numbers. They could represent anything: board positions in your game AI, measurements, or outputs from other neurons.

In C17, what type would naturally represent these values?

```
double x1 = 1.0;
double x2 = 0.5;
```

We could use `float` too. The important point for now is that a neuron doesn't inherently understand what an input means. It just receives numbers.

## 3. Weights: how strongly inputs contribute

Each input has a corresponding weight:

\[ z = x_1w_1 + x_2w_2 + b \]

Suppose:

|Variable|Value|
|---|---|
|`x1`|1.0|
|`w1`|0.8|
|`x2`|0.5|
|`w2`|-0.4|
|`b`|0.1|

The weighted sum is:

\[ z = (1.0 \times 0.8) + (0.5 \times -0.4) + 0.1 \]

\[ z = 0.8 - 0.2 + 0.1 = 0.7 \]

The weights determine how each input affects the result.

- A positive weight makes a positive input contribute positively.
    
- A negative weight makes a positive input contribute negatively.
    
- A weight of zero means that input contributes nothing to this sum.
    

These weights are parameters the learning algorithm can adjust. The input values are the data; the weights are part of what the neuron learns.

## 4. Bias: an adjustable offset

The bias is the `b` in our equation.

Without it, the weighted sum would be:

\[ z = x_1w_1 + x_2w_2 \]

Adding a bias lets the neuron shift its result independently of the input contributions. Even if every input is zero, the weighted sum can still be nonzero.

In C, bias is just another number:

```
double bias = 0.1;
```

Nothing magical about it. Its importance comes from the mathematics, not from a special C feature.

## 5. Activation: what happens after the sum?

So far, we can calculate `z`. But neurons often apply an activation function to it.

For a first experiment, consider the ReLU activation:

\[ f(z) = \max(0,z) \]

It returns zero for negative inputs and leaves positive inputs unchanged.

|`z`|ReLU output|
|---|---|
|-2.0|0.0|
|0.0|0.0|
|0.7|0.7|
|3.0|3.0|

A possible C implementation, once you're ready to write it, is conceptually just a comparison and a return value. You don't need to understand any neural-network framework to implement it.

Other activation functions behave differently. For example, sigmoid squashes values into the range \(0\) to \(1\). We'll compare them later and examine why the choice matters.

# 6. Your first C experiment

Let's pause before writing the neuron itself.

You already know how to declare variables and perform arithmetic in C. The first experiment is to calculate the weighted sum manually using the values above.

## Your first task: 
try those experiments, then tell me what you observed. From there, we'll write the smallest possible C17 program that calculates a neuron's weighted sum. We'll keep it as ordinary C code until we understand every part, then build toward a reusable neuron structure.