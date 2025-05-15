# datascipsych_finalproject

## Replication of Experiment 1: Processing Fluency and Source Memory

This project replicates Experiment 1 from Huang and Shanks (2021), "Examining the relationship between processing fluency and memory for source information." The experiment investigates how perceptual processing fluency relates to source memory accuracy.

### Background

Memory judgments in item recognition tests can be influenced by familiarity-based processes like processing fluency. While traditional accounts of source memory suggest minimal impact of familiarity, recent work indicates that source memory judgments can be affected when test stimuli are processed with greater fluency due to priming. This experiment investigated whether identification response times (a measure of processing fluency) are related to source memory accuracy.

### Experiment Design

In Experiment 1, participants (N=48) studied words presented with different source attributes:
- Font size (small/large)
- Screen location (upper/lower)

During the test phase, participants:
1. Identified words that gradually clarified on screen through progressive demasking (CID-R task)
2. Made old/new and remember/know/guess judgments
3. Provided confidence ratings for source memory (font size and location)

Response times (RTs) from the identification task formed the basis of a fluency measure, which were compared across categories of:
- Item recognition (hits, misses, false alarms, correct rejections)
- Source memory accuracy (0, 1, or 2 correct source dimensions)
- Subjective experience (remember, know, guess)

### Analysis & Results

Key analyses in this replication:
1. Computation of hit rates and false alarm rates
2. Two-way repeated-measures ANOVA examining the relationship between subjective old/new judgments and actual old/new status on identification RTs
3. Comparison of identification RTs across R/K/G judgments
4. Analysis of identification RTs based on source memory accuracy
5. Reproduction of Table 1 showing source accuracy frequencies and confidence ratings

The findings demonstrate that identification RTs were faster in trials with correct retrieval of source information compared with trials where source information was not accurately retrieved, consistent with the assumption that familiarity-based processes are related to source memory judgments.


### Getting Started

1. Clone this repository:
git clone https://github.com/LinzanLiu/datascipsych_finalproject.git

2. Install dependencies:
pip install -e .

3. Run the analysis notebook:
jupyter lab jupyter/replication.ipynb

### Reference

Huang, T. S.-T., & Shanks, D. R. (2021). Examining the relationship between processing fluency and memory for source information. Royal Society Open Science, 8(4), 190430. https://doi.org/10.1098/rsos.190430

