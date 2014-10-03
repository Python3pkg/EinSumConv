# About

The EinSumConv package builds on sympy and supports calculations according to Einstein summation convention. All of sympy should be compatible with EinSumConv.

In this version you can create tensors that may or may not depend on some arguments (Tensor and TensorFunction). There is a Kronecker delta (Delta) a Levi-Civita symbol (Eps). And there are some functions to simplify tensor expressions.


# Future plans

In the near future, I want EinSumConv to handle symmetric tensors (e.g. recognize that T(a,b)==T(b,a) is True iff T is symetric). And I want to adjust sympys pretty_print for the purpose of EinSumConv.

In a slightly further away future, I want to implement GR calculations with upper and lower indices. And also index notation of derivatives.

# Installation

    pip install EinSumConv
