# PyAudioSynth

This is a Python audio synthesizer by Yonatan Bashan
The synthesizer is non-interactive, i.e. it plays pre-written notes.

The available sound features are:
  Waveforms: Sine, Square, and Triangle. Triangle waveform is adjustable to be between pure triangle to sawtooth
  Modulations: FM modulations are available to sine wave form, AM modulations to any waveform
  Envelope: Envelope is available to all waveforms, with attack, decay, and two level stages as parameters
  Effect: Delay and noise effects are available

The general flow to create music using the synthesizer is as follows:

1. Create sounds: i.e. define waveform, and optionally modulations, envelopes and effects
2. Create channel: A channel is a class with a specific sound that stores the notes and audio required to play
3. Create note sheet: A note sheet is a sequence of notes, which can be assigned to any channel.
4. Populate note sheet:
	* Add musical notes to the sheet. You must specify note name(s) (i.e. "C4", "G#3", etc.) and lengths.
	* It is also possible to add silence, or sync to another note sheet's location if you are unsure how much silence is missing until the next part.
  
5. Assign note sheets to channels
6. Generate audio
7. Play!

See example of usage in program1.py which creates sounds, notes, channels, and eventually plays it all.



Future plannings:

* Add a parser to impelement note sheets easier
* Improve threading computation to be actual multiprocessing using multiple cores
* Implement frequenct filters using FFT tools
