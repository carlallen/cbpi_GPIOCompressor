# GPIOCompressor for CraftBeerPi

There are two types of compressor
- GPIOCompressor: A standard GPIO output compressoror
- RelayCompressor: A GPIO compressor with inverted output

Both accept a number of minutes to delay before allowing turning the compressor back on again. The switch will display as though it is on, but the GPIO will not trigger unless enough time has elapsed.
