# -*- coding: utf-8 -*-
"""Tool to produce plots of cryptocurrency price data.

Be careful to direct to a non-empty folder - the app is set to remove
previous contents of the folder it was set to operate in.
"""


import argparse
import pathlib
import os

import requests
import cachetools
import pandas as pd
import matplotlib.pyplot as plt


NUM_SYMBOLS = 12
QUOTE_ASSET = "BTC"
NUM_DAYS = 180
BUFFER_DIR = "/tmp/buzfu"
SAVEFIG_CONF = dict(
    dpi=300,
    facecolor="white",
    bbox_inches="tight",
    pad_inches=1 / 32,
)


def main():
    """Entry point of the application."""
    args = _Parser().specify_args().parse_args()
    prev_contents = list(args.destination.iterdir())
    symbols = _get_symbols()
    chosen = pd.Series(
        symbol for symbol in symbols
    ).sample(n=NUM_SYMBOLS, replace=False)
    for symbol in chosen:
        series = _fetch_prices(symbol)
        fig = _make_plot(series)
        name = "%s.png" % series.name.lower()
        _savefig(
            fig,
            args.destination / name,
            **SAVEFIG_CONF
        )
    for file in prev_contents:
        file.unlink()


def _savefig(fig, fname, *args, **kwargs):
    final, buffer = (pathlib.Path(name) for name in (fname, BUFFER_DIR))
    temp = buffer / final.name
    if not buffer.exists():
        os.makedirs(buffer)
    fig.savefig(temp, *args, **kwargs)
    os.system(f"mv {temp} {final.parent}")


class _Parser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__(description=__doc__)

    def specify_args(self):
        default_destination = pathlib.Path(os.environ["HOME"]) / "Pictures"
        self.add_argument(
            "-d", "--destination",
            default=default_destination,
            type=pathlib.Path,
            help="defaults to %s" % default_destination
        )
        return self


@cachetools.cached(cachetools.TTLCache(1, ttl=60 * 60))
def _get_symbols():
    response = requests.get("https://api.binance.com/api/v3/exchangeInfo")
    if not response.ok:
        # Should I do something here?
        pass
    return {
        entry["symbol"] for entry in response.json()["symbols"]
        if entry["quoteAsset"] == QUOTE_ASSET and not (
            "UP" in entry["baseAsset"] or "DOWN" in entry["baseAsset"]
        )
    }


@cachetools.cached(cachetools.TTLCache(1024, ttl=60 * 60))
def _fetch_prices(symbol):
    response = requests.get("https://api.binance.com/api/v3/klines", params={
        "symbol": symbol,
        "interval": "1d",
        "limit": 1000,
    })
    if not response.ok:
        # Same here...
        pass
    return _make_series(response).rename(symbol)


def _make_series(response):
    return (
        pd.DataFrame(response.json())
            [[4, 6]]
            .set_axis(["price", "time"], axis=1)
            .assign(time=lambda frame: (
                frame["time"]
                    .apply(pd.Timestamp, unit="ms")
                    .apply(lambda entry: entry + pd.Timedelta(1, unit="ms"))
            ))
            .astype({"price": float})
            .set_index("time").squeeze()
    )


def _make_plot(series):
    fontsize = 6
    preprocessed = (
        series
            .tail(NUM_DAYS)
            .pipe(lambda series: series / series[-1])
    )
    figure = plt.figure()
    preprocessed.plot(
        fontsize=fontsize,
        linewidth=1 / 2,
    )
    plt.xlabel(None)
    plt.ylim(0, 2)
    plt.text(
        0.675, 0.85, _make_summary(preprocessed),
        transform=figure.axes[0].transAxes,
        fontsize=fontsize,
    )
    return figure


def _make_summary(series):
    return (
        "Asset: %s (%s)"
        "\nDays: %s"
        "\nSince: %s"
        "\nUntil: %s"
    ) % (
        series.name.replace(QUOTE_ASSET, ""),
        series.name,
        len(series),
        series.index.min(),
        series.index.max(),
    )


if __name__ == "__main__":
    main()
