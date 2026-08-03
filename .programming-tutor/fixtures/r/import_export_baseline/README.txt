R Import/Export Practice Dataset

Files:
- sample_metadata.csv: sample-level metadata.
- gene_counts.tsv: wide count matrix with genes as rows and samples as columns.
- gene_annotation.csv: gene-level annotation table.
- qc_metrics.xlsx: Excel workbook with sequencing_qc, library_notes, and read_me sheets.
- project_config.json: small config file for JSON import practice.

Important:
- The sample order in gene_counts.tsv is intentionally not the same as the row order in sample_metadata.csv.
- One metadata note is blank.
- One QC RIN value is missing.
- One library_notes adaptor_trimmed value is FALSE.
- Adult samples have a different library_prep value in the Excel file.
