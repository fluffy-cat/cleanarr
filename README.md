## Blacklist Filter Logic

- Sequentially run through a list of filters
- If a filter returns true, continue testing with the next filter
- If a filter returns false, reject the download and end the test
- If all filters have returned true and the test has reached the end of the run, accept the download

## Current Filter Logic

Reject if:

- Download contains an .scr file
- Download has no video files (ie mkv, avi, mp4)
