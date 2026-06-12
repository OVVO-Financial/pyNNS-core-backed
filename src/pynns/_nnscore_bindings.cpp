#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/vector.h>

#include <cstddef>
#include <stdexcept>
#include <string>
#include <vector>

#include "nns/nns.hpp"

namespace nb = nanobind;

namespace {

using Vector = nb::ndarray<const double, nb::ndim<1>, nb::c_contig>;

std::size_t checked_size(const Vector& x, const char* name) {
  const std::size_t n = x.shape(0);
  if (n == 0U) {
    throw std::invalid_argument(std::string(name) + " must be non-empty.");
  }
  return n;
}

double lpm_sequence(double degree, double target, const std::vector<double>& x) {
  if (x.empty()) {
    throw std::invalid_argument("x must be non-empty.");
  }
  return nns::lpm(degree, target, x.data(), x.size());
}

double upm_sequence(double degree, double target, const std::vector<double>& x) {
  if (x.empty()) {
    throw std::invalid_argument("x must be non-empty.");
  }
  return nns::upm(degree, target, x.data(), x.size());
}

std::vector<double> lpm_vector(double degree, const Vector& targets, const Vector& x) {
  const std::size_t n = checked_size(x, "x");
  const std::size_t n_targets = targets.shape(0);
  std::vector<double> out(n_targets, 0.0);
  if (n_targets == 0U) {
    return out;
  }
  nns::lpm_v(degree, targets.data(), n_targets, x.data(), n, out.data());
  return out;
}

std::vector<double> upm_vector(double degree, const Vector& targets, const Vector& x) {
  const std::size_t n = checked_size(x, "x");
  const std::size_t n_targets = targets.shape(0);
  std::vector<double> out(n_targets, 0.0);
  if (n_targets == 0U) {
    return out;
  }
  nns::upm_v(degree, targets.data(), n_targets, x.data(), n, out.data());
  return out;
}

nb::dict fast_lm_dict(const Vector& x, const Vector& y) {
  const std::size_t n = checked_size(x, "x");
  if (y.shape(0) != n) {
    throw std::invalid_argument("x and y must have the same length.");
  }
  const nns::FastLmResult result = nns::fast_lm(x.data(), y.data(), n);
  nb::dict out;
  out["coef"] = result.coef;
  out["fitted_values"] = result.fitted_values;
  out["residuals"] = result.residuals;
  out["df_residual"] = result.df_residual;
  return out;
}

nb::dict stochastic_superiority_dict(const Vector& x, const Vector& y) {
  const nns::StochSupResult result = nns::stochastic_superiority(
      x.data(), checked_size(x, "x"), y.data(), checked_size(y, "y"));
  nb::dict out;
  out["p_gt"] = result.p_gt;
  out["p_tie"] = result.p_tie;
  out["p_star"] = result.p_star;
  return out;
}

}  // namespace

NB_MODULE(_nnscore, m) {
  m.doc() = "Private nanobind bindings for the vendored NNS-core C++ backend.";

  m.def("lpm", [](double degree, double target, const Vector& x) {
    return nns::lpm(degree, target, x.data(), checked_size(x, "x"));
  });
  m.def("lpm", &lpm_sequence);
  m.def("lpm", &lpm_vector);

  m.def("upm", [](double degree, double target, const Vector& x) {
    return nns::upm(degree, target, x.data(), checked_size(x, "x"));
  });
  m.def("upm", &upm_sequence);
  m.def("upm", &upm_vector);

  m.def("gravity", [](const Vector& x, bool discrete) {
    return nns::gravity(x.data(), checked_size(x, "x"), discrete);
  });

  m.def("mode", [](const Vector& x, bool discrete, bool multi) {
    return nns::mode(x.data(), checked_size(x, "x"), discrete, multi);
  });

  m.def("fast_lm", &fast_lm_dict);
  m.def("stochastic_superiority", &stochastic_superiority_dict);
}
