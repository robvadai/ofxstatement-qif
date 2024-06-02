OFX Statement QIF plugin
========================

![Workflow Status](https://github.com/robvadai/ofxstatement-qif/actions/workflows/test.yaml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/robvadai/ofxstatement-qif/badge.svg?branch=main)](https://coveralls.io/github/robvadai/ofxstatement-qif?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Summary

Converts [Quicken Interchange Format (QIF)](https://en.wikipedia.org/wiki/Quicken_Interchange_Format) formatted bank transaction files to [Open Financial Exchange (OFX)](https://en.wikipedia.org/wiki/Open_Financial_Exchange) format.

It is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement).

## Installation

```shell
pip install ofxstatement-qif
```

## Usage

```shell
ofxstatement convert -t qif transactions.qif transactions.ofx
```

## Configuration

```shell
ofxstatement edit-config
```

And enter e.g. this:
```ini
[qif]
plugin = qif
currency = USD
account = Quiffen Default Account
separator = \n
day-first = true
encoding = utf-8
```