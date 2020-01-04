# Remove long silences from all .wav files in a directory
# Modified from Kathryn Flack and Shigeto Kawahara's Textgrid_helper_Praat

form Silence remover
	sentence Directory /Users/cynthiazhong/Desktop/lrap/test/
endform

Create Strings as file list... list 'directory$'*.wav
numberOfFiles = Get number of strings

for ifile to numberOfFiles
	select Strings list
	fileName$ = Get string... ifile
	Read from file... 'directory$''fileName$'

	object_name$ = "'fileName$'" - ".wav"
	select Sound 'object_name$'

	#params: trimDuration, onlyAtStartAndEnd, minPitch, timeStep, 
	# silenceThreshold, minSilenceDuration, minSoundingDuration, textGrid, trimLabel
	do ("Trim silences...", 0.05, 1, 100, 0, -30, 0.05, 0.09, 0, "silence")

	trimmed_name$ = "'object_name$'" + "_trimmed"
	select Sound 'trimmed_name$'
	Write to WAV file... 'directory$''trimmed_name$'.wav

	select all
    minus Strings list
    Remove
endfor

select all
Remove