# Background usefulizer :)

Tool that makes backgrounds useful.  Specifically, by

* fetching cryptoasset prices
* producing plots
* and storing them in whatever folder configured as a backgrounds' source

**Note**: be careful to direct to a non-empty folder - the app is set to remove previous contents of the folder it was set to operate in

**To do**:
* replace `_savefig` with `Figure.savefig`
* make `super().__init__(description=__doc__)` honor newlines, instead of replacing it by spaces

## Use

See `buzfu --help`
