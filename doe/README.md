# Design of Experiments (DoE)

To run the surrogate model, it was imperative that the training was done effectively across the operational envelope. A **Latin Hypercube Sampling** space-filling design was used to generate the input parameters.

## Configuration Constraints
* **Total Samples:** 250 unique configurations.
* **Precision:** Hard-constrained to a **maximum of 2 decimal places** to align with simulation constraints.
* **Sampling Window:**
	* Inlet velocity: `[1.0, 3.0]`
	* Battery temperature: `[30.0, 35.0]`
	* Cooler temperature: `[5.0, 15.0]`

