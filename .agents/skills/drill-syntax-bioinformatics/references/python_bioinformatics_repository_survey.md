# Python in bioinformatics repositories: source survey

Survey date: 2026-08-03. This is a curriculum-oriented static survey, not a popularity ranking. I inspected 14 public repositories at pinned commits, including Python source, tests, and `pyproject.toml`/setup configuration. A feature was counted as recurring when it appeared in a repository's Python files; counts indicate breadth across repositories, not line frequency.

## Selection rationale

The sample deliberately spans reusable molecular-biology libraries (Biopython, scikit-bio), indexed genomic formats and intervals (pysam, pybedtools, gffutils, HTSeq, cyvcf2), read processing and coverage tools (Cutadapt, deepTools), single-cell data/analysis (AnnData, Scanpy), workflow and reporting applications (Snakemake, MultiQC), and microbiome/provenance infrastructure (QIIME 2). These are mature, public projects whose implementation is substantially Python, although several use Cython/C extensions for performance.

## Per-repository source evidence

| Repository (pinned source) | Why included | Source-level reading signals |
|---|---|---|
| [Biopython](https://github.com/biopython/biopython/tree/80401d49f407b8303504733906352f6bcd9f9661) | Broad molecular-biology library | [`Bio/SeqIO`](https://github.com/biopython/biopython/blob/80401d49f407b8303504733906352f6bcd9f9661/Bio/SeqIO/__init__.py) exposes iterator-based parse/read/write APIs, records, format dispatch, file handles, and exceptions; [`pyproject.toml`](https://github.com/biopython/biopython/blob/80401d49f407b8303504733906352f6bcd9f9661/pyproject.toml) shows NumPy and modern packaging/testing configuration. |
| [Scanpy](https://github.com/scverse/scanpy/tree/90c2fc50782a6ed2d27f68b725689b1e436b024d) | Major single-cell analysis toolkit | [`_highly_variable_genes.py`](https://github.com/scverse/scanpy/blob/90c2fc50782a6ed2d27f68b725689b1e436b024d/src/scanpy/preprocessing/_highly_variable_genes.py) combines typed functions, decorators, NumPy/pandas, sparse arrays, grouping, validation, and mutation of `AnnData`; [`pyproject.toml`](https://github.com/scverse/scanpy/blob/90c2fc50782a6ed2d27f68b725689b1e436b024d/pyproject.toml) names the scientific/test stack. |
| [AnnData](https://github.com/scverse/anndata/tree/8660a9d346319a561763360575ca74804c8ae2e8) | Core annotated matrix container | [`_core/anndata.py`](https://github.com/scverse/anndata/blob/8660a9d346319a561763360575ca74804c8ae2e8/src/anndata/_core/anndata.py) is class-heavy code involving properties, slicing/index normalization, mappings, copy/view semantics, sparse/dense arrays, and file-backed state; [`pyproject.toml`](https://github.com/scverse/anndata/blob/8660a9d346319a561763360575ca74804c8ae2e8/pyproject.toml) confirms NumPy, pandas, SciPy, h5py/zarr, and pytest. |
| [pysam](https://github.com/pysam-developers/pysam/tree/6a40751c8c9278a3f5be6904437d92ee619377f4) | Python interface to SAM/BAM/CRAM/VCF/BCF and htslib | [`pysam/libcalignmentfile.pyx`](https://github.com/pysam-developers/pysam/blob/6a40751c8c9278a3f5be6904437d92ee619377f4/pysam/libcalignmentfile.pyx) shows the `AlignmentFile`/record/iterator interface and Cython boundary; [`pysam/utils.py`](https://github.com/pysam-developers/pysam/blob/6a40751c8c9278a3f5be6904437d92ee619377f4/pysam/utils.py) shows Python wrappers, temporary files, arguments, dispatch, and error handling. |
| [scikit-bio](https://github.com/scikit-bio/scikit-bio/tree/1158e9f54447f472a5bd3b8e64495b22a6fc2f7c) | Sequence, diversity, alignment, and phylogenetics library | [`skbio/io/registry.py`](https://github.com/scikit-bio/scikit-bio/blob/1158e9f54447f472a5bd3b8e64495b22a6fc2f7c/skbio/io/registry.py) uses decorators, generators, registries, file handles, classes, and exceptions for format plugins; [`pyproject.toml`](https://github.com/scikit-bio/scikit-bio/blob/1158e9f54447f472a5bd3b8e64495b22a6fc2f7c/pyproject.toml) shows NumPy/SciPy/pandas and test tooling. |
| [pybedtools](https://github.com/daler/pybedtools/tree/beedab98dbd4671f7d5cc4773432bd4d5ca2737a) | Pythonic genomic intervals plus BEDTools wrapping | [`pybedtools/bedtool.py`](https://github.com/daler/pybedtools/blob/beedab98dbd4671f7d5cc4773432bd4d5ca2737a/pybedtools/bedtool.py) centers on classes, iterators, decorators, temporary files, subprocess-backed operations, and interval parsing; [`pyproject.toml`](https://github.com/daler/pybedtools/blob/beedab98dbd4671f7d5cc4773432bd4d5ca2737a/pyproject.toml) identifies pysam and pytest dependencies. |
| [deepTools](https://github.com/deeptools/deepTools/tree/ea0f68bb4a1587d713dacb3791861308751ef7d0) | Sequencing coverage/QC command-line suite | [`countReadsPerBin.py`](https://github.com/deeptools/deepTools/blob/ea0f68bb4a1587d713dacb3791861308751ef7d0/deeptools/countReadsPerBin.py) uses NumPy arrays, pysam reads, intervals, multiprocessing-oriented chunking, classes, and validation; [`pyproject.toml`](https://github.com/deeptools/deepTools/blob/ea0f68bb4a1587d713dacb3791861308751ef7d0/pyproject.toml) shows CLI entry points and scientific dependencies. |
| [MultiQC](https://github.com/MultiQC/MultiQC/tree/14f071465794fdfb4392e2038d073a35e8524ad7) | Extensible parser/reporting application | [`multiqc/base_module.py`](https://github.com/MultiQC/MultiQC/blob/14f071465794fdfb4392e2038d073a35e8524ad7/multiqc/base_module.py) demonstrates classes, typed mappings, logging, regex parsing, paths, configuration, and plotting/report data; [`pyproject.toml`](https://github.com/MultiQC/MultiQC/blob/14f071465794fdfb4392e2038d073a35e8524ad7/pyproject.toml) exposes its CLI/plugin and pytest setup. |
| [Snakemake](https://github.com/snakemake/snakemake/tree/08d1d26baa2e1f863e6a0b997fd823db9607bab6) | Python workflow engine used throughout bioinformatics | [`src/snakemake/workflow.py`](https://github.com/snakemake/snakemake/blob/08d1d26baa2e1f863e6a0b997fd823db9607bab6/src/snakemake/workflow.py) uses classes, dataclasses, enums, context managers, async/executor integration, paths, subprocesses, configuration, and exceptions; [`pyproject.toml`](https://github.com/snakemake/snakemake/blob/08d1d26baa2e1f863e6a0b997fd823db9607bab6/pyproject.toml) defines dependencies and entry points. |
| [QIIME 2](https://github.com/qiime2/qiime2/tree/4e70785c7831cc6ec0c2ac5f0fc6f461479b43af) | Microbiome artifact/provenance infrastructure | [`archive_parser.py`](https://github.com/qiime2/qiime2/blob/4e70785c7831cc6ec0c2ac5f0fc6f461479b43af/src/rachis/core/archive/provenance_lib/archive_parser.py) uses abstract classes, dataclasses, paths, mappings, pandas, archive I/O, and validation; [`pyproject.toml`](https://github.com/qiime2/qiime2/blob/4e70785c7831cc6ec0c2ac5f0fc6f461479b43af/pyproject.toml) records package/test configuration. |
| [gffutils](https://github.com/daler/gffutils/tree/6b84330f472dd2b4c69e36f319da7ade95bd5961) | GFF/GTF parsing and SQLite feature database | [`gffutils/interface.py`](https://github.com/daler/gffutils/blob/6b84330f472dd2b4c69e36f319da7ade95bd5961/gffutils/interface.py) shows classes, SQL queries, generators, region filtering, feature objects, and exceptions; [`pyproject.toml`](https://github.com/daler/gffutils/blob/6b84330f472dd2b4c69e36f319da7ade95bd5961/pyproject.toml) shows packaging and pytest configuration. |
| [HTSeq](https://github.com/htseq/htseq/tree/76723210af19d37160baa60020c7f1a16c73bc19) | Read counting and genomic feature operations | [`HTSeq/features.py`](https://github.com/htseq/htseq/blob/76723210af19d37160baa60020c7f1a16c73bc19/HTSeq/features.py) contains iterators over GFF/SAM-oriented objects, attribute parsing, interval logic, and file handling; [`pyproject.toml`](https://github.com/htseq/htseq/blob/76723210af19d37160baa60020c7f1a16c73bc19/pyproject.toml) shows NumPy/pysam/pandas and pytest. |
| [Cutadapt](https://github.com/marcelm/cutadapt/tree/50e9fb8d35b606196ae88d63252fc35674c0eda1) | High-throughput sequencing read trimming | [`src/cutadapt/pipeline.py`](https://github.com/marcelm/cutadapt/blob/50e9fb8d35b606196ae88d63252fc35674c0eda1/src/cutadapt/pipeline.py) uses dataclasses, typed protocols, composition, generators, multiprocessing, statistics accumulation, and exceptions; [`pyproject.toml`](https://github.com/marcelm/cutadapt/blob/50e9fb8d35b606196ae88d63252fc35674c0eda1/pyproject.toml) shows CLI/build/test configuration. |
| [cyvcf2](https://github.com/brentp/cyvcf2/tree/b8f22b53d3c97fac1f44041220af6cc3c9690f95) | Fast VCF/BCF reader and writer | [`cyvcf2/cyvcf2.pyx`](https://github.com/brentp/cyvcf2/blob/b8f22b53d3c97fac1f44041220af6cc3c9690f95/cyvcf2/cyvcf2.pyx) exposes iterable `VCF`, `Variant`, NumPy genotype arrays, indexing, and Cython/htslib boundaries; [`cyvcf2/cli.py`](https://github.com/brentp/cyvcf2/blob/b8f22b53d3c97fac1f44041220af6cc3c9690f95/cyvcf2/cli.py) adds Click CLI patterns and stream processing. |

## Cross-repository recurrence

The strongest result is not a particular algorithm: it is a style of data plumbing. Readers need to follow records lazily from files, transform/filter them, store annotations in mappings or arrays, validate assumptions, and connect Python to scientific libraries or external tools.

Static presence across the 14 repositories:

| Evidence observed in Python source | Repositories | Curriculum implication |
|---|---:|---|
| `collections`/mapping-oriented code | 14/14 | Make dictionaries, sets, counters/default dictionaries, membership, and nested record structures central. |
| `subprocess` or process/tool orchestration | 13/14 | Teach argument lists, return codes, captured streams, failures, environment, and why shell strings are hazardous. |
| `pathlib` | 12/14 | Prefer practical path joining, suffix/name inspection, iteration, opening files, and temporary paths. |
| `itertools` | 12/14 | Emphasize iterator pipelines, `chain`, grouping, pairing, and avoiding unnecessary materialization. |
| pytest imported directly | 11/14 | Reading tests is a primary code-comprehension skill: fixtures, parametrization, assertions, and expected exceptions. Other repositories also contain tests using `unittest` or project helpers. |
| NumPy | 10/14 | Arrays, shape/dtype/axis, masks, broadcasting, reductions, indexing, and dense-versus-sparse expectations deserve high weight. |
| type annotations / `typing` | 10/14 | Teach annotations as documentation: unions/optionals, collections, callables, protocols/generics at a reading level. |
| `argparse` | 10/14 | CLI parsing, flags, defaults, subcommands, namespaces, and entry-point flow recur in user-facing tools. |
| `logging` | 10/14 | Readers must distinguish log flow from returned data and understand levels and module loggers. |
| JSON | 9/14 | Configuration/metadata serialization and nested dictionary traversal are common. |
| dataclasses | 7/14 | Useful middle-tier topic: generated initialization, defaults/factories, frozen records, and post-init behavior. |
| pandas | 6/14 | DataFrame/Series selection, index alignment, grouping, missing data, categorical columns, and mutation matter, especially in single-cell/reporting code. |
| pysam API used directly | 5/14 | High bioinformatics relevance despite narrower breadth: alignment/variant files, records, regions, pileups/fetch, flags, headers, and coordinate conventions. |
| Matplotlib | 5/14 | Reading figure construction, axes, labels, and arrays-to-plots is useful but secondary to data flow. |
| SciPy | 4/14 | Focus on sparse matrices and common statistical/distance calls, not encyclopedic API recall. |

Also repeated but not captured well by import counts: functions with keyword/default arguments; classes and inheritance; list/dict/set comprehensions; slicing and boolean indexing; generators and `yield`; context managers (`with`); `try`/`except`/`raise`; decorators and registries; regex/string parsing; filesystem compression and text/binary modes; warnings; and validation via explicit exceptions. These occur throughout the linked implementation files.

### Bioinformatics-specific interfaces worth recognizing

- Sequence records and format dispatch: Biopython `Seq`, `SeqRecord`, `SeqIO.parse/read/write`, features, annotations, FASTA/FASTQ/GenBank.
- Alignment and variant records: pysam `AlignmentFile`, `AlignedSegment`, `VariantFile`, `VariantRecord`; cyvcf2 `VCF`/`Variant`; flags, CIGAR, qualities, samples/genotypes, headers, region fetches.
- Genomic intervals/features: BED/GFF/GTF coordinates, strand, overlaps, iterators, feature attributes; pybedtools `BedTool`/`Interval`, gffutils feature databases, HTSeq intervals/read counting.
- Annotated matrices: `AnnData.X`, `.obs`, `.var`, `.obsm`, `.layers`, views/copies, sparse versus dense matrices; Scanpy preprocessing/tool functions and `inplace` behavior.
- Workflow/report/plugin code: CLI entry points, configuration, logging, subprocess/executor boundaries, module/plugin discovery, provenance, and structured report data.

### Framework-specific or lower-priority details

Cython declarations and direct htslib bindings (pysam/cyvcf2), QIIME's archive/provenance class hierarchy, Snakemake's internal DSL/executor machinery, Scanpy's plotting conventions, and MultiQC's plugin/report internals are valuable when reading those projects but should not dominate a general Python bank. Likewise, advanced metaclasses/descriptors, asynchronous internals, intricate decorator implementation, packaging backend details, and obscure one-line truthiness puzzles did not recur broadly enough to justify much drill time.

## Recommended topic list and relative emphasis

The percentages are suggested shares of a future Python quickfire bank; they sum to 100%. Questions should mostly ask the learner to trace or complete realistic code fragments rather than recall trivia.

| Topic | Share | What to test |
|---|---:|---|
| Iteration, generators, comprehensions, and record pipelines | 14% | `for`, `enumerate`, `zip`, generator expressions, `yield`, lazy versus materialized data, filtering/aggregation. |
| Dictionaries, sets, records, and nested metadata | 11% | Lookup/update, membership, safe defaults, counters/grouping, nested annotations, ordering assumptions. |
| Functions and API-call reading | 10% | Positional/keyword/default arguments, unpacking, return values, scope, small callbacks, `*args`/`**kwargs` at reading level. |
| Files, paths, streams, compression, and formats | 10% | `with`, `Path`, text/binary modes, handles versus paths, line/record parsing, temporary files. |
| NumPy arrays and sparse-matrix awareness | 10% | shape/dtype/axis, slicing, masks, broadcasting, reductions, copies/views; recognize SciPy sparse constraints. |
| Classes and scientific data objects | 8% | attributes/methods, constructors, properties, inheritance/composition, dataclasses, copying and mutation. |
| Exceptions, validation, warnings, and logging | 8% | `try`/`except`/`finally`, raising informative errors, expected failures, warnings, log levels. |
| Bioinformatics records, coordinates, and domain APIs | 8% | SeqIO/records, BAM/VCF/GFF/BED objects, iterating/fetching, headers/annotations, 0- versus 1-based and half-open intervals. |
| pandas and annotated tables | 6% | Series/DataFrame selection, index alignment, `groupby`, missingness, categorical data, `.obs`/`.var`. |
| Command lines, subprocesses, configuration, and entry points | 5% | `argparse`/Click concepts, argument lists, exit status, JSON/YAML-like mappings, `if __name__ == "__main__"`. |
| Tests and codebase navigation | 5% | pytest assertions, fixtures, parametrization, mocks/temporary paths, reading a test to infer a contract. |
| Strings, regex, parsing, and serialization | 3% | split/join/strip, f-strings, regex groups, JSON conversion, bytes versus text. |
| Essential Python semantics retained despite lower direct salience | 2% | truthiness in normal control flow, `None`, equality versus identity, mutability/aliasing, boolean short-circuiting, slicing boundaries. Avoid puzzle cases such as `all([])` unless tied to a realistic validation bug. |

Deprioritize stand-alone drills on recursion, clever chained comparisons, obscure operator precedence, custom descriptors/metaclasses, advanced async, and implementing algorithms from scratch. Retain them only where they explain real control flow or a recurring library interface. Conversely, coordinate systems, lazy iteration, mutation/copy semantics, sparse data, and exception-driven validation deserve more attention than raw import frequency alone suggests because misunderstanding them causes scientifically consequential reading errors.

## Limits

This is a purposive sample, and static presence does not measure how often a learner will encounter a construct within each project. The pinned snapshots also include tests and developer utilities, intentionally, because understanding a codebase includes reading its contracts and command-line/build boundaries. Results support relative curriculum emphasis; they are not claims about all Python bioinformatics software.
