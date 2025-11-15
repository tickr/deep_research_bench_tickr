# Four evaluation dimensions for final article quality
# 1. Comprehensiveness: Article covers key areas of the industry, ensures overall understanding, doesn't omit important parts
# 2. Insight/Depth: Article deeply analyzes causes, impacts and trends, provides valuable insights
# 3. Instruction-Following/Relevance: Article closely follows research topic, directly answers questions
# 4. Readability: Article has clear structure, fluent language, and is easy to understand

# Shared schema/constraints context block to include in all judge prompts.
_SCHEMA_AND_CONSTRAINTS_BLOCK = """
<report_schema_outline>
## Client And Service Information

## Executive Summary
### Ratings By LOB
### Recommendation Summary
- Critical
- Important
- Advisory
### Key Contacts

## Description Of Operations

## Loss Analysis

## Service Planning

## PCO Survey Sections
### Description Of Products Exposures
- End Product And Intended Use
- Key Customers
- Stream Of Commerce
- Process Flow
- Sales Distribution
- Additional Details
### PCO Operations Considered
- Conclusion Rating (1-4)
- Comments
### Loss Potential
- Frequency
- Severity
- Scenarios
- Comments
### Design & Engineering
- Rating (1-4)
- Comments (labels, warnings, IFUs, legal review)
### Production & Manufacturing
- Rating (1-4)
- Comments (suppliers, risk transfer, contracts, insurance)
### Regulatory Management
- Rating (1-4)
- Comments (regulatory standards, inspections, compliance history)
### Post-Market Surveillance & Recall
- Rating (1-4)
- Comments (CAPA, traceability, recall program, CRO interactions)
### Industry Exposures & Controls
- Rating (1-4)
- Comments (emerging hazards, exposures)
### Accident Investigations & Loss Analysis
- Rating (1-4)
- Comments (claims history, corrective actions, loss trends)

## Disclaimer
</report_schema_outline>

<mandatory_elements>
- Headings and order must match the outline exactly (use '##' for sections, '###' for subsections, exact casing).
- Under 'Executive Summary' include 'Recommendation Summary' with Critical, Important, Advisory.
- In 'PCO Survey Sections', each category requires a 1–4 rating with an evidence-backed rationale:
  - Design & Engineering; Production & Manufacturing; Regulatory Management;
    Post-Market Surveillance & Recall; Industry Exposures & Controls; Accident Investigations & Loss Analysis.
- For every mentioned risk, explicitly identify the underlying drivers/causal factors (emerging risk drivers) and ensure recommendations address those drivers.
- 'Loss Potential' must include Frequency, Severity, at least one Scenario, and Comments.
- Append the standard Disclaimer text verbatim after '## Disclaimer'.
</mandatory_elements>

<grounding_and_provenance_rules>
- All citations must be formatted as either bracketed named sources (e.g., [Data source (date)]) or a bracketed URL (e.g., [https://example.com]). Parenthetical URLs are non‑conforming and should be docked.
- Apply the same rule to both Tickr-derived and web-derived evidence; do not output raw Tickr tokens in-text.
- Key Contacts must be confirmed on official client-owned pages; otherwise output exactly:
  "Unknown — client to provide key contacts (Quality/Regulatory/Operations/EHS)."
</grounding_and_provenance_rules>

<sufficient_insights_criteria>
- ≥ 7 non-duplicative insights overall.
- Coverage across Rules / Frameworks / Controls (at least 1–2 relevant items each).
- Loss analysis includes a sector-relevant scenario with frequency/severity and provenance.
</sufficient_insights_criteria>

<standard_disclaimer_text>
Risk Control evaluations, reports, and recommendations are for underwriting support only.
</standard_disclaimer_text>

<sector_guidance_expectations>
- Explicitly reference at least one sector Rule (legal/regulatory) and one Framework (standard/program) where relevant.
</sector_guidance_expectations>
"""


# Prompt to generate evaluation dimension weights
generate_eval_dimension_weight_prompt = """
<system_role>
You are an experienced research article evaluation expert. You excel at deeply understanding the objectives, challenges, and core value points of specific research tasks, and based on this, setting **dynamic, reasonable, and well-supported** dimension weights for subsequent article quality assessment.
</system_role>

<user_prompt>
There is a deep research task as follows:
<task>
"{task_prompt}"
</task>

""" + _SCHEMA_AND_CONSTRAINTS_BLOCK + """

<instruction>
**Background**: The research team will conduct in-depth and comprehensive research based on the `<task>` above and ultimately produce a high-quality research article.
**Your Task**: As an evaluation expert, you need to set the evaluation criteria weights for this specific `<task>` for our assessment team. The evaluation will be conducted across the following four dimensions:
1.  **Comprehensiveness:** The breadth, depth, and relevance of information coverage.
2.  **Insight:** The depth, originality, logic, and value of the analysis and conclusions.
3.  **Instruction Following:** Whether the report accurately and completely responds to all requirements and constraints of the task.
4.  **Readability:** Clarity of structure, fluency of language, effectiveness of data presentation, and overall ease of understanding.

**Evaluation Formula**: Total Score = Comprehensiveness * Comprehensiveness Weight + Insight * Insight Weight + Instruction Following * Instruction Following Weight + Readability * Readability Weight. (**Note: The sum of all weights must be exactly 1.0**)

**Schema & Grounding Awareness (Critical for this environment)**
- Treat exact schema adherence and grounding/provenance compliance as first-class factors when allocating weights.
- If the task stresses regulatory conformance or ratings-driven evaluation (e.g., PCO categories and Loss Potential), increase emphasis on Instruction Following and Insight.
- If the task is breadth-heavy across multiple exposure areas, increase Comprehensiveness and Readability.

**Core Requirements**:
1.  **In-depth Task Analysis**: Carefully study the specific content of the `<task>`, its implicit goals, potential difficulties, and the core value of its outcomes.
2.  **Dynamic Weight Allocation**: Based on your analysis, assign weights to the four dimensions (use decimals between 0 and 1, e.g., 0.3). **The key is to understand that different tasks have different focuses, and weights must be flexibly adjusted according to task characteristics, not fixed.**
3.  **Justify Allocation Reasons**: Your analysis (`<analysis>`) **must clearly and specifically explain why each dimension is given a particular weight**, and **directly link the reasons to the requirements and characteristics of the <task>**, the `<report_schema_outline>`, and the **mandatory elements** (ratings, scenarios, Recommendation Summary, Disclaimer). Explicitly consider **provenance rules** when justifying the Instruction Following weight.
4.  **Standard Format Output**: Strictly follow the format of the example below, first outputting the `<analysis>` text with detailed reasons, and then immediately providing the `<json_output>` with the weight allocation results.

</instruction>

<examples_rationale>
The following two examples are provided to demonstrate **how to adjust evaluation dimension weights and explain the reasons based on changes in task nature**. Please focus on learning the **thinking logic and analytical methods** in these examples, rather than simply imitating their content or weight values.
</examples_rationale>

<example_1>
<task>
"Evaluate Design & Engineering and Post‑Market Surveillance readiness for a Class II medical device manufacturer to support underwriting risk rating and recommendations."
</task>
<output>
<analysis>
This task's core is to determine underwriting-relevant risk posture by assessing control effectiveness in high-impact categories. The value lies in the depth of causal analysis (why controls are weak/strong), linkage to sector Rules/Frameworks, and actionable recommendations tied to drivers of emerging risk. Therefore, evaluation emphasizes insight and comprehensiveness.
* **Insight (0.35):** Requires deep analysis of design control robustness (labels/warnings/IFUs/legal review) and post‑market systems (CAPA, traceability, recall program), identifying causal drivers and implications for risk.
* **Comprehensiveness (0.30):** Must cover schema-required categories, ratings, and loss pathways to provide a complete underwriting view.
* **Instruction Following (0.20):** Must adhere to the schema (1–4 ratings with rationales, Recommendation Summary, Disclaimer) and provenance rules.
* **Readability (0.15):** Clear rationales and scannable recommendations aid decision-making, but are secondary to analytical depth and coverage.
</analysis>
<json_output>
{{
    "comprehensiveness": 0.30,
    "insight": 0.35,
    "instruction_following": 0.20,
    "readability": 0.15
}}
</json_output>
</output>
</example_1>

<example_2>
<task>
"Produce a comprehensive PCO Liability Survey Report for an industrial equipment manufacturer, covering all required sections, ratings, and loss potential to support underwriting."
</task>
<output>
<analysis>
The core objective is to deliver a broad, accurate, schema-complete underwriting support report. The emphasis is on breadth of coverage across PCO sections, correctness of ratings and required subsections, and clear presentation of key information for scanning.
* **Comprehensiveness (0.40):** Must cover all PCO sections, ratings, and loss inputs (frequency/severity/scenarios) with adequate breadth and completeness.
* **Readability (0.25):** Presenting a large amount of structured risk information clearly and intuitively is key for reviewers.
* **Instruction Following (0.20):** Strict adherence to schema headings/order, Recommendation Summary, Disclaimer, and provenance formatting is a basic requirement.
* **Insight (0.15):** Some synthesis and prioritization add value, but the primary aim is coverage and clarity.
</analysis>
<json_output>
{{
    "comprehensiveness": 0.40,
    "insight": 0.15,
    "instruction_following": 0.20,
    "readability": 0.25
}}
</json_output>
</output>
</example_2>

Please strictly follow the above instructions and methods. Now, begin your work on the following specific task:
<task>
"{task_prompt}"
</task>
Please output your `<analysis>` and `<json_output>`.
</user_prompt>
"""


# Comprehensiveness
generate_eval_criteria_prompt_comp = """
<system_role>
You are an experienced research article evaluation expert. You excel at breaking down abstract evaluation dimensions (like "Comprehensiveness") into actionable, clear, and task-specific criteria, assigning appropriate weights and justifications for each.
</system_role>

<user_prompt>
**Background**: We are evaluating a deep research article written for the following task across four dimensions: Comprehensiveness, Insight, Instruction Following, and Readability.
1.  **Comprehensiveness:** The breadth, depth, and relevance of information coverage.
2.  **Insight:** The depth, originality, logic, and value of the analysis and conclusions.
3.  **Instruction Following:** Whether the report accurately and completely responds to all requirements and constraints of the task.
4.  **Readability:** Clarity of structure, fluency of language, effectiveness of data presentation, and overall ease of understanding.

<task>
"{task_prompt}"
</task>

""" + _SCHEMA_AND_CONSTRAINTS_BLOCK + """

<instruction>
**Your Goal**: For the **Comprehensiveness** dimension of this research article, develop a set of detailed, specific, and highly task-relevant evaluation criteria. You need to:
1.  **Analyze Task**: Deeply analyze the `<task>` to identify key information areas, perspectives, and depths that must be covered to achieve "comprehensiveness."
2.  **Formulate Criteria**: Based on the analysis, propose specific evaluation criteria items.
3.  **Explain Rationale**: Provide a brief explanation (`explanation`) for each criterion, stating why it is important for assessing the comprehensiveness of this `<task>`.
4.  **Assign Weights**: Assign a reasonable weight (`weight`) to each criterion, ensuring the sum of all criteria weights is exactly **1.0**. Weights should reflect the relative importance of each criterion in achieving the task's comprehensiveness goals.
5.  **Avoid Overlap**: Clearly focus on criteria related to the **Comprehensiveness** dimension, avoiding overlap with Insight, Instruction Following, or Readability.

6.  **Evidence Diversity & Argument Variety**: Include a distinct criterion that evaluates the diversity and independence of cited sources and the variety of perspectives/arguments presented, judged only from in-article citations and content. Accept only `[Data source (date)]` and bracketed URL `[https://…]`; explicitly dock parenthetical URLs `(https://…)` and any other non-conforming formats. Reward articles that explicitly weigh multiple considerations/perspectives.

**Core Requirements**:
1.  **Task-Centric**: Analysis, criteria, explanations, and weights must directly relate to the core requirements and characteristics of the `<task>`.
2.  **Well-Justified**: The `<analysis>` section must clearly articulate the overall thinking behind setting these criteria and weights, linking it to the `<task>`, the `<report_schema_outline>`, and **mandatory elements** (ratings, scenarios, Recommendation Summary, Disclaimer).
3.  **Criteria Diversity**: Criteria should minimize overlap and cover all aspects of comprehensiveness as thoroughly as possible, avoiding omissions.
4.  **Reasonable Weights**: Weight allocation must be logical, reflecting the relative importance of each item within the comprehensiveness dimension.
5.  **Standard Format Output**: Strictly follow the example format below, first outputting the `<analysis>` text, then immediately providing the `<json_output>`.
6.  **Source Diversity Focus**: Explicitly assess the diversity and independence of sources and arguments based on in-article citations and perspectives; do not assess off-article veracity. Accept only `[Data source (date)]` and bracketed URL `[https://…]`; explicitly dock parenthetical URLs `(https://…)` and any other non-conforming formats. Reward clear presentation of multiple considerations/trade-offs.
</instruction>

<example_rational>
The following example demonstrates **how to formulate comprehensiveness criteria based on task requirements**. Focus on learning the **thinking logic and analytical methods** from this example, not just imitating its content or weight values.
</example_rational>

<example>
<task>
"Assess PCO exposures and controls for a consumer electronics manufacturer and recommend risk control actions to support underwriting ratings."
</task>

<output>
<analysis>
To comprehensively evaluate a PCO Liability Survey Report for underwriting, considerations must span all schema-required sections and ensure complete coverage of exposures, controls, ratings, and loss inputs. The task has a dual objective: first, to analyze exposures and control effectiveness across PCO sections; second, to recommend actionable risk control actions and service planning tied to emerging risk drivers. Therefore, a comprehensive assessment must ensure the article covers required sections, provides ratings with rationales, integrates Rules/Frameworks/Controls, and details loss potential.

Specifically, evaluation criteria need to cover:
1.  **Coverage of Required Schema Sections**: All primary and subsection headings are present and populated, including Recommendation Summary and Disclaimer.
2.  **Ratings and Rationales Across PCO Categories**: Each required category has a 1–4 rating with an evidence-backed rationale.
3.  **Loss Potential Inputs**: Frequency, Severity, and at least one realistic Scenario with comments and provenance.
4.  **Integration of Rules/Frameworks/Controls**: Use of sector Rules and Frameworks to ground control evaluations and recommendations.
5.  **Diversity of Data Sources and Arguments**: Uses multiple independent sources and presents distinct perspectives; inline citations must be `[Data source (date)]` or bracketed URL `[https://…]`; parenthetical URLs are docked; avoids over-reliance on a single source.
6.  **Client/Service Information and Key Contacts**: Policy-compliant handling, including "Unknown" where evidence is absent.

Weight allocation should be balanced between coverage of PCO sections and the completeness of ratings/loss inputs, as both are critical to underwriting usefulness. Integration of Rules/Frameworks/Controls and evidence breadth are key to defensible conclusions.
</analysis>
<json_output>
[
  {{
    "criterion": "Coverage of All Primary Sections and Subsections per Schema",
    "explanation": "All '##' and '###' headings present and populated, including 'Recommendation Summary' and 'Disclaimer'.",
    "weight": 0.18
  }},
  {{
    "criterion": "Complete Ratings and Rationales in PCO Survey Sections",
    "explanation": "Each category has a 1–4 rating with an evidence-backed rationale.",
    "weight": 0.22
  }},
  {{
    "criterion": "Loss Potential Depth",
    "explanation": "Includes Frequency, Severity, at least one Scenario with comments and provenance.",
    "weight": 0.15
  }},
  {{
    "criterion": "Integration of Rules / Frameworks / Controls",
    "explanation": "Explicitly names at least one sector Rule and one Framework where relevant.",
    "weight": 0.15
  }},
  {{
    "criterion": "Diversity of Sources and Arguments",
    "explanation": "Multiple independent sources cited in-line across varied domains/types; presents differing perspectives and explicitly weighs multiple considerations/trade-offs; avoids single-source dependence; citations must be [Data source (date)] or bracketed URL [https://…]; parenthetical URLs are docked.",
    "weight": 0.20
  }},
  {{
    "criterion": "Key Contacts and Client/Service Information",
    "explanation": "Attempts to populate policy-driven items; declares 'Unknown' with needed evidence when applicable.",
    "weight": 0.10
  }}
]
</json_output>
</output>
</example>

Please strictly follow the above instructions and methods. Now, begin your work on the following specific task:
<task>
"{task_prompt}"
</task>
Please output your `<analysis>` and `<json_output>`.
</user_prompt>
"""


# Insight / Depth
generate_eval_criteria_prompt_insight = """
<system_role>
You are an experienced research article evaluation expert. You excel at breaking down abstract evaluation dimensions (like "Insight") into actionable, clear, and task-specific criteria, assigning appropriate weights and justifications for each.
</system_role>

<user_prompt>
**Background**: We are evaluating a deep research article written for the following task across four dimensions: Comprehensiveness, Insight, Instruction Following, and Readability.
1.  **Comprehensiveness:** The breadth, depth, and relevance of information coverage.
2.  **Insight:** The depth, originality, logic, and value of the analysis and conclusions.
3.  **Instruction Following:** Whether the report accurately and completely responds to all requirements and constraints of the task.
4.  **Readability:** Clarity of structure, fluency of language, effectiveness of data presentation, and overall ease of understanding.

<task>
"{task_prompt}"
</task>

""" + _SCHEMA_AND_CONSTRAINTS_BLOCK + """

<instruction>
**Your Goal**: For the **Insight** dimension of this research article, develop a set of detailed, specific, and highly task-relevant evaluation criteria. You need to:
1.  **Analyze Task**: Deeply analyze the `<task>` to identify areas requiring in-depth analysis, logical deduction, viewpoint synthesis, or value judgment to demonstrate "insight."
2.  **Formulate Criteria**: Based on the analysis, propose specific criteria focusing on analytical depth, logical consistency, originality, and the value of conclusions.
3.  **Explain Rationale**: Provide a brief explanation (`explanation`) for each criterion, stating why it is important for assessing the insight of this `<task>`.
4.  **Assign Weights**: Assign a reasonable weight (`weight`) to each criterion, ensuring the sum of all criteria weights is exactly **1.0**. Weights should reflect the relative importance of each criterion in demonstrating the task's insight objectives.
5.  **Avoid Overlap**: Clearly focus on criteria related to the **Insight** dimension, avoiding overlap with Comprehensiveness, Instruction Following, or Readability.

**Core Requirements**:
1.  **Task-Centric**: Analysis, criteria, explanations, and weights must directly relate to the core requirements and characteristics of the `<task>`.
2.  **Beyond Surface-Level**: Criteria should assess analytical depth, logical rigor, originality of insights, and value of conclusions, not just information listing.
3.  **Overall Report Depth**: Explicitly evaluate the overall analytical depth across critical schema sections (e.g., PCO Survey Sections, Loss Potential), not just isolated paragraphs.
4.  **Well-Justified**: The `<analysis>` section must clearly articulate the overall thinking behind setting these criteria and weights, linking it to the `<task>`, the ratings and their rationales in the `<report_schema_outline>`, and the sector Rules/Frameworks/Controls.
5.  **Reasonable Weights**: Weight allocation must be logical, reflecting the relative importance of each item within the insight dimension.
6.  **Standard Format Output**: Strictly follow the example format below, first outputting the `<analysis>` text, then immediately providing the `<json_output>`.
</instruction>

<example_rational>
The following example demonstrates **how to formulate insight criteria based on task requirements**. Focus on learning the **thinking logic and analytical methods** from this example, not just imitating its content or weight values.
</example_rational>

<example>
<task>
"Evaluate a pharmaceutical packaging supplier’s risk controls, justify 1–4 ratings across PCO categories, and provide loss scenarios and mitigation aligned to emerging risk drivers."
</task>

<output>
<analysis>
To evaluate the insight of a PCO Liability Survey Report, focus on analytical depth, logical strength, and the underwriting value of conclusions. The core involves analyzing product liability risk drivers, evaluating control effectiveness against sector Rules/Frameworks, constructing realistic loss pathways, and providing forward-looking, actionable recommendations tied to drivers.

Evaluation criteria should emphasize:
1.  **Identification and Analysis of Core Risk Drivers**: Deeply analyze mechanisms and relative importance of drivers (e.g., labeling adequacy, supplier qualification, CAPA maturity) altering exposure.
2.  **Sophistication in Uncovering Impacts**: Move beyond obvious findings to reveal second-order effects and cross-category interactions (e.g., design changes affecting recall traceability).
3.  **Logical Rigor of Recommendations**: Ensure recommendations are derived from evidence, linked to drivers, and consider implementation constraints and sequencing (Immediate/90d/6–12m).
4.  **Nuance in Risk Pathway Construction**: Provide realistic scenarios with clear precursors, failure modes, and expected frequency/severity.
5.  **Originality and Strategic Value**: Offer perspectives or control patterns that materially improve risk posture beyond boilerplate guidance.
6.  **Future Outlook and Adaptability**: Consider evolving regulations/standards and how controls should adapt.

Weight allocation should favor depth of driver analysis, rigorous recommendations linked to drivers, and high-quality scenario construction, as these most strongly evidence insight for underwriting decisions.
</analysis>
<json_output>
[
  {{
    "criterion": "Causal Rationale Behind 1–4 Ratings",
    "explanation": "Depth and specificity of why each category received its rating, grounded by evidence.",
    "weight": 0.20
  }},
  {{
    "criterion": "Linkage to Rules / Frameworks / Controls",
    "explanation": "Ratings and recommendations clearly tie to sector Rules/Frameworks and practical Controls.",
    "weight": 0.16
  }},
  {{
    "criterion": "Scenario Quality and Risk Pathways",
    "explanation": "Loss scenarios reflect realistic pathways, second-order effects, and sector nuances.",
    "weight": 0.16
  }},
  {{
    "criterion": "Actionability of Recommendations",
    "explanation": "Recommendations are concrete, time-phased (Immediate/90d/6–12m where applicable), and risk-reducing.",
    "weight": 0.15
  }},
  {{
    "criterion": "Handling of Uncertainty and Evidence Gaps",
    "explanation": "Clearly marks unknowns and specifies required evidence; avoids speculation.",
    "weight": 0.10
  }},
  {{
    "criterion": "Emerging Risk Driver Identification and Alignment",
    "explanation": "Explicitly identifies underlying drivers behind each mentioned risk and shows how recommendations mitigate those drivers.",
    "weight": 0.13
  }},
  {{
    "criterion": "Overall Analytical Depth Across Critical Sections",
    "explanation": "Evaluates the depth, layering of reasoning, and evidence density across sections most material to risk judgment (e.g., PCO Survey Sections, Loss Potential).",
    "weight": 0.10
  }}
]
</json_output>
</output>
</example>

Please strictly follow the above instructions and methods. Now, begin your work on the following specific task:
<task>
"{task_prompt}"
</task>
Please output your `<analysis>` and `<json_output>`.
</user_prompt>
"""


# Instruction-Following / Relevance
generate_eval_criteria_prompt_Inst = """
<system_role>
You are an experienced research article evaluation expert. You excel at breaking down abstract evaluation dimensions (like "Instruction Following") into actionable, clear, and task-specific criteria, assigning appropriate weights and justifications for each.
</system_role>

<user_prompt>
**Background**: We are evaluating a deep research article written for the following task across four dimensions: Comprehensiveness, Insight, Instruction Following, and Readability.
1.  **Comprehensiveness:** The breadth, depth, and relevance of information coverage.
2.  **Insight:** The depth, originality, logic, and value of the analysis and conclusions.
3.  **Instruction Following:** Whether the report accurately and completely responds to all requirements and constraints of the task.
4.  **Readability:** Clarity of structure, fluency of language, effectiveness of data presentation, and overall ease of understanding.

<task>
"{task_prompt}"
</task>

""" + _SCHEMA_AND_CONSTRAINTS_BLOCK + """

<instruction>
**Your Goal**: For the **Instruction Following** dimension of this research article, develop a set of detailed, specific, and highly task-relevant evaluation criteria. You need to:
1.  **Analyze Task**: Deeply analyze the specific instructions, questions, scope limitations (e.g., geography, time, subject), and core objectives within the `<task>`.
2.  **Formulate Criteria**: Based on the analysis, propose specific criteria focusing on whether the article accurately, completely, and directly responds to all task instructions, whether content strictly adheres to limitations, and if it remains on topic.
3.  **Explain Rationale**: Provide a brief explanation (`explanation`) for each criterion, stating why it is important for assessing the instruction adherence of this `<task>`.
4.  **Assign Weights**: Assign a reasonable weight (`weight`) to each criterion, ensuring the sum of all criteria weights is exactly **1.0**. Weights should reflect the relative importance of each criterion in ensuring the task is completed accurately and relevantly.
5.  **Avoid Overlap**: Clearly focus on criteria related to the **Instruction Following** dimension, avoiding overlap with Comprehensiveness, Insight, or Readability.

**Core Requirements**:
1.  **Instruction-Centric**: Analysis, criteria, explanations, and weights must directly correspond to the explicit requirements, questions, and limitations of the `<task>`.
2.  **Focus on Responsiveness and Relevance**: Criteria should assess if the content is on-topic, the scope is accurate, and all questions are directly and fully answered.
3.  **Well-Justified**: The `<analysis>` section must clearly articulate the overall thinking behind setting these criteria and weights, linking it to the `<task>`, the `<report_schema_outline>`, and the **mandatory elements**.
4.  **Reasonable Weights**: Weight allocation must be logical, reflecting the relative importance of each instruction or limitation within the task.
5.  **Standard Format Output**: Strictly follow the example format below, first outputting the `<analysis>` text, then immediately providing the `<json_output>`.
</instruction>

<example_rational>
The following example demonstrates **how to formulate instruction following criteria based on task requirements**. Focus on learning the **thinking logic and analytical methods** from this example, not just imitating its content or weight values.
</example_rational>

<example>
<task>
"Assess PCO exposures and controls for a mid-sized contract manufacturer and provide 1–4 ratings, loss potential, and a time-phased service plan to support underwriting."
</task>

<output>
<analysis>
Evaluating instruction-following centers on whether the report precisely addresses all schema-mandated components and constraints. The task has core components: 1) analyze PCO exposures and controls; 2) provide 1–4 ratings with rationales; 3) present Loss Potential (frequency/severity/scenario); and 4) deliver a time-phased Service Planning section and Recommendation Summary. Constraints include exact headings/order, required subsections, and provenance formatting.

Therefore, evaluation criteria must focus on:
1.  **Response to PCO Exposure/Control Analysis**: Does the report directly and clearly analyze exposures and control effectiveness across required categories?
2.  **Response to Ratings and Service Plan**: Does the report provide 1–4 ratings with rationales and a time-phased plan (Immediate/90d/6–12m) aligned to drivers?
3.  **Adherence to Schema Scope**: Is content strictly aligned to required sections and subsections (including Recommendation Summary and Disclaimer)?
4.  **Provenance Compliance**: Are Tickr tokens and web URLs formatted inline per rules?
5.  **Completeness of Task Components**: Are all schema components populated without omissions?

Weight allocation should prioritize direct responses to the analysis and ratings/service plan components, followed by strict schema and provenance adherence, since these determine evaluability for underwriting.
</analysis>
<json_output>
[
  {{
    "criterion": "Exact Schema Headings and Order",
    "explanation": "All required '##'/'###' headings present with exact casing and sequence.",
    "weight": 0.20
  }},
  {{
    "criterion": "Mandatory Subsections Present",
    "explanation": "Includes 'Recommendation Summary' (Critical/Important/Advisory) and 'Disclaimer' text verbatim.",
    "weight": 0.15
  }},
  {{
    "criterion": "Ratings Presence and Validity",
    "explanation": "All PCO categories have a single 1–4 rating and rationale.",
    "weight": 0.17
  }},
  {{
    "criterion": "Provenance Formatting Compliance",
    "explanation": "Citations use [Data source (date)] or bracketed URL [https://…]; parentheses are non-conforming; no raw Tickr tokens in-text.",
    "weight": 0.20
  }},
  {{
    "criterion": "Sufficient Insights Criteria Satisfied",
    "explanation": "Meets breadth and distribution requirements for the active mode (Tickr+Web/Web-only/Tickr-only).",
    "weight": 0.10
  }},
  {{
    "criterion": "Key Contacts Policy Compliance",
    "explanation": "Follows strict policy for confirming or marking 'Unknown' with required evidence.",
    "weight": 0.08
  }},
  {{
    "criterion": "Emerging Risk Driver Alignment",
    "explanation": "Each mentioned risk explicitly states the underlying drivers/causal factors and shows that recommendations target those drivers.",
    "weight": 0.10
  }}
]
</json_output>
</output>
</example>

Please strictly follow the above instructions and methods. Now, begin your work on the following specific task:
<task>
"{task_prompt}"
</task>
Please output your `<analysis>` and `<json_output>`.
</user_prompt>
"""


# Readability - Generates general criteria and typical weights
generate_eval_criteria_prompt_readability = """
<system_role>
You are an experienced research article evaluation expert. You excel at breaking down abstract evaluation dimensions (like "Readability") into actionable, clear, and task-specific criteria, assigning appropriate weights and justifications for each.
</system_role>

<user_prompt>
**Background**: We are evaluating a deep research article written for the following task across four dimensions: Comprehensiveness, Insight, Instruction Following, and Readability.
1.  **Comprehensiveness:** The breadth, depth, and relevance of information coverage.
2.  **Insight:** The depth, originality, logic, and value of the analysis and conclusions.
3.  **Instruction Following:** Whether the report accurately and completely responds to all requirements and constraints of the task.
4.  **Readability:** Clarity of structure, fluency of language, effectiveness of data presentation, and overall ease of understanding.

<task>
"{task_prompt}"
</task>

""" + _SCHEMA_AND_CONSTRAINTS_BLOCK + """

<instruction>
**Your Goal**: For the **Readability** dimension of this research article, develop a set of detailed, specific, and relatively general evaluation criteria, while also considering the characteristics of the `<task>`. You need to:
1.  **Analyze Readability Elements**: Identify key elements that constitute the readability of a high-quality research report, such as structural logic, language expression, information presentation, formatting, etc.
2.  **Formulate Criteria**: Based on the analysis, propose specific criteria covering:
    *   Language clarity and correctness (sentences, terminology, wording, errors)
    *   Content structure and logic (headings, paragraphs, introduction/conclusion, transitions)
    *   Information presentation and density (key points, breakdown, organization, redundancy)
    *   Data and citation presentation (data accuracy/clarity, inline provenance placement)
    *   Formatting and layout (paragraphs, spacing, highlighting)
    *   Audience adaptation (term explanation, expression style)
3.  **Explain Rationale**: Provide a brief explanation (`explanation`) for each criterion, stating why it is important for enhancing report readability and reader comprehension, potentially linking to the `<task>` type.
4.  **Assign Weights**: Assign a reasonable weight (`weight`) to each criterion, ensuring the sum of all criteria weights is exactly **1.0**. Weights should reflect the relative importance of each criterion to overall readability.
5.  **Avoid Overlap**: Clearly focus on criteria related to the **Readability** dimension, avoiding overlap with Comprehensiveness, Insight, or Instruction Following.

**Core Requirements**:
1.  **Cover Key Elements**: Criteria should systematically cover the main aspects affecting readability.
2.  **Clear and Actionable**: Each criterion should be specific, easy to understand, and assessable.
3.  **Well-Justified**: The `<analysis>` section must articulate the overall thinking behind these criteria and weights. The `explanation` for each criterion must justify its importance.
4.  **Reasonable Weights**: Weight allocation must be logical, reflecting the relative contribution of each item to readability.
5.  **Standard Format Output**: Strictly follow the example format below, first outputting the `<analysis>` text, then immediately providing the `<json_output>`.
</instruction>

<example_rational>
The following example demonstrates **how to formulate readability criteria**. Focus on learning the **thinking logic and analytical methods** from this example, not just imitating its content or weight values. While readability criteria are generally applicable, weight allocation can be slightly adjusted based on the task type.
</example_rational>

<example>
<task>
"Assess the impact of supplier quality variability and evolving regulatory expectations on PCO risk for a medical device assembler and recommend risk control actions to support underwriting."
</task>

<output>
<analysis>
Evaluating the readability of a risk control report requires ensuring that complex exposure analyses, control evaluations, and scenarios are easy to follow. For underwriting support, a clear structure mirroring the schema, precise professional language, and intuitive presentation of data and citations are particularly crucial.

Evaluation criteria should cover:
1.  **Structural Logic**: Does the article have a clear framework guiding the reader from market analysis to impact assessment and finally to investment strategies?
2.  **Language and Terminology**: Is the language fluent and accurate? Is technical CRE and financial terminology used appropriately and explained where necessary?
3.  **Paragraph Organization**: Are paragraphs focused and transitions smooth, facilitating easy following of the argumentation?
4.  **Information Presentation**: Is key information highlighted? Is data presented clearly, with inline citations placed to preserve reading flow?
5.  **Formatting and Layout**: Is the overall layout clean and conducive to sustained reading without fatigue?

Weight allocation should give the highest importance to structural clarity, as it's fundamental to understanding complex analyses. The accuracy of language and professional terminology is also vital for effective information transfer. For a data-intensive task like this, the presentation of data and citations significantly contributes to readability. Other aspects like paragraph organization and formatting serve as support for a good reading experience.
</analysis>
<json_output>
[
  {{
    "criterion": "Structure Mirrors Schema and Guides Flow",
    "explanation": "Headings and transitions help navigate Operations → Regulatory → Loss → Recommendations; mirrors exact schema.",
    "weight": 0.25
  }},
  {{
    "criterion": "Clarity and Precision of Language",
    "explanation": "Professional, concise wording; correct sector terminology; avoids ambiguity.",
    "weight": 0.20
  }},
  {{
    "criterion": "Concise, Scannable Rating Rationales",
    "explanation": "Each rating followed by brief, evidence-backed bullets (why/so-what).",
    "weight": 0.20
  }},
  {{
    "criterion": "Data and Citation Legibility",
    "explanation": "[Data source (date)], [https://…] are placed to preserve reading flow; parentheses are non-conforming; data points easy to parse.",
    "weight": 0.15
  }},
  {{
    "criterion": "Effective Summaries and Lists",
    "explanation": "'Recommendation Summary' uses clear bullets; 'Service Planning' is time-phased (Immediate/90d/6–12m).",
    "weight": 0.10
  }},
  {{
    "criterion": "Terminology Consistency",
    "explanation": "Consistent casing and canonical terms across sections to reduce cognitive load.",
    "weight": 0.10
  }}
]
</json_output>
</output>
</example>

Please strictly follow the above instructions and methods. Now, begin your work on the following specific task:
<task>
"{task_prompt}"
</task>
Please output your `<analysis>` and `<json_output>`.
</user_prompt>
"""


