# Changelog

All notable changes to the Nordic Semiconductor Technical Documentation Style Guide are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Main Branch]

### Changed
- Aligned the unit symbol entry in the "Do not use a hyphen" table in `dashes-and-hyphens.md` with the rule for spelled-out units used as modifiers.
- Added an explanation of when to use a hyphen or a space between a number and a unit used as a modifier to `dashes-and-hyphens.md`.

## [Release 1.0.1] - 2026-07-30

### Added
- Added DITA-specific guidelines and integrated them into related style topics.
- Added Auracast to the glossary.
- Added brief release and deployment guidelines for the github pages site.

### Changed
- Updated style guidance across grammar, content structure, procedures, punctuation, planning, and writing tips based on editorial feedback.
- Standardized Bluetooth terminology throughout the guide.
- Updated repository references and site configuration for the `techdocs-style-guide` repository.
- Updated ignored development artifacts.

### Fixed
- Fixed an encoding issue in the beginner-friendly MCP server.

## [Release 1.0.0] - 2026-03-12

### Added

#### Capitalization (`capitalization.md`)
- Added proper noun identification guidelines with article test
- Added structural document references (Chapter, Section, Table, Example capitalization rules)
- Added multi-volume documentation capitalization (Part I, Part II)
- Added page number formatting guidelines
- Added illustration labels and callouts capitalization
- Added input device controls capitalization (keyboard keys, buttons, switches)
- Added technical notation guidelines (hexadecimal, architecture, dimensions)
- Added variables and placeholders formatting rules
- Added physical component labels guidelines
- Added emphasis methods section

#### Contractions (`writing-tips/index.md`)
- Added guidance on spelling out contractions for critical instructions
- Added apostrophe ambiguity guidelines (possessive vs contraction)
- Added "it's" vs "its" confusion prevention
- Added regional and nonstandard contractions to avoid
- Added subject-verb agreement rules for contractions

#### Grammar: -ing words (`grammar/ing-words.md`)
- Expanded from 13 to 109 lines with comprehensive guidance
- Added "Understanding dual-meaning problems" section
- Added solutions for -ing word ambiguity (5 strategies)
- Added practical guidelines for headings, procedures, descriptions, and warnings

#### Numbers (`numbers.md`)
- Added industry specifications exception for numerals
- Added technical specifications with numeric values section
- Expanded fractions and decimals guidance with 4 subsections:
  - Positioning fractional components
  - Choosing between fractional and decimal formats
  - Symbol versus written form
  - Plural forms with fractional quantities

#### Pronouns (`grammar/nouns-pronouns.md`)
- Added pronoun reference distance section
- Added reading flow test for evaluating pronoun clarity
- Added techniques to strengthen weak pronoun links
- Added guidance for paragraph and section boundaries
- Added demonstrative pronouns in technical contexts
- Added ownership pronouns in hardware descriptions
- Added technical review checklist

#### Acronyms and abbreviations (`acronyms.md`)
- Added direct expression over abbreviated Latin (for example, specifically, and so on)
- Added navigation-aware term definitions for modular content
- Added preventing word-form confusion with punctuation
- Added density versus clarity optimization for tables and diagrams

#### Units of measurement (`units-of-measurement.md`)
- Added proper notation versus keyboard approximations
- Added measurement system bridging strategies
- Added temporal interval formatting guidelines
- Added industry convention conflicts guidance

#### Punctuation

##### Parentheses (`parentheses.md`)
- Created new Parentheses file.

##### Apostrophes (`apostrophes.md`)
- Added apostrophe rules for inanimate objects, compound constructions, joint/individual ownership, and letter plurals

##### Colons (`colons.md`)
- Added "Common colon misuses" section with error-pattern teaching

##### Dashes and hyphens (`dashes-and-hyphens.md`)
- Added en dash usage for list term separators
- Added en dash usage for reference numbering (Figure, Table, Example)
- Added nonbreaking hyphens section with guidance for key combinations, product identifiers, and technical compounds

##### Periods (`periods.md`)
- Added technical terminology guidance (periods as "dots")
- Added current directory notation for Unix-like systems

##### Quotation marks (`quotation-marks.md`)
- Added "Don't use quotation marks" section for commands and technical elements
- Added guidance to use code formatting instead of quotation marks for literal text

##### Semicolons (`semicolons.md`)
- Added conjunctive adverb usage guidance
- Added "Rewrite complex semicolon lists" section with conversion examples

##### Slashes (`slashes.md`)
- Added "Why slashes create translation challenges" section explaining multiple meanings

### Changed

#### Punctuation: commas (`commas.md`)
- Replaced generic examples with Nordic-specific technical examples:
  - Firmware signature verification
  - MCU initialization
  - Status LED behavior
  - nRF Connect SDK features
  - Nordic Semiconductor contact information
  - SoC descriptions
  - ISO 8601 timestamp formatting

## [Release 0.1.0] - 2023-11-16

### Added
- Initial fork of Nordic Technical Documentation Style Guide
- Base documentation structure with comprehensive style guidance
- Grammar, punctuation, and content structure guidelines
- Planning and procedures documentation
- Writing tips and bias-free communication guidance

