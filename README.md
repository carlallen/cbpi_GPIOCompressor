# GPIOCompressor for CraftBeerPi

This plugin adds Actors for controlling compressors (like refridgerators/freezers). To prevent damage to the compressor, you should not turn the compressor on and off repeatedly. It's best to have a delay between cycles. This actor allows for that delay.

There are two types of compressor
- GPIOCompressor: A standard GPIO output compressoror
- RelayCompressor: A GPIO compressor with inverted output

Both accept a number of minutes to delay before allowing turning the compressor back on again. The switch will display as though it is on, but the GPIO will not trigger unless enough time has elapsed.

Future Features
- Trigger GPIO if state is still "on" and wait time has elapsed
