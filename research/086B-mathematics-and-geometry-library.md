# 086B — Mathematics, geometry, and topology library

## Question
What mathematical primitives — number systems, geometric objects, topology, algebra, calculus, statistics, signal processing — must GSPL ship at v1 so that any computation, shape, transform, or analysis a creator or engine needs is available as a substrate-callable form?

## Why it matters
Every other library in this round depends on math. A campfire needs ODEs. A ring of stars needs projective geometry. A character's skin needs differentiable BRDFs. A song needs FFTs. A statistical visualization needs distributions. If math lives only inside scattered engines, the substrate cannot guarantee numerical correctness or differentiability across them. If it ships as **a single signed substrate of mathematical primitives**, every engine speaks the same numerical language and gradients flow everywhere.

## What we know from the spec
- Brief 071: differentiable substrate.
- Brief 082: physics (consumes math).
- Brief 081, 083, 084, 085: all consume math.

## Findings — what GSPL ships at v1

### 1. Number systems and exact arithmetic
- **Integers** (arbitrary precision via GMP-equivalent).
- **Rationals** (exact).
- **Reals** (IEEE 754 single, double, quad; bfloat16, float16 for ML).
- **Complex** (real and dual complex).
- **Quaternions, octonions** (for 3D rotation and physics).
- **Dual numbers** (forward-mode autodiff substrate).
- **Hyperreal** (for symbolic limits).
- **Modular and finite fields** (for crypto, Brief 077).
- **Interval arithmetic** for guaranteed bounds.
- **Symbolic** (computer algebra subset via SymPy-equivalent).

### 2. Linear algebra
- **Vectors, matrices, tensors** with full BLAS/LAPACK operations.
- **Decompositions:** LU, QR, SVD, eigen, Cholesky, Schur.
- **Sparse matrices** with CSR/CSC/COO/BSR.
- **Tensor contractions** (Einstein notation, named-axis tensors).
- **Quaternion and dual-quaternion algebra** for rigging.

### 3. Geometry — primitives and operations
- **Euclidean primitives:** point, line, ray, segment, plane, polygon, polyhedron, sphere, cylinder, cone, torus, ellipsoid, capsule, AABB, OBB, frustum.
- **Curves:** Bézier (quadratic, cubic, rational), B-spline, NURBS, Catmull-Rom, Hermite, arc, conic.
- **Surfaces:** NURBS surface, subdivision surface (Catmull-Clark, Loop, Doo-Sabin), implicit surface (signed distance functions), parametric surface, T-spline.
- **Meshes:** half-edge, winged-edge, indexed face set, with full mesh operations (boolean, decimation, subdivision, repair, parameterization).
- **Computational geometry:** convex hull (QuickHull), Voronoi/Delaunay (CGAL-equivalent), constrained Delaunay, BSP, k-d tree, octree, BVH.
- **Geometric algebra (Clifford algebra)** primitives for rotor-based 3D math.

**Source:** CGAL, Eigen, GLM, libigl, OpenMesh, OpenSubdiv, geometric algebra references.

### 4. Topology
- **Simplicial complexes** for mesh topology.
- **Genus, Euler characteristic** computation.
- **Homology and persistent homology** for shape analysis.
- **Knots and links** taxonomy (for braided structures, fabric, hair).
- **Manifold maps** for parameterization.

**Source:** GUDHI, Dionysus persistence libraries.

### 5. Calculus and analysis
- **Symbolic differentiation and integration** (via CAS subset).
- **Numerical differentiation** (forward, central, complex-step).
- **Numerical integration** (Gauss quadrature, Romberg, adaptive Simpson).
- **ODE solvers** (RK4, Dormand-Prince RK45, BDF, Rosenbrock, symplectic Verlet/leapfrog for Hamiltonian systems).
- **PDE solvers** (FDM, FEM, FVM, spectral) wrapped as substrate primitives.
- **Optimization:** gradient descent, Adam, L-BFGS, Newton, trust region, Nelder-Mead, simulated annealing, genetic algorithms, CMA-ES.
- **Root finding** (bisection, Newton, Brent).
- **Autograd** through every analytic operation (consumes Brief 071 differentiable substrate).

### 6. Statistics and probability
- **Distributions:** uniform, normal, lognormal, exponential, gamma, beta, Poisson, binomial, multinomial, Dirichlet, Wishart, Cauchy, Student-t, Pareto, Weibull, von Mises, von Mises-Fisher (for directional data).
- **Sampling:** inverse CDF, rejection, Metropolis-Hastings, HMC, NUTS, slice sampling.
- **Estimators:** MLE, MAP, Bayesian inference primitives.
- **Tests:** t, chi-square, KS, ANOVA, Mann-Whitney.
- **Information theory:** entropy, KL divergence, mutual information.
- **Random number generators** with named substrate seeds for reproducibility (consumes Brief 026 determinism contract).

### 7. Signal processing and transforms
- **FFT** (1D, 2D, 3D, real, complex).
- **Wavelets** (Daubechies, Haar, biorthogonal).
- **DCT, DST, Hartley, Hadamard.**
- **Convolution, correlation, deconvolution.**
- **Filter design** (FIR, IIR, Butterworth, Chebyshev, elliptic, Bessel, Kaiser).
- **Resampling** (polyphase, sinc, Lanczos).
- **Spectrograms, mel spectrograms** (for audio engines).
- **Hilbert transform, analytic signal.**
- **Color space transforms** (RGB ↔ XYZ ↔ Lab ↔ OKLab ↔ HSL ↔ HSV ↔ YCbCr) — referenced by visual identity (Brief 078).

### 8. Procedural and noise primitives
- **Perlin, simplex, OpenSimplex, value, Worley/cellular, curl** noise — all dimensionally generalized.
- **Fractals:** Mandelbrot, Julia, Burning Ship, Lyapunov, IFS (Iterated Function Systems), L-systems (consumes Brief 085 plant L-systems).
- **Stochastic textures:** reaction-diffusion (Turing patterns), Gabor noise, phasor noise, blue noise (Poisson disk).
- **Hashing primitives** (PCG, xxHash, MurmurHash for procedural seeding).

### 9. Constants
- **Mathematical constants:** π, e, γ (Euler-Mascheroni), φ (golden ratio), Catalan, Apéry, all to bfloat16/float32/float64/float128/MPFR-1000-digit precision.
- **Special functions:** Γ, B, ζ, Bessel J/Y/I/K, Legendre, Hermite, Chebyshev, spherical harmonics (real and complex), Wigner D, Clebsch-Gordan.

## Findings — math gseed structure

```
math://constant/pi@v1.0
math://op/fft@v1.0
math://geom/sphere@v1.0
math://noise/simplex@v1.0
math://distribution/normal@v1.0
math://solver/ode/rk45@v1.0
math://transform/colorspace/rgb-to-oklab@v1.0
```

Every math primitive is a signed, differentiable, dimensionally-checked substrate callable. Engines do not reimplement math — they consume the substrate's. The same FFT runs on T0/T1/T2/T3 with bit-identical results given the same seed (consumes Brief 026 determinism).

## Inventions

### INV-326: Math as a single signed differentiable substrate
Every math primitive — from arithmetic to spherical harmonics — is encoded as a substrate-callable form with autograd, dimensional checking, and tier-routable execution. Engines do not ship their own math libraries; they consume the substrate's. Novel because no creative tool ships math as substrate primitives with cross-engine numerical coherence.

### INV-327: Named substrate noise seeds with cross-tier reproducibility
Procedural noise primitives accept named substrate seeds and produce bit-identical output across all execution tiers. A noise field generated on a phone matches one generated in a federated render farm exactly. Novel as substrate-level deterministic procedural primitives.

## Phase 1 deliverables

- **Full number system + linear algebra + tensor stack** at v1.
- **Geometry, topology, calculus, statistics, signal processing, transforms** at v1.
- **All major noise and fractal primitives** at v1.
- **Mathematical constants + special functions** at v1.
- **Autograd through every analytic op** at v1.
- **Cross-tier reproducibility** for every primitive at v1.

## Risks

- **Library bloat.** Mitigation: modular packaging; load on demand.
- **Numerical determinism across tiers.** Mitigation: ship reference CPU implementations as ground truth (consumes INV-217).

## Recommendation

1. **Wrap Eigen, CGAL, libigl, FFTW, SciPy, SymPy** as substrate-wrapped libraries.
2. **Sign every primitive** under GSPL Foundation Identity.
3. **Build the dimensional checker** (consumes INV-313).
4. **Wire autograd** through every analytic op.

## Confidence
**5/5.** Sources are open, mature, and well-tested. Engineering is wrapping, not invention.

## Spec impact

- `inventory/mathematics.md` — new doc.
- `inventory/math-schema.md` — new doc.
- New ADR: `adr/00NN-math-as-substrate-primitive.md`.

## Open follow-ups

- Library wrapping API design.
- Reference CPU kernel certification.
- Cross-tier numerical equivalence test suite.

## Sources

- Eigen (C++ linear algebra).
- CGAL (computational geometry).
- libigl (geometry processing).
- OpenMesh, OpenSubdiv.
- FFTW.
- SciPy, NumPy, SymPy.
- GUDHI persistent homology.
- Boost.Math, GSL.
- *Numerical Recipes*.
- *Real-Time Collision Detection* (Ericson).
- *Geometric Tools* (Eberly).
- Internal: Briefs 026, 071, 077, 081, 082, 083, 084, 085.
