import re
import json

BTC_REGEX = re.compile(r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b")
XMR_REGEX = re.compile(r"4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}")
ETH_REGEX = re.compile(r"\b0x[a-fA-F0-9]{40}\b")
PGP_REGEX = re.compile(
    r"-----BEGIN PGP PUBLIC KEY BLOCK-----.*?-----END PGP PUBLIC KEY BLOCK-----",
    re.DOTALL,
)


def crypto_wallets(text):
    return {
        "btc": list(set(BTC_REGEX.findall(text))),
        "xmr": list(set(XMR_REGEX.findall(text))),
        "eth": list(set(ETH_REGEX.findall(text))),
    }


def pgp_keys(text):
    return PGP_REGEX.findall(text)


def named_entities(text):
    # Dummy: bisa pakai spaCy atau stanza
    return {"persons": [], "organizations": []}
