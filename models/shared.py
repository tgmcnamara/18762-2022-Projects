
from lib.MatrixBuilder import MatrixBuilder


def stamp_line(Y: MatrixBuilder, Vr_from, Vr_to, Vi_from, Vi_to, G, B):
    #From Bus - Real
    Y.stamp(Vr_from, Vr_from, G)
    Y.stamp(Vr_from, Vr_to, -G)
    Y.stamp(Vr_from, Vi_from, B)
    Y.stamp(Vr_from, Vi_to, -B)

    #From Bus - Imaginary
    Y.stamp(Vi_from, Vi_from, G)
    Y.stamp(Vi_from, Vi_to, -G)
    Y.stamp(Vi_from, Vr_from, -B)
    Y.stamp(Vi_from, Vr_to, B)

    #To Bus - Real
    Y.stamp(Vr_to, Vr_from, -G)
    Y.stamp(Vr_to, Vr_to, G)
    Y.stamp(Vr_to, Vi_from, -B)
    Y.stamp(Vr_to, Vi_to, B)

    #To Bus - Imaginary
    Y.stamp(Vi_to, Vi_from, -G)
    Y.stamp(Vi_to, Vi_to, G)
    Y.stamp(Vi_to, Vr_from, B)
    Y.stamp(Vi_to, Vr_to, -B)