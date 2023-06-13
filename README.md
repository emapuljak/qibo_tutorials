# Quantum k-medians clustering

Implementation from paper: [https://arxiv.org/abs/2301.10780](2301.10780).

## Algorithm's pseudocode

```
    Randomly initialize **k** centroids
    Until convergence:
        Find closest cluster centroid
            - For each data point use quantum subroutine for distance calculation to calculate distance to each centroid
            - Find minimal distance (either classicaly or using **Grover** search)
        Find new cluster centroids
            For each cluster find **median** using hybrid classical-quantum subroutine
```

## Distance calculation quantum circuit

![Distance circuit](DistCirc.pdf)


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