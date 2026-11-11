# IG feed re-ranker PoC

1. Register https://bugbounty.meta.com using your Facebook account.
2. In Profile --> Settings --> Researcher Settings, check "Enable the Meta Bug Bounty settings menu for FoA accounts"
3. Log into your IG account on your test device or emulator.
4. Go to IG settings --> Whitehat Settings --> Allow User Certificates
5. Download and set up mitmproxy on your computer.
6. Point your phone or emulator's proxy to your computer.
7. Go to mitm.it/ on your phone's browser, and follow the instructions to download the CA certificate.
8. Run `mitmdump -s ig_rerank.py` on your computer.
9. Scroll Instagram. You should see the re-ordered posts injected with "POS k/N" in the title.

If developing a standalone VPN app, steps 5-8 would involve downloading an application from the study website
and also installing a CA certificate.

To dump samples of the JSON feed, Instead of using the `ig_rerank.py` script, use
`ig_dump_responses.py` -- these will go to `sample_data/responses/<response_num>_<timestamp>.json`.

