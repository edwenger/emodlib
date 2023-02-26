from test_host import params_from_test_file

from emodlib.malaria import Infection, IntrahostComponent, Susceptibility


def test_infection():
    params = params_from_test_file()
    IntrahostComponent.configure(params)  # required for Infection::Initialize params?

    s = Susceptibility.create()

    infs = [Infection.create(susceptibility=s, hepatocytes=1) for _ in range(10)]

    msp_types = [i.msp_type for i in infs]
    print(msp_types)
    assert all([t < params["Falciparum_MSP_Variants"] for t in msp_types])

    major_types = infs[0].pfemp1_major_types
    print(major_types)
    assert len(major_types) == 50
    assert all([t < params["Falciparum_PfEMP1_Variants"] for t in major_types])


if __name__ == "__main__":
    test_infection()
