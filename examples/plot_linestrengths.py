import numpy as np
from matplotlib import pyplot as plt
from numpy import exp

from radis.db.classes import get_molecule, get_molecule_identifier
from radis.io.hitemp import fetch_hitemp
from radis.levels.partfunc import PartFuncHAPI
from radis.phys.constants import hc_k


def get_Qgas(molecule, iso, T):

    M = get_molecule_identifier(molecule)

    Q = PartFuncHAPI(M, iso)
    return Q.at(T=T)


def calc_linestrength_eq(df, Tref, Tgas):

    print("Scaling equilibrium linestrength")

    # %% Load partition function values

    def _calc_Q(molecule, iso, T_ref, T_gas):

        Qref = get_Qgas(molecule, iso, T_ref)
        Qgas = get_Qgas(molecule, iso, T_gas)

        return Qref, Qgas

    id_set = df.id.unique()
    id = list(id_set)[0]
    molecule = get_molecule(id)  # retrieve the molecule
    iso_set = set(df.iso)  # df1.iso.unique()

    iso_arr = list(range(max(iso_set) + 1))

    Qref_arr = np.empty_like(iso_arr, dtype=np.float64)
    Qgas_arr = np.empty_like(iso_arr, dtype=np.float64)
    for iso in iso_arr:
        if iso in iso_set:
            Qref, Qgas = _calc_Q(molecule, iso, Tref, Tgas)
            Qref_arr[iso] = Qref
            Qgas_arr[iso] = Qgas

    df["Qref"] = Qref_arr.take(df.iso)
    df["Qgas"] = Qgas_arr.take(df.iso)

    # Scaling linestrength with the equations from Rotham's paper
    line_strength = df.int * (df.Qref / df.Qgas)
    line_strength *= exp(-hc_k * df.El * (1 / Tgas - 1 / Tref))
    line_strength *= (1 - exp(-hc_k * df.wav / Tgas)) / (1 - exp(-hc_k * df.wav / Tref))
    # Add a fresh columns with the scaled linestrength
    df["S"] = line_strength  # [cm-1/(molecules/cm-2)]

    # Just to make sure linestrength is indeed added
    assert "S" in df

    return df


if __name__ == "__main__":
    Tref = 296
    df = fetch_hitemp(
        molecule="CH4",
        databank_name="HITEMP-CH4",
        isotope="1, 2, 3",
        load_wavenum_min=2000,
        load_wavenum_max=2020,
    )

    Tgas = 300

    df = calc_linestrength_eq(df, Tref, Tgas)
    plt.bar(df["wav"], df["S"])
    plt.xlabel("Wavenumbers in cm-1")
    plt.ylabel("Linestrengths in cm-1/(molecules/cm-2)")
    plt.show()
