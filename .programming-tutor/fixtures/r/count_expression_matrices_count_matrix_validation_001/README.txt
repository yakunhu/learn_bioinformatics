Assignment: count_expression_matrices / count_matrix_validation

The TSV represents a raw mouse-cortex RNA-seq count table received before
differential-expression analysis. It intentionally contains several kinds of
validation failures.

Import it with:

counts_df <- read.delim(
  ".programming-tutor/fixtures/r/count_expression_matrices_count_matrix_validation_001/mouse_cortex_counts_unvalidated.tsv",
  check.names = FALSE,
  stringsAsFactors = FALSE,
  na.strings = c("NA", "")
)

Keeping check.names = FALSE is important because sample-column names are part
of the data contract being audited.
