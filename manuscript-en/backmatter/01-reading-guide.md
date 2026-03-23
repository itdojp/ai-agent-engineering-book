# Reading Guide

This reading guide is for the point after a reader has finished the chapter prose and repo artifacts and wants durable sources that deepen understanding. It favors reuse value over exhaustiveness.

## How to Use This Guide

- Return first to the manuscript and repo artifacts in this book
- Then read the official docs for the tool or platform you actually use
- Use books and handbooks to strengthen organizational judgment, not to replace local artifacts
- The goal is not academic completeness. The goal is durable next-step reading

## Prompts and Requirements Shaping

| Source | What It Strengthens | Related Chapters |
|---|---|---|
| Official prompting guide for the model in use | Prompt Contracts, constraint design, tool-use assumptions | CH02, CH04 |
| Official eval docs for the model in use | Case design, rubrics, version comparison | CH04 |
| Michael Nygard, *Architecture Decision Records* | Writing short and durable design decisions | CH03 |
| Internal product-spec and acceptance-criteria templates | The threshold for turning exploratory dialogue into implementation-ready artifacts | CH03 |

## Context and Repo Design

| Source | What It Strengthens | Related Chapters |
|---|---|---|
| Official docs for the agent runtime in use | Instruction layering, workspace access, session handling | CH05, CH06, CH07, CH08 |
| Internal repo maps, architecture docs, and coding standards | Canonical repo context and clearer ownership | CH06 |
| Internal handoff, incident, and change-log rules | Session memory, restart packets, and resume discipline | CH07, CH11 |

## Verification, Reliability, and Operations

| Source | What It Strengthens | Related Chapters |
|---|---|---|
| Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google* | Change management, review discipline, testing, and documentation practice | CH03, CH06, CH10, CH12 |
| Betsy Beyer et al., *Site Reliability Engineering* | Reliability, operational responsibility, and service thinking | CH09, CH10, CH12 |
| Betsy Beyer et al., *The Site Reliability Workbook* | Checklists, runbooks, and implementation-focused operations design | CH09, CH10, CH11, CH12 |
| Nicole Forsgren, Jez Humble, Gene Kim, *Accelerate* | Metrics, throughput, and operational improvement | CH10, CH12 |

## How to Choose Which Source to Read Next

- If a prompt question is unclear, return first to official docs and local eval artifacts
- If a context question is unclear, return first to repo artifacts and ownership documents
- If a harness question is unclear, return first to verify, evidence, and review policy
- Books and handbooks should reinforce judgment, not replace local artifacts
