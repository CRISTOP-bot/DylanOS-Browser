<!--
This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
-->

# DylanOS Browser

DylanOS Browser is a community fork of Zen Browser, based on Firefox. This repository preserves upstream MPL 2.0 notices and source availability for modified MPL-covered files. The DylanOS name and original artwork are separate branding assets.

## Product changes

- Crimson/DylanOS browser identity and original D-mark app icons.
- Zen vertical tabs and workspaces remain central; new profiles also get Firefox profile management, tab groups and split view enabled.
- Keep built-in privacy protections, signed extensions and security updates enabled.
- Session persistence is slightly less frequent (30 seconds) to reduce routine disk writes; performance gains are not claimed without benchmarks.

## Build status

These are source and branding changes only. No DylanOS Browser binary has been built or tested yet. Follow upstream build instructions and test Linux release artifacts before distribution.

The workflow `DylanOS Browser source checks` validates brand metadata, preferences, MPL notices and icon file formats on pushes and pull requests to `dev`. It is not Firefox compilation or runtime QA.
