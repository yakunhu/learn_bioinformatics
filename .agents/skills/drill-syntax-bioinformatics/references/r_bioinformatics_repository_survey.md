# R bioinformatics repository survey

Surveyed 2026-08-03 to calibrate the interview-focused R quickfire bank. The survey samples representative source files rather than treating GitHub stars as a scientific-quality ranking. Questions should teach patterns recurring across repositories, not repository-specific trivia.

| Repository | Area | Representative source | Recurring code-reading constructs |
|---|---|---|---|
| `satijalab/seurat` | Single-cell analysis | `R/utilities.R` | nested `[[`/`$` access, matrix subsetting, `lapply`/`vapply`, `Matrix::` operations, validation, namespaces |
| `bioc/DESeq2` | Bulk RNA-seq differential expression | `R/AllClasses.R` | S4 classes, `assay()`/`counts()`/`colData()`, missingness and numeric validation, factors, formulas, design matrices |
| `Bioconductor/GenomicRanges` | Genomic intervals | `R/findOverlaps-methods.R` | S4 method dispatch, range subsetting, `match.arg()`, validation, internal namespaces |
| `YuLab-SMU/clusterProfiler` | Functional enrichment | `R/simplify.R` | S4 methods, data-frame filtering, `is.na()`, `lapply`/`vapply`, namespace-qualified calls |
| `cole-trapnell-lab/monocle3` | Single-cell trajectories | `R/order_cells.R` | nested object access, Bioconductor accessors, pipes, `apply`/`vapply`, assertions, graph and matrix dimensions |
| `bioc/edgeR` | Bulk RNA-seq differential expression | `R/glmfit.R` | S3 methods, matrices, `drop = FALSE`, factors, `model.matrix()`, dimension checks, errors |
| `Bioconductor/SummarizedExperiment` | Bioconductor containers | `R/Assays-class.R` | S4 classes and methods, matrix-like interfaces, list iteration, dimension invariants, replacement methods |
| `tidyomics/tidybulk` | Tidy transcriptomics | `R/pivot.R` | generics, `SummarizedExperiment` accessors, native pipes, tidy transformations, row and column metadata |
| `MarioniLab/scran` | Single-cell normalization and modeling | `R/fixedPCA.R` | `assay()` access, matrix transposition and subsetting, `drop = FALSE`, argument matching |
| `saeyslab/nichenetr` | Ligand-target modeling | `R/supporting_functions.R` | tidy pipelines, nested subsetting, apply-family calls, sparse matrices, factors, design matrices, optional namespaces |
| `jinworks/CellChat` | Cell-cell communication | `R/CellChat_class.R` | S4 objects and slots, Seurat/SCE interoperability, sparse matrices, lists, factors, validation and warnings |
| `LTLA/scuttle` | Single-cell preprocessing | `R/logNormCounts.R` | S4 generics and methods, `SummarizedExperiment`/`SingleCellExperiment` accessors, subsetting, argument matching |

## Curriculum implications

- Highest priority: one- and two-dimensional subsetting, dimensions and names, list extraction, vectorized predicates, missingness, functions, and validation.
- Bioinformatics-specific priority: sparse matrices, factors and design formulas, S3/S4 dispatch, accessors for assay and metadata containers, namespaces, and package layout.
- Important workflow literacy: pipes, grouped transformations, joins, reshaping, plotting layers, tests, and debugging entry points.
- Deprioritized: arithmetic curiosities such as `0 / 0` or `Inf - Inf`, isolated `is.nan()` distinctions, `Map()`/`Reduce()` trivia, and other constructs not supported by the surveyed code-reading burden.
