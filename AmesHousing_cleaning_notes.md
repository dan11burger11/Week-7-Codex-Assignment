# AmesHousing cleaning notes

`AmesHousing_clean.csv` is derived from `AmesHousing-1.csv` by running
`clean_ames_housing.py`.

- Trim leading and trailing whitespace from every field (including entries such
  as `WD `); keep the original column names and other values.
- Keep `NA` category values as supplied; in this dataset they commonly mean
  “not applicable,” rather than an unknown value.
- Remove exact duplicate rows and repeated property IDs if encountered, keeping
  the first row. The source file has neither.
- Require valid, nonnegative integer bathroom counts and a positive whole-dollar
  `SalePrice`. Remove a row only if a required value is missing or invalid.
- For missing basement bath counts, use zero only when the row indicates no
  basement. Both such source rows indicate no basement. Missing bath values with
  evidence of a basement would be excluded because their total cannot be
  determined reliably.
- Add `Total Bathrooms` as `Bsmt Full Bath + 0.5 × Bsmt Half Bath + Full Bath +
  0.5 × Half Bath`. The source half-bath columns count half-bath rooms, each of
  which contributes 0.5 bathroom to this amount.

All 2,930 source observations were retained. There are no missing sale prices,
no duplicate rows or property IDs, and the only missing required bath values
were the two basement counts on the no-basement records, which were set to zero.
