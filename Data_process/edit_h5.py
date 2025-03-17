import h5py

datapath1 = r"D:\ExpData\SPE\20250224_SPE_hBN_afterSEMprocess\measurement-2\20250224_SPE_hBN_afterSEM_measurement-2 - 副本.h5"
with h5py.File(datapath1, "a") as f:
    spectra = f["OceanOpticsSpectrometer"]
    del spectra["hBN_afterSEM_5kV_5min_expose10s_200uW_back_2_1"]
    del spectra[""]
    del spectra[""]
    del spectra[""]
    del spectra[""]
    del spectra[""]
    del spectra[""]




    for key in spectra.keys():
        print(key)
    # data = f["OceanOpticsSpectrometer"]
    # for key in data.keys():
    #     print(key)