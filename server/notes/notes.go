package notes

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/go-audio/audio"
	"github.com/go-audio/wav"
)

type NotesDefinition struct {
	Notes    string `form:"notes"`
	EDO      int    `form:"edo"`
	Timbre   string `form:"timbre"`
	Duration int    `form:"duration"`
}

const sampleRate = 44100
const bitDepth = 16
const numChannels = 1
const audioFormat = 1
const trailingMs = 1000

func CreateNotes(d NotesDefinition, w io.WriteSeeker) error {
	encoder := wav.NewEncoder(w, sampleRate, bitDepth, numChannels, audioFormat)

	var notes [][]int
	err := json.Unmarshal([]byte(d.Notes), &notes)
	if err != nil {
		return err
	}

	var numFrames int = (d.Duration*len(notes) + trailingMs) * sampleRate / 1000
	var pcm []int = make([]int, numFrames)
	for i := range pcm {
		pcm[i] = 0
	}

	for groupIndex, noteGroup := range notes {
		offset := d.Duration * groupIndex * sampleRate / 1000

		for _, note := range noteGroup {
			filename := fmt.Sprintf("./static/wav/%s/%dedo/%d.wav", d.Timbre, d.EDO, note)
			file, err := os.Open(filename)
			if err != nil {
				return err
			}

			dec := wav.NewDecoder(file)
			buf, err := dec.FullPCMBuffer()
			if err != nil {
				panic(err)
			}
			for frameIndex := range min(len(buf.Data), len(pcm)-offset) {
				pcm[offset+frameIndex] += buf.Data[frameIndex]
			}
		}
	}

	encoder.Write(&audio.IntBuffer{
		Format:         &audio.Format{SampleRate: sampleRate, NumChannels: numChannels},
		Data:           pcm,
		SourceBitDepth: bitDepth,
	})
	encoder.Close()

	return nil
}
