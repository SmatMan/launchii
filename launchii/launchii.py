"""launchii

Usage:
    $ python launchii.py --cli
    $ python launchii.py --gui
"""
import sys
import platform
import pathlib

import pinject
import appdirs

import launchii.cli
import launchii.gui
from launchii.core import PluginLaunchii


def main(cli, gui, print, args, launchii):
    if "--cli" in args:
        cli(launchii).start()
    elif "--gui" in args:
        gui(launchii).start()
    else:
        print(__doc__)


def run():
    class BoostrapProviderSpec(pinject.BindingSpec):
        def provide_app_dirs(self):
            return appdirs.AppDirs("launchii")

        def provide_user_config_dir(self, app_dirs):
            return pathlib.Path(app_dirs.user_config_dir)

        def provide_system(self):
            return platform.system()

        def provide_bootstrap_provider_spec(self):
            return self

    instantiator = pinject.new_object_graph(
        modules=[launchii.core, launchii.plugins],
        binding_specs=[BoostrapProviderSpec()],
    )

    launchiiApp = instantiator.provide(PluginLaunchii)

    main(launchii.cli.Cli, launchii.gui.Gui, print, sys.argv, launchiiApp)
