# genai-mental-health-thematic-analysis
Overview:
This repository contains a Python-based data processing pipeline developed to support a thematic analysis of Reddit posts examining how users engage with generative AI chatbots in mental health contexts. The project focuses on understanding user experiences, sentiment, and how individuals position AI chatbots (e.g., as supplementary tool, alternative, or primary support) within their mental health practices.
  
Objectives:
  Prepare Reddit data for qualitative thematic analysis,
  Clean and standardize unstructured text data,
  Filter posts based on relevance to AI and mental health,
  Generate a structured sample for manual coding and analysis, and
  Support downstream analysis of sentiment and user positioning

Methods & Approach:
The pipeline was developed using Python and follows a structured preprocessing workflow:
1. Data Separation
  Extract relevant fields (title, body, timestamps, etc.)
2. Data Cleaning
  Remove noise (formatting issues, missing values, inconsistencies)
  Standardize text for analysis
2. Filtering
  Apply inclusion/exclusion criteria
  Retain posts related to generative AI and mental health experiences
4. Sampling
  Generate a representative subset of posts for thematic analysis

This preprocessing pipeline supported an inductive thematic analysis, allowing patterns and themes to emerge directly from the data.

Research Focus:
The broader study investigates:
  Generative AI in mental health contexts,
  User experience (UX) with AI chatbots,
  Chatbot positioning (supplement, alternative, or limited support), and
  Sentiment toward AI use (positive, negative, mixed, neutral)

├── scripts/
│   ├── 01_data_separation.py
│   ├── 02_data_cleaning.py
│   ├── 03_filtering_posts.py
│   └── 04_sampling_posts.py
│
├── data/
│   └── README.md
│
│
├── requirements.txt
├── .gitignore
└── README.md

Requirements
Install dependencies with:
pip install -r requirements.txt

Data Availability
Raw Reddit data are not included in this repository to protect user privacy and comply with research and ethical guidelines.

Outcomes:
This pipeline supported:

The development of a thematic coding framework,
Identification of key themes (emotional support, self-understanding, limited/risky support), and
Analysis of user sentiment and AI positioning

The findings contribute to understanding how generative AI is being integrated into real-world mental health practices.

Author:
Aayush Rabadey
Master of Professional Science in Biomedical Health Informatics
UNC Chapel Hill
