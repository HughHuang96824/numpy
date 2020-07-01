from numpy.core._multiarray_umath import __cpu_features__, __cpu_baseline__, __cpu_dispatch__
from numpy.core import _umath_tests
from numpy.core import _multiarray_umath
from numpy.testing import assert_equal

def dispatch_assert(test, highest_sfx, all_sfx):
    assert_equal(test["func"], "func" + highest_sfx)
    assert_equal(test["var"], "var"  + highest_sfx)

    if highest_sfx:
        assert_equal(test["func_xb"], "func" + highest_sfx)
        assert_equal(test["var_xb"], "var"  + highest_sfx)
    else:
        assert_equal(test["func_xb"], "nobase")
        assert_equal(test["var_xb"], "nobase")

    all_sfx.append("func") # add the baseline
    assert_equal(test["all"], all_sfx)
    all_sfx.pop()

def test_dispatcher():
    """
    Testing the utilites of the CPU dispatcher
    """
    targets = (
        "SSE2", "SSE41", "AVX2",
        "VSX", "VSX2", "VSX3",
        "NEON", "ASIMD", "ASIMDHP"
    )
    highest_sfx = "" # no suffix for the baseline
    all_sfx = []
    for feature in reversed(targets):
        # skip baseline features, by the default `CCompilerOpt` do not generate separated objects
        # for the baseline,  just one object combined all of them via 'baseline' option
        # within the configuration statments.
        if feature in __cpu_baseline__:
            continue
        # check compiler and running machine support
        if feature not in __cpu_dispatch__ or not __cpu_features__[feature]:
            continue

        if not highest_sfx:
            highest_sfx = "_" + feature
        all_sfx.append("func" + "_" + feature)

    dispatch_assert(_umath_tests.test_dispatch(), highest_sfx, all_sfx)
    dispatch_assert(_multiarray_umath.test_dispatch(), highest_sfx, all_sfx)
