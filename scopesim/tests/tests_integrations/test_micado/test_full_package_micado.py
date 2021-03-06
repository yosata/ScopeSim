# integration test using everything and the MICADO package
import pytest
from pytest import approx
import os
import shutil

import numpy as np
from astropy import units as u
from astropy.io import fits

import scopesim
from scopesim import rc

from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm


# if rc.__config__["!SIM.tests.run_integration_tests"] is False:
#     pytestmark = pytest.mark.skip("Ignoring MICADO integration tests")

rc.__config__["!SIM.file.local_packages_path"] = "./micado_temp/"


PKGS = {"Armazones": "locations/Armazones.zip",
        "ELT": "telescopes/ELT.zip",
        "MAORY": "instruments/MAORY.zip",
        "MICADO": "instruments/MICADO.zip"}

CLEAN_UP = True
PLOTS = False


def setup_module():
    rc_local_path = rc.__config__["!SIM.file.local_packages_path"]
    if not os.path.exists(rc_local_path):
        os.mkdir(rc_local_path)
        rc.__config__["!SIM.file.local_packages_path"] = os.path.abspath(
            rc_local_path)

    for pkg_name in PKGS:
        if not os.path.isdir(os.path.join(rc_local_path, pkg_name)) and \
                "irdb" not in rc_local_path:
            scopesim.download_package(PKGS[pkg_name])


def teardown_module():
    rc_local_path = rc.__config__["!SIM.file.local_packages_path"]
    if CLEAN_UP and "irdb" not in rc_local_path:
        shutil.rmtree(rc.__config__["!SIM.file.local_packages_path"])


class TestInit:
    def test_all_packages_are_available(self):
        rc_local_path = rc.__config__["!SIM.file.local_packages_path"]
        for pkg_name in PKGS:
            assert os.path.isdir(os.path.join(rc_local_path, pkg_name))
        print("irdb" not in rc_local_path)


class TestLoadUserCommands:
    def test_user_commands_loads_without_throwing_errors(self, capsys):
        cmd = scopesim.UserCommands(use_instrument="MICADO")
        assert isinstance(cmd, scopesim.UserCommands)
        for key in ["SIM", "OBS", "ATMO", "TEL", "INST", "DET"]:
            assert key in cmd and len(cmd[key]) > 0

        stdout = capsys.readouterr()
        assert len(stdout.out) == 0

    def test_user_commands_loads_mode_files(self):
        cmd = scopesim.UserCommands(use_instrument="MICADO")
        yaml_names = [yd["name"] for yd in cmd.yaml_dicts]
        print(yaml_names)

        assert "MICADO_IMG_LR" in yaml_names

    def test_user_commands_can_change_modes(self):
        cmd = scopesim.UserCommands(use_instrument="MICADO")
        cmd.set_modes(["MCAO", "SPEC_3000x50"])
        assert "MAORY" in [yd["name"] for yd in cmd.yaml_dicts]
        assert "MICADO_SPEC" in [yd["name"] for yd in cmd.yaml_dicts]

    def test_user_commands_can_change_modes_via_init(self):
        cmd = scopesim.UserCommands(use_instrument="MICADO",
                                    set_modes=["MCAO", "SPEC_3000x50"])
        assert "MAORY" in [yd["name"] for yd in cmd.yaml_dicts]
        assert "MICADO_SPEC" in [yd["name"] for yd in cmd.yaml_dicts]


class TestMakeOpticalTrain:
    def test_works_seamlessly_for_micado_wide_mode(self):
        cmd = scopesim.UserCommands(use_instrument="MICADO",
                                    properties={"!OBS.filter_name": "Ks"})
        opt = scopesim.OpticalTrain(cmd)
        assert isinstance(opt, scopesim.OpticalTrain)

        # src = scopesim.source.source_templates.star_field(10000, 10, 25, 20)
        src = scopesim.source.source_templates.empty_sky()
        opt.observe(src)
        hdu_list = opt.readout()[0]

        assert isinstance(hdu_list, fits.HDUList)

        # opt.image_planes[0].hdu.writeto("temp_small_LR_flux_TEST.fits",
        #                                 overwrite=True)
        # hdu_list.writeto("temp_small_LR_TEST.fits", overwrite=True)

    def test_works_seamlessly_for_micado_zoom_mode(self):
        cmd = scopesim.UserCommands(use_instrument="MICADO",
                                    set_modes=["SCAO", "IMG_1.5mas"],
                                    properties={"!OBS.filter_name": "Ks"})
        opt = scopesim.OpticalTrain(cmd)
        assert isinstance(opt, scopesim.OpticalTrain)

        # src = scopesim.source.source_templates.star_field(10000, 10, 25, 20)
        src = scopesim.source.source_templates.empty_sky()
        opt.observe(src)
        hdu_list = opt.readout()[0]

        assert isinstance(hdu_list, fits.HDUList)

        # opt.image_planes[0].hdu.writeto("small_HR_flux_TEST.fits",
        #                                 overwrite=True)
        # hdu_list.writeto("small_HR_TEST.fits", overwrite=True)

    def test_works_for_full_frame(self):
        pass









class TestSkyBackgroundIsRealistic:
    @pytest.mark.parametrize("mode_names, filt_name, etc_flux_values, mag_diff",
                             [(["SCAO", "IMG_4mas"], "Ks", 147, 2.05),  # ph/s/pix
                              (["SCAO", "IMG_1.5mas"], "Ks", 147, 2.05),
                              (["SCAO", "IMG_4mas"], "H", 108, 0.25),
                              (["SCAO", "IMG_1.5mas"], "H", 108, 0.25),
                              (["SCAO", "IMG_4mas"], "J", 27, 0.75),
                              (["SCAO", "IMG_1.5mas"], "J", 27, 0.75)])
    def test_background_is_within_2x_of_eso_etc(self, mode_names, filt_name,
                                                etc_flux_values, mag_diff):
        """
        Comparison of the scopesim MICADO package against the ESO ETC

        Notes
        -----
        - mag_diff the discrepancy between the ETC and the skycalc BG mags
        - The ETC uses 1100m2 area and 5mas pixel size
        - ETC sky BG mags can be found on the ETC website, skycalc BG mags can
          be given when getting a spectrum on the skycalc website
        """

        cmd = scopesim.UserCommands(use_instrument="MICADO",
                                    set_modes=mode_names,
                                    properties={"!OBS.filter_name": filt_name})
        opt = scopesim.OpticalTrain(cmd)
        src = scopesim.source.source_templates.empty_sky()
        opt.observe(src)
        av_sim_bg = np.average(opt.image_planes[0].hdu.data)

        sim_pix_scale = cmd["!INST.pixel_scale"]
        sim_area = cmd["!TEL.area"].value
        etc_pix_scale = 0.005
        etc_area = 1100
        scale_factor = sim_pix_scale**2 / etc_pix_scale**2 * sim_area / etc_area
        scale_factor *= 2.512**-mag_diff

        scaled_etc_bg = etc_flux_values * scale_factor
        assert 0.5 < scaled_etc_bg / av_sim_bg < 2

        print(filt_name, scaled_etc_bg, av_sim_bg)



