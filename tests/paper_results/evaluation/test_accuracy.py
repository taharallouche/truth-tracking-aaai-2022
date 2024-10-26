from pathlib import Path

import numpy as np
import pandas as pd
import pytest


@pytest.mark.e2e
def test_compare_methods() -> None:
	# Given
	import random

	from hakeem.paper_results.evaluation.accuracy import compare_methods
	from hakeem.paper_results.inventory import COLUMNS, DATASETS

	random.seed(42)
	dataset = DATASETS["animals"]
	max_voters = 5
	n_batch = 5
	ground_truth = pd.read_csv(
		Path(dataset.path).parent / "ground_truth.csv", index_col=[COLUMNS.question]
	)
	annotations = pd.read_csv(
		Path(dataset.path).parent / "annotations.csv",
		index_col=[COLUMNS.question, COLUMNS.voter],
	)
	expected_output = {
		"Standard Approval Aggregator": np.array(
			[
				[0.5375, 0.35884218, 0.71615782],
				[0.6625, 0.52152533, 0.80347467],
				[0.8, 0.68489467, 0.91510533],
				[0.6375, 0.42215764, 0.85284236],
			]
		),
		"Euclidean Mallow Aggregator": np.array(
			[
				[0.5375, 0.35884218, 0.71615782],
				[0.6625, 0.52152533, 0.80347467],
				[0.8, 0.65072573, 0.94927427],
				[0.65, 0.41978933, 0.88021067],
			]
		),
		"Jaccard Mallow Aggregator": np.array(
			[
				[0.5375, 0.35884218, 0.71615782],
				[0.6625, 0.52152533, 0.80347467],
				[0.8, 0.65072573, 0.94927427],
				[0.65, 0.41978933, 0.88021067],
			]
		),
		"Dice Mallow Aggregator": np.array(
			[
				[0.5375, 0.35884218, 0.71615782],
				[0.6625, 0.52152533, 0.80347467],
				[0.8, 0.65072573, 0.94927427],
				[0.65, 0.41978933, 0.88021067],
			]
		),
		"Condorcet Aggregator": np.array(
			[
				[0.525, 0.33810482, 0.71189518],
				[0.5875, 0.42657692, 0.74842308],
				[0.7625, 0.54027596, 0.98472404],
				[0.575, 0.32115069, 0.82884931],
			]
		),
	}

	# When
	result = compare_methods(annotations, ground_truth, max_voters, n_batch)

	# Then
	for key, value in result.items():
		np.testing.assert_allclose(value, expected_output[key], rtol=1e-6)
