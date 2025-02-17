import pytest
from optimization import OptimizationBounds
from trend_labelling import (
    BaseLabeller,
    BinaryCTL,
    TernaryCTL,
    OracleBinaryTrendLabeller,
    OracleTernaryTrendLabeller,
)


@pytest.fixture
def optimisation_bounds():
    """Fixture providing an OptimisationBounds instance."""
    return OptimizationBounds()


class TestOptimizationBounds:
    """Tests for the OptimizationBounds class."""

    def test_binary_ctl_bounds(self):
        """Test bounds for BinaryCTL."""
        bounds = OptimizationBounds().get_bounds(BinaryCTL)
        assert "omega" in bounds
        assert bounds["omega"] == (0.0, 1.0)

    def test_ternary_ctl_bounds(self):
        """Test bounds for TernaryCTL."""
        bounds = OptimizationBounds().get_bounds(TernaryCTL)
        assert "marginal_change_thres" in bounds
        assert "window_size" in bounds
        assert bounds["marginal_change_thres"] == (0.000001, 0.1)
        assert bounds["window_size"] == (1, 5000)

    def test_oracle_binary_bounds(self):
        """Test bounds for OracleBinaryTrendLabeller."""
        bounds = OptimizationBounds().get_bounds(OracleBinaryTrendLabeller)
        assert "transaction_cost" in bounds
        assert bounds["transaction_cost"] == (0.0, 1.0)

    def test_oracle_ternary_bounds(self):
        """Test bounds for OracleTernaryTrendLabeller."""
        bounds = OptimizationBounds().get_bounds(OracleTernaryTrendLabeller)
        assert "transaction_cost" in bounds
        assert "trend_coeff" in bounds
        assert bounds["transaction_cost"] == (0.0, 1.0)
        assert bounds["trend_coeff"] == (0.0, 1.0)

    def test_unsupported_labeller(self):
        """Test error handling for unsupported labeller class."""

        class UnsupportedLabeller(BaseLabeller):
            def get_labels(self, time_series: list[float]) -> list[int]:
                return []

        with pytest.raises(ValueError, match="No default bounds for labeller class"):
            OptimizationBounds().get_bounds(UnsupportedLabeller)

    @pytest.mark.parametrize(
        "labeller_class,expected_params",
        [
            (BinaryCTL, ["omega"]),
            (TernaryCTL, ["marginal_change_thres", "window_size"]),
            (OracleBinaryTrendLabeller, ["transaction_cost"]),
            (OracleTernaryTrendLabeller, ["transaction_cost", "trend_coeff"]),
        ],
        ids=[
            "binary_ctl",
            "ternary_ctl",
            "oracle_binary",
            "oracle_ternary",
        ],
    )
    def test_bounds_parameters(
        self, optimisation_bounds, labeller_class, expected_params
    ):
        """Test that each labeller class returns the expected parameter bounds."""
        bounds = optimisation_bounds.get_bounds(labeller_class)
        assert set(bounds.keys()) == set(expected_params)
        for param in expected_params:
            assert isinstance(bounds[param], tuple)
            assert len(bounds[param]) == 2
            assert bounds[param][0] <= bounds[param][1]
