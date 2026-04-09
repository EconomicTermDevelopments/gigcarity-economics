---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- gigcarity
- computational-economics
- labor-economics
- emerging-terminology
pretty_name: Gigcarity Economics Dataset
size_categories:
- n<1K
---

# Gigcarity Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `Gigcarity` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Labor Economics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique worker-period id
- `week`: Synthetic weekly labor observation
- `income_volatility`: Short-horizon earnings volatility
- `benefit_gap`: Gap in access to employment-linked benefits
- `schedule_instability`: Unpredictability in work scheduling
- `algorithmic_control`: Degree of platform algorithmic management control
- `earnings_uncertainty`: Uncertainty around expected earnings
- `collective_voice_deficit`: Lack of collective bargaining/voice mechanisms
- `safety_net_access`: Access to social insurance and safety nets
- `gigcarity_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating Gigcarity applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{gigcarity2026,
title={{Gigcarity Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
