#!/usr/bin/env python
import numpy as np

# def convolution(a, m, tipoop, tipoborda):
#     (height, width) = m.shape
#     halfh = int(height / 2)
#     halfw = int(width / 2)
#     ll, cc = np.indexes((height, width))
#     ll = np.ravel(ll) - halfh
#     cc = np.ravel(cc) - halfw
#     ll = -ll
#     cc = -cc
#     mravel = np.ravel(m)
#     if tipoop == 1:
#         mravel = m[-1::1]
#
#     a = borda(a, m , tipoborda)
#     conv = np.zeros(a.shape)
#     for elem, l, c in zip(mravel, ll, cc):
#         caux = translate(a, l, c)
#         conv += caux * elem
#     conv = conv[halfh:-halfh, halfw:-halfw]
#     return conv

# def correlation(img, mask, border)
#     pass
