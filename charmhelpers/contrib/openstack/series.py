# Copyright 2014-2018 Canonical Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Various utilies for dealing with Neutron and the renaming from Quantum.

from subprocess import check_output

from charmhelpers.core.hookenv import (
    config,
    log,
    ERROR,
    WARNING,
    INFO,
    status_set,
)

from charmhelpers.contrib.openstack.utils import (
    os_release,
    clear_unit_upgrading,
    CompareOpenStackReleases,
    set_unit_upgrading,
    is_unit_paused_set,
    clear_unit_paused,
)

UPGRADE_LOG = '/var/log/juju/do_release_upgrade.log'


def prepare_upgrade(pause_unit=None, configs=None):
    log("XXX: Running prepare series upgrade hook")
    # Stop servies
    # pause?
    # set status

    state = "blocked"
    msg = "Ready for do_release_upgrade, reboot, set complete when finished"
    set_unit_upgrading()
    if pause_unit and not is_unit_paused_set():
        pause_unit(configs)
    status_set(state, msg)


def complete_upgrade():
    log("XXX: Running complete series upgrade hook", WARNING)
    # Run config_changed hook
    clear_unit_paused()
    clear_unit_upgrading()


def do_upgrade():
    # This method in particular is purely for testing and should not be used
    # in production

    log("XXX: Running complete series upgrade hook", WARNING)
    status_set(
        "maintenance",
        "Running do_release_upgrade, reboot, set complete when finished")
    check_output(["juju-updateseries",
                  "--from-series", "trusty",
                  "--to-series", "xenial"])
    cmd = ['do-release-upgrade', '-f', 'DistUpgradeViewNonInteractive']
    results = check_output(cmd)
    with open(UPGRADE_LOG, 'wb') as upgrade_log:
        upgrade_log.write(results)
    status_set("blocked", "Do upgrade complete, reboot, set complete")
    check_output(["reboot"])
    exit(0)
