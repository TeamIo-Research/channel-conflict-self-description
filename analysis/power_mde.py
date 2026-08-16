# -*- coding: utf-8 -*-
"""
power_mde.py -- a-priori minimum detectable effect for the confirmatory family.

Produces the figures quoted in Methods 3.8. Written 2026-08-13, BEFORE any
confirmatory data. Takes no data as input: this is a design-stage power
calculation, a function of n, alpha and the assumed control-cell baseline only.

Why this file exists: the report states that every reported number is produced
by a script in this repository and copied from its output. The 2026-08-13 cold
review pointed out that the power figures were, at that moment, the one
exception -- computed inline and hand-carried. This closes that gap.

Design: the pre-registered multiple-comparison family is three tests, cell A vs
cell C flip-rate difference at k = 4, 6, 9, each pooled across 2 attributes and
3 model families. So n = 15 x 2 x 3 = 90 conversations per cell per test,
BEFORE valid-single-choice loss shrinks it. Holm thresholds are .0167 / .025 /
.05 in p-value order; the strictest (.0167) is reported as the binding case.

Method: two-proportion normal approximation, two-sided,
    n per group = (z_{1-a/2} + z_{power})^2 * [p1(1-p1) + p2(1-p2)] / (p2-p1)^2
solved for the smallest (p2 - p1) that the given n supports. Reported to the
nearest percentage point; a normal approximation is adequate at this precision
and errs conservatively at small p.

Usage:  python power_mde.py            (prints the table quoted in Methods 3.8)
Writes nothing. ASCII output only.
"""
import math

ALPHA_UNCORRECTED = 0.05
ALPHA_HOLM_STRICTEST = 0.0167     # first of three tests under Holm at alpha=.05
POWER = 0.80
N_PER_CELL_POOLED = 15 * 2 * 3    # n=15 x 2 attributes x 3 families
N_SINGLE_CELL = 15                # one attribute, one family
BASELINES = (0.05, 0.10, 0.20, 0.30, 0.50)


def z(p):
    """Inverse standard normal CDF (Acklam's rational approximation)."""
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    pl = 0.02425
    if p < pl:
        q = math.sqrt(-2 * math.log(p))
        return ((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
                ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))
    if p <= 1 - pl:
        q = p - 0.5
        r = q * q
        return ((((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q /
                (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1))
    q = math.sqrt(-2 * math.log(1 - p))
    return -((((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) /
             ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1))


def mde(n_per_group, alpha, power, p_control, step=0.0001):
    """Smallest detectable absolute difference in proportions, or None."""
    za, zb = z(1 - alpha / 2.0), z(power)
    d = step
    while p_control + d < 1.0:
        p2 = p_control + d
        required = ((za + zb) ** 2 *
                    (p_control * (1 - p_control) + p2 * (1 - p2)) / (d * d))
        if required <= n_per_group:
            return d
        d += step
    return None


def fmt(m):
    return "%.0f pp" % (m * 100) if m is not None else "not detectable"


def main():
    print("A-PRIORI MINIMUM DETECTABLE EFFECT  (two-proportion, two-sided, power %.2f)" % POWER)
    print("No data is used. Design-stage calculation only.\n")
    print("Confirmatory family: cell A vs cell C flip-rate difference, per k.")
    print("Pooled across 2 attributes x 3 families -> n = %d per cell per test.\n"
          % N_PER_CELL_POOLED)
    print("%-16s %-18s %-22s" % ("control baseline",
                                 "alpha=%.3f" % ALPHA_UNCORRECTED,
                                 "alpha=%.4f (Holm, strictest)" % ALPHA_HOLM_STRICTEST))
    for p in BASELINES:
        print("%-16s %-18s %-22s" % (
            "%.0f%%" % (p * 100),
            fmt(mde(N_PER_CELL_POOLED, ALPHA_UNCORRECTED, POWER, p)),
            fmt(mde(N_PER_CELL_POOLED, ALPHA_HOLM_STRICTEST, POWER, p))))

    print("\nSingle cell (one attribute, one family), n = %d, alpha=%.2f:"
          % (N_SINGLE_CELL, ALPHA_UNCORRECTED))
    for p in (0.10, 0.20, 0.30):
        print("   baseline %2.0f%% -> %s"
              % (p * 100, fmt(mde(N_SINGLE_CELL, ALPHA_UNCORRECTED, POWER, p))))

    print("\nNOTE: these are ceilings on sensitivity, not floors on importance.")
    print("A difference smaller than the figures above is not thereby unimportant;")
    print("the MDE describes prospective power, not a post-result threshold.")


if __name__ == "__main__":
    main()
