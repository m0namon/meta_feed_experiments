Sample JSON data returned from the timeline/ endpoint from Instagram 450.0.0.50.77 / 385611438.

`feed.json` is a full response with 5 items that can appear in the feed. It contains every "type" of object, including:
 * `media_or_ad`: either a regular post or an ad
 * `explore_story`: injected Reels post, wraps a "nested" `media_or_ad` post from Reels
 * `suggested_users`: "Suggested for you" account recommendation.

Interestingly enough, for this version of IG, ads include `ad_debug_info`, which contain insanely rich detail about the ad including bidding data, expected conversion rates, etc. Samples of the full ad object can be found in `ad_full/`.

NOTE:
This data is from my personal `mona_traditional` IG account which I use for art and calligraphy. Please do not share as it may contain my personal connections, data from private profiles, etc.

