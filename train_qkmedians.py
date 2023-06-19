import argparse
import numpy as np
import h5py
import qibo

qibo.set_backend("tensorflow")

import qkmedians as qkmed


def train_qkmedians(
    train_size,
    read_file,
    device_name,
    seed=None,
    k=2,
    tolerance=1.0e-3,
    save_dir=None,
):
    """Performs training of quantum k-medians.

    Parameters
    ----------
    train_size : int
        Number of training samples.
    read_file : str
        Name of the file where training data is saved.
    device_name : str
        Name of device for running a simulation of quantum circuit.
    seed : int
        Seed for data shuffling.
    k : int
        Number of classes in quantum k-medians.
    tolerance : float
        Tolerance for algorithm convergence.
    save_dir : str
        Name of the file for saving results.
    """

    # read train data
    with h5py.File(read_file, "r") as file:
        data = file["latent_space"]
        l1 = data[:, 0, :]
        l2 = data[:, 1, :]

        data_train = np.vstack([l1[:train_size], l2[:train_size]])
        if seed:
            np.random.seed(seed)  # matters for small data sizes
        np.random.shuffle(data_train)

    # Intialize centroids
    centroids = qkmed.initialize_centroids(data_train, k)

    i = 0; new_tol = 1
    loss = []
    while True:
        # find nearest centroids
        cluster_label, _ = qkmed.find_nearest_neighbour(data_train, centroids, device_name)
        # find new centroids
        new_centroids = qkmed.find_centroids(data_train, cluster_label, clusters=k)
        # calculate loss -> distance old_centroids to new_centroids
        loss_epoch = np.linalg.norm(centroids - new_centroids)
        loss.append(loss_epoch)

        if loss_epoch < tolerance:
            centroids = new_centroids
            print(f"Converged after {i+1} iterations.")
            break
        elif (loss_epoch > tolerance and i > new_tol * 200):# if after 200*new_tol epochs, difference != 0, lower the tolerance
            tolerance *= 10
            new_tol += 1
        i += 1
        centroids = new_centroids

    if save_dir:
        np.save(
            f"{save_dir}/cluster_label.npy",
            cluster_label,
        )
        np.save(
            f"{save_dir}/centroids.npy", centroids
        )
        np.save(f"{save_dir}/loss.npy", loss)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="read arguments for qkmedians training"
    )
    parser.add_argument(
        "--train_size", dest="train_size", type=int, help="training data size"
    )
    parser.add_argument(
        "--read_file", dest="read_file", type=str, help="path to training data"
    )
    parser.add_argument(
        "--seed", dest="seed", type=int, help="seed for consistent results"
    )
    parser.add_argument(
        "--k", dest="k", type=int, default=2, help="number of classes"
    )
    parser.add_argument(
        "--tolerance", dest="tolerance", type=float, default=1.0e-3, help="convergence tolerance"
    )
    parser.add_argument(
        "--save_dir", dest="save_dir", type=str, help="directory to save results"
    )
    parser.add_argument(
        "--device_name", dest="device_name", type=str, help="name of device for running quantum circuit simulation"
    )

    args = parser.parse_args()

    if args.device_name:
        qibo.set_device(args.device_name)

    train_qkmedians(
        args.train_size,
        args.read_file,
        args.device_name,
        args.seed,
        args.k,
        args.tolerance,
        args.save_dir,
    )
