REPEATED_PROMPT = """
The content of this section should logically follow on from the content of the previous section, and the content of the entire case.
Write in a neutral and factual tone, without explicitly naming the project.
Use the passive voice where possible; do not use first-person pronouns.
All claims and data should be referenced with links in <a> tags.
Use British (UK) English for spelling and grammar.
Do not use 'flowery language' - don't introduce references (e.g. 'according to X...'), just state the point and make sure it is referenced.
Within section content, always use '\\n' for line breaks between HTML elements.
All double quotes must be escaped with a backslash - they should appear as \\\"\n
"""

OPTIONS_FRAMEWORK_PROMPT = """
Before the table, there should be a small section explaining each of the options considered. Begin this with a sentence like 'The <type> options considered were:' Then list a brief description of each option.
The first column should be titled 'Critical Success Factors' and should contain the five CSF categories, one for each row:
    - Strategic fit and meets business needs
    - Potential value for money
    - Supplier capability and capacity
    - Potential affordability
    - Potential achievability
Each subsequent column should be reserved for each option. They should be given a header containing each option description. Number the options numerically.
Columns should be ordered from least ambitious on the left to most ambitious on the right. Don't specifically refer to this in the column headings.
Each option should be rated against the critical success factors in each row using the Red Amber Green (RAG) rating system.
There should be a very brief sentence in each cell explaining how the option applies to the CSF. Use coloured dots (🔴🟡🟢) at the beginning of each cell.
All assessments should be qualitative - **do not perform quantitative analysis at this stage.**
The last row should be a conclusion row, accounting for all CSF applicability for that specific option.
Out of all the option conclusions, **there MUST only be ONE preferred option (green dot 🟢).**
**If there is at least one red dot for that option, the conclusion dot MUST be red 🔴 and the option must be discounted**.
Otherwise, if it is a combination of amber and green, the conclusion should be decided accordingly, with green conclusions being more preferable.
These options should consider all previous sections as context (particularly business needs and market failure sections) in suggesting first cut of options and RAG ratings.
After the table, include a brief discussion and summary of options considered. This should be around 50 words long.
"""

BLANK_PROMPT = """
Leave this section blank - it is generated at a later step.
"""

SECTION_PROMPTS = {
    # STRATEGIC CASE
    # 1.1 Strategic Context
    "1-1": f"""
    Write an introduction of around 250 words (±50) that sets the scene by describing national and local trends relevant to the project's sector and location, with only brief reference to global context where essential.
    The trends may include themes such as population and demographics, economy and public services, digitalisation, consumer behaviour, political priorities, legislative changes, development pressures, and so forth, but feel free to include other themes if relevant and available.
    Include 3-5 headline statistics, with at least one at national and one at the location of the project, and present the content in a neutral and factual tone.
    Integrate these themes into a cohesive narrative, explicitly linking the proposed project to its intended impacts.
    Focus only on wider trends and circumstantial information, without mentioning the specific project explicitly.
    All claims and data should be referenced with links in <a> tags.
    {REPEATED_PROMPT}
    """,
    # 1.2 Organisational Overview
    "1-2": f"""
    Write an overview of around 300 words (±100) of the organisation delivering the proposed project.
    Describe its legal form, governance arrangements, mission, and strategic objectives.
    Summarise its track record in delivering comparable initiatives and its reputation in the community or sector.
    Highlight available resources, skills, facilities, and partnerships that strengthen its capacity.
    In addition, briefly note any other relevant organisations responsible for oversight, management, or regulation in this area.
    This section should be written strictly in prose and not bullet points.
    {REPEATED_PROMPT}
    """,
    # 1.3 Strategic Drivers
    "1-3": f"""
    Write a 300–400 word section on the strategic drivers relevant to the proposed project. 
    Begin with a short introductory paragraph summarising recent changes in national, regional, and local policy that affect this area, highlighting their significance in shaping the case for intervention.
    After the introduction, present a table with four columns: (1) Level (National, Regional, or Local), (2) Strategic Driver (e.g. Policy, Strategy), (3) Objective, and (4) Basis of grading, specific focus of alignment and contribution.
    The columns should be titled: (1) Level, (2) Strategic Driver, (3) Objective, (4) Description
    In the table, list at least 5–7 policies spanning national, regional, and local levels, each with a clear objective and explanation of how it is relevant.
    Table rows should be ordered so that all National level drivers appear first, then all Regional level drivers, than Local level drivers last.
    This section should conclude with a description of any overarching programme or related projects to the project being developed (if available), so it is clear where the new project fits in the landscape of related investment.
    When wording this section, do not assume that the project exists - for example, use "An investment could..." instead of "The project will...".
    All links to references should be included.
    {REPEATED_PROMPT}
    """,
    # 1.4 Spending Objectives
    "1-4": f"""
    Write approximately 150–250 words outlining between three and six SMART (Specific, Measurable, Achievable, Relevant, Time-bound) objectives that justify public or external investment in the proposed project.
    Ensure each objective maps to a different dimension—such as cultural, physical, financial, economic, environmental, or social.
    Present the outputs in a numbered table with two columns: (1) Objective and (2) SMART Measures.
    Under each objective, provide between one and three SMART measures, listed as bullet points.
    SMART objectives should consider the following reasons for public investment: economy (cost reduction), efficiency (doing more for less), effectiveness (quality), statutory compliance and re-procurement.
    In practice you should aim to include an objective for the first three and only for the last two if they are relevant.
    {REPEATED_PROMPT}
    """,
    # 1.5 Existing Arrangements
    "1-5": f"""
    Write an overview of around 400 words (±200) describing the current situation regarding the proposed project investment.
    Begin with the wider context, outlining how service provision is currently structured at local authority and town level (e.g. what facilities or venues exist, who operates them, and what services they provide).
    Then focus on the specific facilities at the project location, describing ownership, governance, management arrangements, physical condition, and role within the town.
    Highlight how any facilities are currently used to provide services, how they compare to other provision, and what limitations or gaps exist in both organisational and physical terms.
    Ensure the response integrates both the broader community/cultural landscape and the individual facility context.
    All claims and data should be referenced with links in <a> tags.
    {REPEATED_PROMPT}
    """,
    # 1.6 Business Needs
    "1-6": f"""
    Write an overview of around 400 words (±100) describing the business needs that underpin the proposed project.
    Begin with broader evidence of community demand for cultural and civic space at the town and district level, before narrowing to specific evidence from local groups, facilities, or consultations.
    Emphasise that the primary driver of the need is bottom-up community demand and user preferences, not just top-down government priorities.
    Show this through evidence such as demographic pressures, consultation findings, levels of bookings at comparable venues, or the number and type of community groups seeking the intended project’s impacts.
    Identify barriers created by limited, outdated, or unsuitable facilities, and explain the consequences of not addressing these needs.
    Include any foreseen future issues.
    Ensure the response demonstrates how these needs align with, but are distinct from, broader policy goals.
    Present in a neutral and factual tone, avoiding abstract statements or unsupported generalisations.
    Any online-sourced evidence and data used must be correctly referenced referenced with links in <a> tags.
    Present the analysis in two sections: 'problems with the existing arrangements' and 'opportunities'.
    Use a mixture of narrative and bullet points for clarity.
    {REPEATED_PROMPT}
    """,
    # 1.7 Case for Change Summary
    "1-7": f"""
    Produce a Case for Change table that summarises the challenges, objectives, and business needs relevant to the proposed project.
    Structure the table into three columns: (1) Existing challenges and opportunities, (2) Objectives, and (3) Business need (Gap).
    Present rows thematically but without a separate thematic area column, and do not insert headings within the cells.
    The objectives must match the spending objectives presented in section 1.3. Do not add or remove any objectives from this section.
    Write concisely and factually in each cell, focusing on practical needs and evidence.
    Do not contrast a 'do nothing' vs 'do minimum' scenario; instead, present the key challenges, what should be achieved, and what the gap is that must be addressed.
    For each row, the existing arrangements must align with the objective and corresponding business needs.
    {REPEATED_PROMPT}
    """,
    # 1.8 Potential Benefits
    "1-8": f"""
    Write an overview of around 150 words (±50) setting out the potential benefits of the proposed project.
    After the introductory text, present a concise table with three columns: (1) Benefit number, (2) brief description of the benefit, and to whom this benefit accrues – the beneficiaries, (3) is the benefit cash releasing, non-cash releasing or wider social, economic or environmental benefit.
    The three columns should be titled (1) (leave title blank), (2) Benefit, (3) Type of Benefit
    Structure the content to follow the same order as the objectives previously identified, but do not explicitly label or categorise the dimensions. 
    In each case, state clearly who the beneficiaries would be (e.g. residents, community groups, audiences, visitors, or the local economy).
    Where possible, provide quantitative estimates of potential benefits, such as projected attendance, financial sustainability measures, visitor numbers, or environmental performance.
    {REPEATED_PROMPT}
    """,
    # 1.9 Potential Risks
    "1-9": f"""
    Write an overview of no more than 150 words introducing the potential risks associated with the proposed project.
    After the introductory text, present a concise table with four columns: (1) Risk number, (2) Potential risk, (3) Mitigation method, and (4) Level of impact (High/Medium/Low). 
    Order the risks in the table by level of impact, with High-impact risks listed first, followed by Medium, and then Low.
    Cover risks across strategic, financial, operational, market/demand, and environmental/regulatory areas.
    Keep the section concise so that its overall length does not exceed that of the Potential Benefits section.
    {REPEATED_PROMPT}
    """,
    # 1.10 Constraints
    "1-10": f"""
    Write an overview of around 150 words (±50) summarising the likely constraints that could limit the scope or shape of the proposed project.
    Cover legal, regulatory, financial, environmental, planning, and practical constraints.
    {REPEATED_PROMPT}
    """,
    # 1.11 Dependencies
    "1-11": f"""
    Write an overview of around 150 words (±50) summarising the dependencies that could affect this proposed project.
    Describe reliance on other factors, including for example funding streams, infrastructure availability, planning or regulatory approvals, local partnerships, policy frameworks, community engagement, and other relevant areas.
    Highlight both risks and opportunities that arise from these dependencies.
    {REPEATED_PROMPT}
    """,

    # ECONOMIC CASE PART 1
    # 2.1 Purpose of Economic Case
    "2-1": f"""
    This section should consist of one short paragraph describing the overall structure and approach of the economic case. It should cover the objectives and coverage of the case.
    Use the following passage as a boilerplate from which to base this section:
    'The purpose of the Economic Case is to identify the preferred project option – i.e. the option that provides the 'optimal' balance of cost, risk and benefits to deliver the objectives set out in the Strategic Case. Identifying this option includes two main steps:
    - Use the HMT Green Book options assessment framework to generate and appraise a long list of options, using the categories of choice in sequence, to develop a shortlist
    - Further assess the shortlist to identify the preferred option, taking into account value for money (VfM), risk, qualitative factors, place-based considerations, and wider sustainability impacts, applied proportionately'
    {REPEATED_PROMPT}
    """,
    # 2.2 Market Failure
    "2-2": f"""
    This section must only consist of a table, and optionally one short sentence introducing the table (e.g. 'The market failures are presented in the table below').
    The table should use the four categories of market failure recognised in HM Treasury's Green Book: (1) Public goods, (2) Imperfect information, (3) Externalities, and (4) Market power.
    Only include rows for those failures that are actually relevant to the proposed project; if one does not apply, leave it out.
    Within each relevant row, explain briefly how that type of failure applies to the project, with references where possible.
    Where appropriate, refer also to the related concepts of factor immobility and missing markets, but integrate these into the explanation rather than presenting them as separate rows.
    Keep the explanations concise, factual, and aligned with Green Book definitions.
    {REPEATED_PROMPT}
    """,
    # 2.3 Longlist to Shortlist using the Options Framework
    "2-3": f"""
    This section should consist of one short paragraph that comprises a brief introduction to the options framework.
    This is a six-part section consisting of:
    - Critical success factors
    - Scope options (the 'what')
    - Solution options (the 'how')
    - Delivery options (the 'who')
    - Implementation (the 'when')
    - Funding options (the 'who pays')
    Do not explain why this is a good thing to do, etc., only outline the process.
    Critical success factors will be defined in the next section, and the following five sections will be worked through for each.
    This section should be written strictly in prose and not bullet points.
    {REPEATED_PROMPT}
    """,
    # 2.3.1 Critical Success Factors
    "2-3-1": f"""
    This section must only consist of a table, and optionally one sentence introducing the table. For example, 'The critical success factors are presented in the table below:'.
    The table should consist of two columns: (1) Critical Success Factor, (2) How well does the option... (3) Description
    These factors should be derived from strategic objectives, legal statutes, or absolute technical necessities. List each CSF clearly (e.g., 'Full operation by Q1 2027', 'Compliance with the Environment Act 2021', 'Integration with existing Core IT System X').
    Do not begin the success factors with 'must', they should be worded as variable statements like the examples given above.
    There should be five critical success factors that correspond to the following categories. Each row should start with, in the first column:
    - "Strategic fit and meets business needs" (Does the option fulfil the [strategic drivers section 1.3 of strategic case and meet the spending objectives and business needs in the 1.7 summary case for change]?)
    - "Potential value for money" (How likely is the option to deliver benefits such as [expected benefits section of strategic case] at a proportionate cost, while managing delivery and operational risks?)
    - "Supplier capability and capacity" (Does the market and its suppliers in the [MARKET from 2.2 market failure section] have the capacity and capability to deliver the option?)
    - "Potential affordability" (Is the option feasible given the available [capital budget input at landing page], and in terms of covering operational costs given reasonable assumptions regarding expected revenue and funding when in operation?)
    - "Potential achievability" (Is the option likely to be delivered successfully, considering the skills of the project proponent and organisation responsible for delivery [see project information page], governance, risks, and timescales [of proposition]?)
    In the second column, the values should be, from top to bottom:
    -------------------------------
    - meet agreed spending objectives, related business needs and service requirements?
    - provide holistic fit and synergy with other strategies, programmes and projects?
    -------------------------------
    - optimise social value (social, economic and environmental), in terms of the potential costs, benefits and risks?
    -------------------------------
    - match the ability of potential suppliers to deliver the required services?
    -------------------------------
    - fit within available funding?
    - align with sourcing constraints?
    -------------------------------
    - match the level of available skills required for successful delivery
    - appear likely to be delivered given an organisation's ability to respond to the changes required
    -------------------------------
    In this second column, all list items should begin with hyphens, and there should be a line break between each item.
    
    These critical success factors should have their meaning explained in relation to the project.
    {REPEATED_PROMPT}
    """,
    # 2.3.2 Scope Options
    "2-3-2": f"""
    This section should consist of a table with scope options.
    Define the 'what' by outlining different extents or boundaries for the project. Present distinct choices for what the project will and will not cover. Examples include: 'Whole service end-to-end', 'Phased rollout by geography', 'Minimum viable product (MVP) vs. full enhancement', or 'Target user group A only vs. all user groups'. Describe the service model, estimated costs, delivery approach, and key limitations for each scope option.
    {OPTIONS_FRAMEWORK_PROMPT}
    This is part 1 of 5 sections. Each category of choice (scope, solution, delivery implementation and funding) builds on the previous category of choice and the preferred and carry forward options selected.
    {REPEATED_PROMPT}
    """,
    # 2.3.3 Solution Options
    "2-3-3": f"""
    This section should consist of a table with solution options.
    Define the 'how' by presenting different methods or models to meet the project's objectives and address the limitations of the status quo. These options should relate to the practical, physical solutions.
    {OPTIONS_FRAMEWORK_PROMPT}
    This is part 2 of 5 sections. Each category of choice (scope, solution, delivery implementation and funding) builds on the previous category of choice and the preferred and carry forward options selected.
    {REPEATED_PROMPT}
    """,
    # 2.3.4 Delivery Options
    "2-3-4": f"""
    This section should consist of a table with delivery options.
    Define the 'who' and 'how' by evaluating different models for procuring and delivering the chosen solution. Present and analyze options such as in-house delivery, outsourcing, strategic partnership, joint venture, or using a central government framework. These options should relate to who is going to implement the solution.
    {OPTIONS_FRAMEWORK_PROMPT}
    This is part 3 of 5 sections. Each category of choice (scope, solution, delivery implementation and funding) builds on the previous category of choice and the preferred and carry forward options selected.
    {REPEATED_PROMPT}
    """,
    # 2.3.5 Implementation Options
    "2-3-5": f"""
    This section should consist of a table with implementation options
    Define the 'when' and 'how' by outlining high-level strategic approaches for rolling out the project. Present different phasing and sequencing strategies, such as 'Big Bang' launch, 'Phased Geographical Rollout', or 'Pilot followed by scaled deployment'. For each option, briefly describe the key stages, timeline, and major dependencies. This should be directly linked to achieving the project's spending objectives.
    {OPTIONS_FRAMEWORK_PROMPT}
    This is part 4 of 5 sections. Each category of choice (scope, solution, delivery implementation and funding) builds on the previous category of choice and the preferred and carry forward options selected.
    {REPEATED_PROMPT}
    """,
    # 2.3.6 Funding Options
    "2-3-6": f"""
    This section should consist of a table with funding options.
    Define the financial mechanisms for resourcing the project. Present and analyze different potential sources of funding, such as 'Treasury Grant', 'Departmental Budget', 'Public-Private Financing (PF2)', 'User Charges', or 'Capital Markets Raising'. For each option, summarize the key implications for affordability, value for money, risk transfer, and budgetary treatment.
    {OPTIONS_FRAMEWORK_PROMPT}
    This is part 5 of 5 sections. Each category of choice (scope, solution, delivery implementation and funding) builds on the previous category of choice and the preferred and carry forward options selected.
    {REPEATED_PROMPT}
    """,
    # 2.4 Options Framework Summary
    "2-4": f"""
    Provide a consolidated summary of the Options Framework. Present a matrix or table showing how each option from the longlist (across scope, solution, delivery, implementation, and funding) performed against the Critical Success Factors and initial high-level scoring.
    The table should consist of five rows and a header row. The first column in the table should represent the five areas considered in the options framework:
        - Scope options
        - Solution options
        - Delivery options
        - Implementation
        - Funding options
    The options considered for each area should then be presented in columns to the right, with a number of columns in each row equal to the number of options.
    If the number of options is different for each row, fill the extra cells with empty space.
    Options should be listed in numerical order from left to right.
    Be sure to include the same coloured dot as provided in the conclusion for each option considered.
    Less ambitious options should be placed to the left, and more ambitious options should be placed to the right.
    Introduce the table with a brief introduction. Do not include any kind of analysis or conclusion beneath the table.
    {REPEATED_PROMPT}
    """,
    # 2.5 Shortlist of Options
    "2-5": f"""
    This section should contain a table identifying the short list for further assessment.
    The table should contain one column for each option considered.
    The following rows should contain all five types of options considered:
        - Scope option
        - Solution option
        - Delivery option
        - Implementation option
        - Funding option
    The corresponding cells should contain the options considered from each of the five types of option considered in previous sections.
    The last two rows should have headings on the left 'Description' and 'Rationale'.
    The first column should have the heading 'Option 1 - Counterfactual' and contain the text 'No investment' for each of the five option rows.
    The second column should have the heading 'Option 2 - Less ambitious' and contain the 'Less ambitious' option.
    The third column should have the heading 'Option 3- Preferred' and contain the 'preferred' option - all five preferred (green) options from the options framework.
    The fourth column should have the heading 'Option 4 - More ambitious' and contain the 'More ambitious' option.
    Outside of the Counterfactual option, the five options that contribute to that way forward should be listed.
    The Counterfactual option should refer back to content from section 1.5 (1-5) in the strategic case.
    Clearly state which options have been eliminated and which have progressed to the shortlist, providing the rationale for each decision.
    A shortlist should be suggested based on the available options. Green choices per category of choice form the preferred option; these are combined with yellow carry forward options which are more or less ambitious to construct a more ambitious and a less ambitious option to take forward to part 2 of the analysis
    Present the final, viable shortlist of options that will undergo detailed appraisal. Each shortlisted option should be a coherent combination of choices from the framework (e.g., 'Option 3: MVP Scope - Outsourced Solution - Phased Implementation - Departmental Funding'). Provide a succinct description for each shortlisted option, explaining why it is considered a strong contender before the full economic analysis is conducted.
    The analysis beneath the table should consist of 250-500 words, as required. It should begin with a brief sentence and bullet point list introducing the preferred way forward - all five green dotted conclusions from the previous option tables.
    {REPEATED_PROMPT}
    """
}
