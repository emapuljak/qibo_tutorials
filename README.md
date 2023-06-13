# Quantum k-medians clustering

Implementation of QKmedians from the paper: [https://arxiv.org/abs/2301.10780](2301.10780).

## Algorithm's pseudocode

![pseudo](figures/pseudocode_QKmed.jpeg)

## Distance calculation quantum circuit

![Distance circuit](figures/DistCirc.png)

## How to run an example?

To run a particular instance of the problem we have to set up the initial
arguments:
- `nqubits` (int): number of quantum bits.
- `layers` (int): number of ansatz layers.
- `compress` (int): number of compressed/discarded qubits.
- `lambdas` (list or array): different λ on the Ising model to consider for the training.

As an example, in order to compress 2 qubits on an initial quantum state with 6 qubits, and using 3 layers,
you should execute the following command:

```python
python main.py --nqubits 6 --layers 3 --compress 2 --lambdas [0.9, 0.95, 1.0, 1.05, 1.10]
```