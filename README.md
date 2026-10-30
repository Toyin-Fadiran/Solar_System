Yorùbá Video-to-English Subtitles
MVP / Proof of Concept — Project Walkthrough

Project goal: Transform a Yorùbá-language video into readable, timestamped English subtitles using locally run AI models, open-source tooling, Python automation, and human review.

Outcome: A manually refined English .srt file with timestamps derived from forced alignment, ready for playback and private review on YouTube.

Table of Contents
Project Overview
Workspace and File Organization
Transcript Preparation
Forced Alignment with CTC-Forced-Aligner
Converting Word Timings into Subtitle Cards
Evaluating Local Translation Models
Building the Translation Pipeline
Full-Context Translation Experiment
Human-in-the-Loop Refinement
Final Delivery Through YouTube
Tools and Technologies
Key Engineering Decisions
Lessons Learned
Reproducibility and Handover Checklist
1. Project Overview

The project followed a modular workflow:

Obtain a Yorùbá transcript from speech recognition.
Clean and inspect the transcript.
Align the transcript to the original audio.
Convert word-level timestamps into readable subtitle cards.
Translate the cards into English using a local language model.
Generate an English SRT while preserving the original timing structure.
Compare against a full-context English translation.
Manually refine the English subtitles.
Prepare the finished video for private review.

The central architectural principle was to separate transcription, alignment, translation, subtitle formatting, and quality control rather than asking a single model to perform everything.

The result was a practical MVP, not a fully automated production translation system.

2. Workspace and File Organization

The project was developed on Linux inside a Python virtual environment.

bash
cd ~/compare_all_texts
source .venv/bin/activate


A dedicated experiment directory kept intermediate files separate from the original material:

text
compare_all_texts/
├── .venv/
├── translate_yoruba_srt.py
├── check_timestamps.py
└── alignment_test/
    ├── alignment_test.wav
    ├── malik_freeman_transcript_test.txt
    ├── yoruba_draft.srt
    ├── english_full.json
    ├── english_pilot.json
    └── malik_freeman_english.srt


This is a representative list of project artifacts, not an exhaustive inventory of every file created during experimentation.

Engineering decision: preserve the original media and transcript, and use separate files for every major processing stage.

This makes experimentation reversible and allows intermediate results to be inspected independently.

3. Transcript Preparation

The first linguistic artifact was a Yorùbá transcript, including a cleaned test transcript named:

malik_freeman_transcript_test.txt

The transcript required attention to Unicode representation and Yorùbá orthography.

Examples of important characters include:

ẹ
ọ
ṣ
Tone-marked vowels such as é, è, and ẹ́

Unicode normalization was investigated using Python's unicodedata module. This matters because two strings can look identical while using different underlying character representations.

The installed aligner's text-normalization implementation was also inspected to understand its handling of punctuation, numbers, case, Unicode normalization, and romanization.

Important distinction: Unicode normalization improves consistency; it does not correct transcription errors. Likewise, romanization is not automatically appropriate for a language already written in Latin script.

The goal was to preserve the linguistic information needed for accurate alignment and translation.

4. Forced Alignment with CTC-Forced-Aligner
Objective

The task was to assign timestamps to an existing transcript, not to transcribe the audio again.

CTC-Forced-Aligner was installed in the Python environment and its command-line interface was inspected:

bash
ctc-forced-aligner --help


The inspected version used this default alignment model:

text
MahmoudAshraf/mms-300m-1130-forced-aligner


The model is based on Meta's multilingual speech-model family.

Working command

After correcting an initial relative-path mistake, the command was run from the project root:

bash
ctc-forced-aligner \
  --audio_path alignment_test/alignment_test.wav \
  --text_path alignment_test/malik_freeman_transcript_test.txt \
  --language yor \
  --romanize \
  --split_size word \
  --device cpu


The first attempt failed because the audio path was incorrect. Running from the correct directory with the correct relative path resolved that issue.

Inspecting the results

The aligner generated word-level timing artifacts, including .txt and .json files.

The output was inspected with:

bash
head -n 20 alignment_test/alignment_test.txt
python check_timestamps.py


The diagnostic reported:

text
Total aligned segments: 2336
First segment: 0.14–0.26 seconds
Last segment: 683.58–684.00 seconds


Some punctuation-only segments had zero duration, and several short words occupied very small intervals. These findings prompted further inspection rather than an assumption that every timestamp was correct.

Engineering decision: use forced alignment as an intermediate timestamping step, not as proof that the transcript is perfect.

A forced aligner can struggle when the supplied words differ from the audio or when the acoustic model does not adequately represent the language.

5. Converting Word Timings into Subtitle Cards

Word-level timestamps are useful for alignment, but they are generally too fragmented for ordinary subtitles.

A separate Python conversion stage grouped the words into readable, sentence-like units.

The resulting draft was:

alignment_test/yoruba_draft.srt

It contained 207 subtitle cards.

Example:

srt
1
00:00:00,140 --> 00:00:02,640
Òun ló mú kó jẹ́ pé kí n mú àbá kan wá.

2
00:00:02,640 --> 00:00:04,540
Ẹ wà pẹ̀lú mi o, ẹ̀yin tèmi.


The conversion preserved the chronological order of the words while grouping them into subtitle-sized passages.

The output was inspected at the beginning and end, and a timestamp-checking script was used to examine suspicious segment durations.

Engineering decision: distinguish alignment granularity from subtitle granularity. The aligner provides word timings; a separate process decides how those words should be grouped for reading.

6. Evaluating Local Translation Models

Rather than immediately relying on a cloud translation service, the project used Ollama to run language models locally.

The available models were inspected with:

bash
ollama list


The relevant models were:

Model	Purpose
hf.co/CohereLabs/tiny-aya-earth-GGUF:Q4_K_M	Primary translation model
gemma2:2b	Additional local model available for experimentation
qwen3:14b	Larger-model experiment

Tiny Aya Earth was selected as the working baseline after comparison with Qwen3 on sample material.

Direct API experimentation

Ollama exposes a local HTTP API that can be called directly from the terminal or from Python.

A representative request used these generation options:

json
{
  "temperature": 0.1,
  "top_p": 0.95,
  "num_ctx": 8192,
  "num_predict": 150,
  "repeat_penalty": 1.0
}


The low temperature was intended to encourage consistent, restrained output. The context and prediction limits controlled the amount of input and generated text.

These settings influence generation behavior; they do not guarantee translation accuracy.

A concrete failure

In an early test, the model translated àbá as a blanket in a sentence where the intended meaning was closer to a suggestion or proposal.

That example illustrated a central risk: fluent English can still be semantically wrong.

Engineering decision: evaluate models on the actual source material and retain human review, rather than selecting a model solely because of its size or published multilingual claims.

7. Building the Translation Pipeline

The first translation approach worked on individual subtitle cards. It encountered missing entries, inconsistent numbering, and context-dependent mistranslations.

The workflow was therefore expanded into a Python script:

translate_yoruba_srt.py

Responsibilities of the script
Parse the source SRT.
Submit batches of cards to Tiny Aya through Ollama.
Include neighboring cards as context.
Request structured JSON translations.
Validate the model's returned entries.
Preserve original subtitle IDs and timestamp strings.
Save completed translations to a JSON checkpoint.
Retry incomplete batches and report errors.
Generate a separate English SRT.
Avoid overwriting an existing output unless explicitly requested.
Representative command
bash
python translate_yoruba_srt.py \
  --batch-size 5 \
  --context-before 3 \
  --context-after 3 \
  --temperature 0.1 \
  --top-p 0.95 \
  --num-ctx 8192 \
  --num-predict 2048 \
  --translations alignment_test/english_full.json \
  --output alignment_test/malik_freeman_english.srt


The command illustrates the configurable properties of the translation stage. The exact options available depend on the version of the script being run.

Why structured JSON mattered

The model was asked to provide English translations, while Python retained ownership of the subtitle structure.

This avoided asking the model to reproduce timestamps or reconstruct the SRT format itself.

The JSON checkpoint also made the workflow more resilient. If a batch failed, completed translations could be retained and reused instead of repeating all the work.

Engineering decision: let the language model handle language, and let deterministic code handle IDs, timestamps, validation, and file generation.

8. Full-Context Translation Experiment

The project also explored translating a longer, continuous passage using the cleaned Yorùbá transcript.

The purpose was to give Tiny Aya enough context to understand the speaker's argument, recurring expressions, and references across sentence boundaries.

A separate English reference, master_english.txt, was produced for comparison with the timestamped English draft.

The experiments highlighted three different strengths:

Individual cards: simple to process, but vulnerable to ambiguity and missing context.
Small groups of cards: better continuity while retaining a manageable output structure.
Full-context translation: a stronger reference for understanding the overall meaning, but not automatically aligned to the original timestamps.

The full-context translation was valuable because a sentence that looks ambiguous in isolation may become clear when the surrounding argument is understood.

However, translating an entire passage does not establish where each translated sentence belongs in the audio.

A semantically correct sentence can still be assigned to the wrong timestamp interval if the alignment between the two texts is not established reliably.

A larger model was also tested, but Qwen3 14B produced worse results on the initial sample. The project therefore retained Tiny Aya Earth rather than assuming that a larger model would necessarily perform better.

Engineering decision: use full-context translation as a linguistic reference, not as a replacement for the timestamped subtitle structure.

9. Human-in-the-Loop Refinement

The most consequential decision was to stop short of automatically merging the full-context translation into the timestamped SRT.

The timestamped English draft was already useful. The full-context translation often conveyed the speaker's meaning more clearly, but automatically replacing subtitle text introduced risks:

Sentences could drift into the wrong time interval.
Translated sentences might not correspond cleanly to individual subtitle cards.
A sentence could become too long to read comfortably.
The resulting subtitles could be linguistically good but poorly synchronized.

The final workflow therefore used both artifacts for different purposes:

The timestamped SRT remained the authoritative timing source.
The full-context English translation served as a reference for meaning and continuity.
The subtitle text was manually refined.
The original timing lines and subtitle IDs were preserved.
The finished subtitles were intended to be checked against actual playback.

This was not a rejection of automation. It was a decision to allocate human effort where it delivered the greatest improvement.

Engineering decision: automate the repetitive operations and use human judgment for meaning, fluency, and timing-sensitive refinement.

The resulting SRT was a human-reviewed translation built on automated alignment.

10. Final Delivery Through YouTube

The original video was a QuickTime movie of approximately 515 MB.

Because the subtitle file is separate from the video, there was no need to re-encode the video merely to deliver an SRT.

The intended workflow was:

Upload the original video through YouTube Studio.
Keep the video Private during review.
Upload the final English .srt through the video's subtitle controls.
Watch the video with subtitles enabled.
Invite the colleague's Google account through YouTube's private-sharing controls.
Review feedback before deciding whether to publish more broadly.

Private sharing requires the invited viewer to use the account that was granted access. An unlisted video is different: anyone with its link can view it, so it is not equivalent to private sharing.

The SRT also remains an independent, reusable deliverable that can be archived or edited later.

11. Tools and Technologies
Component	Tool or artifact	Purpose
Operating environment	Linux	Local processing
Python isolation	.venv	Dependency management
Speech recognition	Initial ASR stage	Obtain the Yorùbá transcript
Text inspection	Python, Unicode normalization	Identify text representation issues
Forced alignment	CTC-Forced-Aligner	Associate words with audio timestamps
Acoustic model	MMS-300M multilingual aligner	Generate alignment emissions
Subtitle construction	Python conversion script	Group words into readable SRT cards
Local model runtime	Ollama	Run translation models locally
Translation model	Tiny Aya Earth GGUF, Q4_K_M	Generate English translation drafts
Translation orchestration	translate_yoruba_srt.py	Batching, context, validation, checkpointing
Full-context reference	master_english.txt	Understand the complete argument
Human editing	Subtitle editor	Refine English while preserving timing
Delivery	YouTube Studio	Private review and subtitle playback

Documentation note: the exact original ASR model and command should be recovered from the project's original notes if a fully reproducible record is required. They are not established by the alignment and translation commands documented here.

12. Key Engineering Decisions
12.1 Preserve the source artifacts

Original media, cleaned transcripts, alignment outputs, translation drafts, and final subtitles were kept separate.

This made it possible to revisit earlier stages without destroying the source material.

12.2 Separate alignment from translation

Alignment determines where supplied words fit into the audio. Translation determines what those words mean in another language.

Neither operation guarantees the correctness of the other.

12.3 Separate subtitle timing from subtitle wording

The original timestamps were treated as data that should remain unchanged during linguistic refinement.

This prevented a translation experiment from accidentally damaging the synchronization work.

12.4 Use structured data between stages

JSON checkpoints made translation progress inspectable and resumable. The SRT was generated from the translations and original timings rather than being reconstructed entirely by the model.

12.5 Evaluate models empirically

Tiny Aya Earth was retained because it was useful on the actual material. Qwen3 14B was not retained simply because it was larger.

12.6 Keep a human in the loop

Automatic translation was used to produce a strong starting point. Human review was retained for subtle meaning, natural phrasing, and subtitle readability.

12.7 Know when to stop automating

An automatic full-text-to-timestamp merge would have added complexity and potentially introduced synchronization errors.

Manual refinement was the more reliable choice for this first iteration.

13. Lessons Learned
Clean the transcript before alignment, but preserve the original.
Treat forced alignment as timestamping, not as proof of transcription accuracy.
Keep word-level alignment and subtitle segmentation as separate operations.
Use contextual translation when the meaning depends on surrounding sentences.
Do not assume a larger model will outperform a smaller model on a particular low-resource language.
Let Python own subtitle IDs, timestamps, and file integrity.
Preserve the full-context translation as a reference even when it cannot be mapped directly to subtitle intervals.
Review translations for meaning, not just grammatical fluency.
Verify the final subtitle file against the audio.
Stop automating when additional automation creates more risk than value.
14. Reproducibility and Handover Checklist

Before archiving the MVP, retain the following:

Original video and source audio.
Original ASR transcript.
Cleaned Yorùbá transcript.
Exact alignment command and model identifier.
Word-level alignment JSON and text output.
Timestamped Yorùbá draft SRT.
check_timestamps.py and its diagnostic output.
translate_yoruba_srt.py and its chosen configuration.
Translation JSON checkpoint.
Full-context English reference.
Final manually refined English SRT.
Validation confirming that all subtitle IDs and timing lines remain intact.
A playback review confirming that the subtitles remain synchronized.
Notes on the original ASR model and command, if recoverable.
Recommended final integrity check

Compare the original timestamped SRT with the manually refined version and confirm that every subtitle ID and timing line is unchanged.

The desired invariant is:

The subtitle wording may change; the subtitle IDs and timing lines must remain identical.

This check turns manual editing into a controlled, verifiable transformation rather than an assumption that synchronization survived.

Conclusion

This MVP established a workable, modular path from Yorùbá speech to human-reviewed English subtitles.

The achievement was not complete automation. It was a practical division of labor:

Speech recognition provided the transcript.
Forced alignment supplied timestamps.
Python created and validated the subtitle structure.
Tiny Aya Earth generated translation drafts.
Full-context translation helped resolve ambiguity.
Human refinement delivered the final English subtitles.

The result is a reusable foundation for future videos. It can be improved incrementally without requiring a complete redesign of the workflow.

The guiding principle: automate the repetitive work, preserve intermediate artifacts, verify structural integrity, and reserve human judgment for the parts that matter most.


=================================================================================================
Solar System

A simple Python console program that lets users explore basic information about the planets in our Solar System. This project demonstrates foundational Python concepts such as lists, functions, modular programming, user input handling, and basic graphics using the turtle module.

How to Run

To launch the program, simply execute:

python planet_main.py


Make sure all supporting files (e.g., planet_data.py, planet_features.py, planet_ui.py, planet_opencredit.py) are located in the same directory.

Project Overview

This project was developed as part of my learning process while studying Introduction to Python by Y. Daniel Liang. It includes:

Searching for planets

Listing planets with moons

Showing planets that may support life

Displaying basic Solar System visuals using turtle

License

This project is open-source and released under the MIT License.
