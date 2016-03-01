# RPM Packaging
This repo contains all my efforts towards packaging previously unpackaged
software in the RH environment. An illustrative example is Facebook's Mcrouter.

# License
This work is released under the `Try To Pay Me License` which is the `MIT License` with modifications:

`In case any money changes hands, please do make a sincere effort to give the original/upstream author some of it.`

# Layout
The repo is styled to be pulled as the home directory of a user of `rpmbuild` and `mock`.

# Building
* `spectool -g -A -R $SPEC` foreach SPEC in `rpmbuild/SPECS/*.spec`
* `rpmbuild -bs --rmsource $SPEC` foreach SPEC in `rpmbuild/SPECS/*.spec`
* `mockchain -l $RESULTDIR/ --log=$LOGFILE -r default  --recurse rpmbuild/SRPMS/*.src.rpms`
* Go flirt with your target of choice, in the hope that flirting will be as easy as package building.

# References
* http://rpm.org/wiki/Docs
* https://fedorahosted.org/mock/
