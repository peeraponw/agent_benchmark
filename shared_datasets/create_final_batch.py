#!/usr/bin/env python3
"""
Create final batch of documents to reach 40+ total.
"""

import json
from pathlib import Path

docs_dir = Path("rag_documents/documents")

# Final batch of documents
final_docs = [
    # Technology
    ("tech_13_ai_ethics.txt", """Artificial Intelligence Ethics and Responsible AI

INTRODUCTION TO AI ETHICS

AI ethics is the branch of ethics that examines the moral implications of artificial intelligence systems, addressing questions about fairness, accountability, transparency, and human values in AI development and deployment.

CORE ETHICAL PRINCIPLES

Fairness and Non-Discrimination:
- Avoiding bias in AI systems
- Ensuring equal treatment across groups
- Addressing historical inequalities
- Promoting inclusive design

Transparency and Explainability:
- Making AI decisions interpretable
- Providing clear explanations for outcomes
- Enabling algorithmic auditing
- Building trust through openness

Accountability and Responsibility:
- Establishing clear lines of responsibility
- Ensuring human oversight of AI systems
- Creating mechanisms for redress
- Defining liability for AI decisions

Privacy and Data Protection:
- Protecting personal information
- Implementing data minimization
- Ensuring consent and control
- Securing data against breaches

Human Autonomy and Agency:
- Preserving human decision-making
- Avoiding manipulation and coercion
- Respecting human dignity
- Maintaining meaningful human control

ETHICAL CHALLENGES IN AI

Algorithmic Bias:
- Training data bias
- Historical discrimination perpetuation
- Representation gaps
- Feedback loops amplifying bias

Job Displacement:
- Automation impact on employment
- Economic inequality concerns
- Reskilling and retraining needs
- Social safety net considerations

Surveillance and Privacy:
- Facial recognition technology
- Behavioral tracking and profiling
- Government surveillance capabilities
- Corporate data collection practices

Autonomous Weapons:
- Lethal autonomous weapon systems
- Military AI applications
- International humanitarian law
- Human control requirements

Deepfakes and Misinformation:
- Synthetic media creation
- Truth and authenticity concerns
- Political manipulation potential
- Detection and verification challenges

RESPONSIBLE AI DEVELOPMENT

Ethics by Design:
- Incorporating ethical considerations from the start
- Multidisciplinary team involvement
- Stakeholder engagement
- Iterative ethical assessment

Risk Assessment and Management:
- Identifying potential harms
- Evaluating likelihood and impact
- Implementing mitigation strategies
- Continuous monitoring and adjustment

Testing and Validation:
- Bias testing across different groups
- Robustness and reliability testing
- Edge case evaluation
- Real-world performance monitoring

Documentation and Governance:
- Model cards and data sheets
- Ethical review processes
- Governance frameworks
- Audit trails and accountability

REGULATORY LANDSCAPE

International Initiatives:
- EU AI Act: Comprehensive AI regulation
- UNESCO AI Ethics Recommendation
- OECD AI Principles
- Partnership on AI initiatives

National Strategies:
- US National AI Initiative
- China AI governance framework
- UK AI ethics guidelines
- Canada Directive on Automated Decision-Making

Industry Self-Regulation:
- Corporate AI ethics boards
- Industry standards and best practices
- Professional codes of conduct
- Voluntary commitments and pledges

IMPLEMENTATION STRATEGIES

Organizational Approaches:
- AI ethics committees
- Chief AI Officer roles
- Ethics training programs
- Cross-functional collaboration

Technical Solutions:
- Bias detection and mitigation tools
- Explainable AI techniques
- Privacy-preserving technologies
- Robustness and safety measures

Stakeholder Engagement:
- Community involvement
- User feedback mechanisms
- Expert consultation
- Public participation

FUTURE CONSIDERATIONS

Emerging Technologies:
- Artificial General Intelligence (AGI)
- Brain-computer interfaces
- Quantum AI systems
- Synthetic biology integration

Global Coordination:
- International standards development
- Cross-border enforcement mechanisms
- Technology transfer considerations
- Capacity building initiatives

Societal Adaptation:
- Education and digital literacy
- Social contract renegotiation
- Democratic participation in AI governance
- Cultural and value considerations"""),

    ("tech_14_quantum_computing_applications.json", {
        "title": "Quantum Computing Applications and Impact",
        "overview": "Practical applications and potential impact of quantum computing across industries",
        "current_applications": {
            "optimization": {
                "description": "Solving complex optimization problems",
                "examples": [
                    "Portfolio optimization in finance",
                    "Route optimization in logistics",
                    "Resource allocation in manufacturing",
                    "Network optimization in telecommunications"
                ],
                "quantum_advantage": "Exponential speedup for certain optimization problems"
            },
            "cryptography": {
                "description": "Breaking and creating cryptographic systems",
                "applications": [
                    "RSA encryption breaking with Shor's algorithm",
                    "Quantum key distribution for secure communication",
                    "Post-quantum cryptography development",
                    "Random number generation"
                ],
                "timeline": "Near-term threat to current encryption"
            },
            "simulation": {
                "description": "Simulating quantum systems and complex phenomena",
                "use_cases": [
                    "Drug discovery and molecular modeling",
                    "Materials science and catalyst design",
                    "Climate modeling and weather prediction",
                    "Financial risk modeling"
                ],
                "advantage": "Natural simulation of quantum phenomena"
            }
        },
        "industry_impact": {
            "finance": {
                "applications": [
                    "Risk analysis and portfolio optimization",
                    "Fraud detection and prevention",
                    "High-frequency trading algorithms",
                    "Credit scoring and loan approval"
                ],
                "timeline": "5-10 years for practical applications"
            },
            "healthcare": {
                "applications": [
                    "Drug discovery acceleration",
                    "Personalized medicine",
                    "Medical imaging enhancement",
                    "Genomic analysis"
                ],
                "potential_impact": "Reduced drug development time and cost"
            },
            "logistics": {
                "applications": [
                    "Supply chain optimization",
                    "Traffic flow management",
                    "Warehouse automation",
                    "Delivery route planning"
                ],
                "benefits": "Significant cost savings and efficiency gains"
            },
            "energy": {
                "applications": [
                    "Grid optimization and smart grids",
                    "Battery and energy storage design",
                    "Solar cell efficiency improvement",
                    "Nuclear fusion simulation"
                ],
                "impact": "Accelerated clean energy transition"
            }
        },
        "technical_requirements": {
            "hardware": {
                "qubit_count": "50-100 qubits for useful applications",
                "error_rates": "Below 0.1% for fault-tolerant computing",
                "coherence_time": "Milliseconds to seconds",
                "connectivity": "High qubit connectivity for complex algorithms"
            },
            "software": {
                "programming_languages": ["Qiskit", "Cirq", "Q#", "PennyLane"],
                "algorithms": ["Variational quantum algorithms", "Quantum machine learning", "Quantum optimization"],
                "simulation": "Classical simulation for algorithm development"
            }
        },
        "challenges": {
            "technical": [
                "Quantum error correction",
                "Scalability to large qubit counts",
                "Noise and decoherence",
                "Limited gate fidelity"
            ],
            "practical": [
                "High cost of quantum systems",
                "Need for specialized expertise",
                "Integration with classical systems",
                "Limited quantum software ecosystem"
            ],
            "economic": [
                "Uncertain return on investment",
                "Long development timelines",
                "Competition with classical improvements",
                "Market readiness questions"
            ]
        },
        "timeline_predictions": {
            "near_term_2024_2030": [
                "NISQ applications in optimization",
                "Quantum advantage demonstrations",
                "Hybrid quantum-classical algorithms",
                "Specialized quantum processors"
            ],
            "medium_term_2030_2040": [
                "Fault-tolerant quantum computers",
                "Practical cryptography applications",
                "Large-scale simulations",
                "Quantum internet development"
            ],
            "long_term_2040_plus": [
                "Universal quantum computers",
                "Quantum artificial intelligence",
                "Revolutionary scientific discoveries",
                "Widespread commercial adoption"
            ]
        }
    }),

    # Business
    ("business_08_innovation_management.md", """# Innovation Management and Strategy

## Introduction
Innovation management is the systematic approach to fostering, developing, and implementing new ideas, products, services, or processes within an organization to create value and competitive advantage.

## Types of Innovation

### Product Innovation
- New or improved products and services
- Feature enhancements and functionality
- Design and user experience improvements
- Technology integration

### Process Innovation
- Operational efficiency improvements
- Workflow optimization
- Automation and digitization
- Quality enhancement methods

### Business Model Innovation
- Revenue model changes
- Value proposition redefinition
- Customer relationship transformation
- Partnership and ecosystem development

### Organizational Innovation
- Structure and governance changes
- Culture and mindset shifts
- Talent management approaches
- Communication and collaboration methods

## Innovation Strategy Framework

### Innovation Vision and Goals
- Long-term innovation aspirations
- Strategic alignment with business objectives
- Innovation portfolio balance
- Success metrics and KPIs

### Innovation Scope and Focus
- Market and technology domains
- Innovation horizons (core, adjacent, transformational)
- Resource allocation priorities
- Risk tolerance levels

### Innovation Capabilities
- Research and development capabilities
- Technology and digital infrastructure
- Human capital and skills
- External partnerships and networks

## Innovation Process

### Idea Generation
- **Brainstorming**: Structured creative sessions
- **Crowdsourcing**: Internal and external idea collection
- **Design Thinking**: Human-centered problem solving
- **Open Innovation**: External collaboration and partnerships

### Idea Evaluation and Selection
- Feasibility assessment
- Market potential analysis
- Strategic fit evaluation
- Resource requirement estimation

### Development and Implementation
- Project management and execution
- Prototype development and testing
- Pilot programs and market validation
- Scaling and commercialization

### Monitoring and Learning
- Performance measurement and tracking
- Feedback collection and analysis
- Continuous improvement
- Knowledge capture and sharing

## Innovation Culture

### Leadership and Vision
- Executive commitment and sponsorship
- Innovation leadership development
- Clear communication of innovation priorities
- Resource allocation and investment

### Organizational Environment
- Psychological safety and risk tolerance
- Collaboration and knowledge sharing
- Diversity and inclusion
- Learning and experimentation mindset

### Incentives and Recognition
- Innovation-focused performance metrics
- Reward systems for creative contributions
- Career development opportunities
- Celebration of successes and failures

### Structure and Processes
- Dedicated innovation teams and roles
- Cross-functional collaboration mechanisms
- Flexible and agile processes
- Time and space for innovation activities

## Innovation Tools and Methods

### Design Thinking
- Empathize: Understand user needs
- Define: Frame the problem
- Ideate: Generate solutions
- Prototype: Build and test concepts
- Test: Validate with users

### Lean Startup Methodology
- Build-Measure-Learn cycle
- Minimum Viable Product (MVP) development
- Validated learning approach
- Pivot or persevere decisions

### Stage-Gate Process
- Structured innovation funnel
- Go/no-go decision points
- Risk reduction through stages
- Resource allocation optimization

### Innovation Tournaments
- Competitive idea generation
- Crowdsourcing and collaboration
- Evaluation and selection processes
- Winner recognition and implementation

## Open Innovation

### External Collaboration
- University partnerships
- Startup ecosystems and incubators
- Supplier and customer co-innovation
- Industry consortiums and alliances

### Technology Acquisition
- Licensing and technology transfer
- Mergers and acquisitions
- Joint ventures and partnerships
- Corporate venture capital

### Innovation Platforms
- Innovation challenges and competitions
- Online collaboration platforms
- Innovation labs and accelerators
- Ecosystem orchestration

## Digital Innovation

### Technology Enablers
- Artificial intelligence and machine learning
- Internet of Things (IoT) and sensors
- Cloud computing and edge computing
- Blockchain and distributed ledgers

### Digital Transformation
- Business model digitization
- Customer experience enhancement
- Operational efficiency improvements
- Data-driven decision making

### Emerging Technologies
- Virtual and augmented reality
- Robotics and automation
- Quantum computing
- Biotechnology and nanotechnology

## Innovation Metrics and Measurement

### Input Metrics
- R&D investment levels
- Innovation team size and composition
- Training and development spending
- External partnership investments

### Process Metrics
- Idea generation rates
- Time to market
- Project success rates
- Innovation pipeline health

### Output Metrics
- New product revenue percentage
- Patent applications and grants
- Market share gains
- Customer satisfaction improvements

### Impact Metrics
- Revenue growth from innovation
- Profit margin improvements
- Market capitalization increases
- Competitive advantage measures

## Innovation Challenges

### Resource Constraints
- Limited funding and budgets
- Competing priorities and trade-offs
- Talent shortages and skill gaps
- Technology and infrastructure limitations

### Organizational Barriers
- Risk-averse culture
- Bureaucratic processes
- Siloed structures
- Resistance to change

### Market Uncertainties
- Customer adoption challenges
- Competitive responses
- Regulatory and compliance issues
- Technology disruptions

### Execution Difficulties
- Project management complexities
- Scaling and commercialization challenges
- Quality and reliability issues
- Time-to-market pressures

## Best Practices

### Strategic Alignment
- Link innovation to business strategy
- Balance portfolio across innovation types
- Align resources with priorities
- Communicate innovation vision clearly

### Culture Development
- Foster psychological safety
- Encourage experimentation
- Celebrate learning from failures
- Promote cross-functional collaboration

### Process Excellence
- Implement structured innovation processes
- Use appropriate tools and methodologies
- Establish clear decision criteria
- Monitor and improve continuously

### External Engagement
- Build innovation ecosystems
- Leverage external partnerships
- Engage with customers and users
- Monitor technology and market trends

## Future Trends

### Sustainable Innovation
- Environmental and social impact focus
- Circular economy principles
- Clean technology development
- Responsible innovation practices

### Collaborative Innovation
- Ecosystem-based innovation
- Platform and network effects
- Co-creation with stakeholders
- Global innovation networks

### AI-Powered Innovation
- Artificial intelligence in R&D
- Automated idea generation
- Predictive innovation analytics
- Intelligent innovation platforms

## Conclusion
Innovation management is critical for organizational success in today's rapidly changing business environment. It requires a systematic approach that combines strategic vision, cultural transformation, process excellence, and external collaboration. Organizations that master innovation management will be better positioned to create value, compete effectively, and adapt to future challenges and opportunities.
"""),

    # Science
    ("science_08_environmental_science.csv", """Category,Topic,Description,Key Concepts,Measurement Methods,Environmental Impact,Solutions
Atmosphere,Climate Change,Long-term changes in global climate patterns,Greenhouse gases; Global warming; Climate feedback loops,Temperature records; Ice core data; Satellite measurements,Rising temperatures; Sea level rise; Extreme weather,Renewable energy; Carbon capture; Policy measures
Atmosphere,Air Pollution,Contamination of air by harmful substances,Particulate matter; Ozone; Nitrogen oxides; Sulfur dioxide,Air quality monitoring; Emission measurements; Health studies,Respiratory diseases; Acid rain; Smog formation,Emission controls; Clean technologies; Urban planning
Atmosphere,Ozone Depletion,Reduction of ozone layer in stratosphere,CFCs; Ozone hole; UV radiation; Montreal Protocol,Satellite monitoring; Ground-based measurements; Chemical analysis,Increased UV exposure; Skin cancer; Ecosystem damage,CFC phase-out; Alternative chemicals; International cooperation
Hydrosphere,Water Pollution,Contamination of water bodies,Point sources; Non-point sources; Eutrophication; Bioaccumulation,Water quality testing; Chemical analysis; Biological indicators,Ecosystem disruption; Human health risks; Economic losses,Wastewater treatment; Source control; Watershed management
Hydrosphere,Water Scarcity,Insufficient water resources for human needs,Water stress; Drought; Aquifer depletion; Water security,Flow measurements; Groundwater monitoring; Demand analysis,Agricultural impacts; Economic disruption; Social conflict,Water conservation; Desalination; Efficient irrigation
Hydrosphere,Ocean Acidification,Decrease in ocean pH due to CO2 absorption,Carbonic acid; Coral bleaching; Shell dissolution; Marine food webs,pH measurements; Chemical monitoring; Biological surveys,Marine ecosystem damage; Fisheries decline; Economic impacts,CO2 reduction; Marine protected areas; Adaptation strategies
Lithosphere,Soil Degradation,Deterioration of soil quality and productivity,Erosion; Salinization; Contamination; Nutrient depletion,Soil sampling; Erosion measurements; Chemical analysis,Reduced agricultural productivity; Food security; Economic losses,Sustainable agriculture; Soil conservation; Restoration
Lithosphere,Land Use Change,Conversion of natural habitats to human uses,Deforestation; Urbanization; Agricultural expansion; Habitat fragmentation,Remote sensing; GIS analysis; Land cover mapping,Biodiversity loss; Climate impacts; Ecosystem service loss,Land use planning; Protected areas; Sustainable development
Lithosphere,Mining Impacts,Environmental effects of mineral extraction,Habitat destruction; Water pollution; Air pollution; Waste generation,Environmental monitoring; Impact assessments; Restoration monitoring,Ecosystem damage; Community displacement; Health impacts,Sustainable mining; Restoration; Alternative materials
Biosphere,Biodiversity Loss,Decline in species diversity and abundance,Extinction rates; Habitat loss; Invasive species; Overexploitation,Species surveys; Population monitoring; Genetic analysis,Ecosystem instability; Loss of services; Reduced resilience,Conservation; Habitat protection; Sustainable use
Biosphere,Ecosystem Services,Benefits that humans derive from ecosystems,Provisioning; Regulating; Cultural; Supporting services,Economic valuation; Ecosystem mapping; Service quantification,Loss of benefits; Economic costs; Human well-being impacts,Ecosystem restoration; Payment for services; Sustainable management
Biosphere,Invasive Species,Non-native species that cause ecological harm,Introduction pathways; Establishment; Spread; Impact,Species monitoring; Distribution mapping; Impact assessment,Native species displacement; Economic damage; Ecosystem disruption,Prevention; Early detection; Control; Management
Energy,Renewable Energy,Energy from naturally replenishing sources,Solar; Wind; Hydro; Geothermal; Biomass,Energy production monitoring; Efficiency measurements; Lifecycle analysis,Reduced emissions; Environmental benefits; Sustainability,Technology development; Policy support; Investment
Energy,Energy Efficiency,Using less energy to provide same service,Conservation; Efficiency improvements; Demand reduction,Energy audits; Consumption monitoring; Performance metrics,Reduced environmental impact; Cost savings; Resource conservation,Efficient technologies; Building standards; Behavioral change
Energy,Fossil Fuels,Energy from ancient organic matter,Coal; Oil; Natural gas; Combustion; Emissions,Production monitoring; Emission measurements; Reserve assessments,Climate change; Air pollution; Environmental degradation,Transition to renewables; Efficiency; Carbon pricing
Waste,Solid Waste,Management of municipal and industrial waste,Generation; Collection; Treatment; Disposal; Recycling,Waste audits; Composition analysis; Diversion rates,Land pollution; Resource depletion; Greenhouse gas emissions,Waste reduction; Recycling; Composting; Circular economy
Waste,Hazardous Waste,Management of dangerous waste materials,Toxicity; Persistence; Bioaccumulation; Treatment,Chemical analysis; Risk assessment; Monitoring,Human health risks; Environmental contamination; Long-term impacts,Source reduction; Safe disposal; Treatment technologies
Waste,Electronic Waste,Disposal of electronic devices and components,E-waste generation; Toxic materials; Resource recovery,Collection tracking; Material analysis; Recovery rates,Toxic exposure; Resource loss; Environmental contamination,Extended producer responsibility; Recycling; Design for environment
Pollution,Chemical Pollution,Contamination by synthetic chemicals,Persistent organic pollutants; Endocrine disruptors; Heavy metals,Chemical monitoring; Biomonitoring; Risk assessment,Health impacts; Ecosystem damage; Bioaccumulation,Chemical regulation; Green chemistry; Substitution
Pollution,Noise Pollution,Excessive or harmful levels of noise,Sound levels; Frequency; Duration; Sources,Sound level measurements; Noise mapping; Health studies,Hearing damage; Stress; Wildlife impacts,Noise control; Urban planning; Technology improvements
Pollution,Light Pollution,Excessive artificial light in environment,Sky glow; Glare; Light trespass; Circadian disruption,Light measurements; Sky brightness monitoring; Ecological studies,Wildlife disruption; Energy waste; Human health impacts,Lighting design; Shielding; Timing controls"""),

    # Legal
    ("legal_06_international_law.xml", """<?xml version="1.0" encoding="UTF-8"?>
<international_law_guide>
    <overview>
        <title>International Law Principles and Practice</title>
        <description>Comprehensive guide to public international law, treaties, and international relations</description>
        <scope>Public international law, international organizations, dispute resolution</scope>
    </overview>

    <sources_of_international_law>
        <primary_sources>
            <treaties>
                <description>Written agreements between states</description>
                <types>
                    <bilateral>Between two states</bilateral>
                    <multilateral>Between multiple states</multilateral>
                    <framework>General principles requiring implementation</framework>
                    <protocol>Amendments or additions to existing treaties</protocol>
                </types>
                <examples>
                    <example>UN Charter</example>
                    <example>Geneva Conventions</example>
                    <example>Paris Climate Agreement</example>
                    <example>Vienna Convention on Diplomatic Relations</example>
                </examples>
            </treaties>

            <customary_law>
                <description>Practices accepted as legally binding</description>
                <elements>
                    <state_practice>Consistent behavior by states</state_practice>
                    <opinio_juris>Belief that practice is legally required</opinio_juris>
                </elements>
                <examples>
                    <example>Diplomatic immunity</example>
                    <example>Freedom of navigation</example>
                    <example>Prohibition of torture</example>
                </examples>
            </customary_law>

            <general_principles>
                <description>Fundamental legal principles recognized by civilized nations</description>
                <examples>
                    <example>Good faith</example>
                    <example>Pacta sunt servanda (agreements must be kept)</example>
                    <example>Due process</example>
                    <example>Proportionality</example>
                </examples>
            </general_principles>
        </primary_sources>

        <subsidiary_sources>
            <judicial_decisions>
                <icj>International Court of Justice decisions</icj>
                <arbitral_tribunals>International arbitration awards</arbitral_tribunals>
                <regional_courts>European Court of Human Rights, etc.</regional_courts>
            </judicial_decisions>

            <scholarly_writings>
                <description>Academic commentary and analysis</description>
                <role>Subsidiary means for determining law</role>
            </scholarly_writings>
        </subsidiary_sources>
    </sources_of_international_law>

    <key_principles>
        <sovereignty>
            <description>States have supreme authority within their territory</description>
            <implications>
                <non_interference>States cannot interfere in domestic affairs of others</non_interference>
                <territorial_integrity>Borders must be respected</territorial_integrity>
                <political_independence>States choose their own government</political_independence>
            </implications>
        </sovereignty>

        <equality>
            <description>All states are equal under international law</description>
            <applications>
                <voting_rights>Equal representation in international organizations</voting_rights>
                <legal_capacity>Same rights and obligations</legal_capacity>
            </applications>
        </equality>

        <peaceful_settlement>
            <description>Disputes should be resolved peacefully</description>
            <methods>
                <negotiation>Direct talks between parties</negotiation>
                <mediation>Third party assistance</mediation>
                <arbitration>Binding third party decision</arbitration>
                <adjudication>Court proceedings</adjudication>
            </methods>
        </peaceful_settlement>
    </key_principles>

    <international_organizations>
        <united_nations>
            <structure>
                <general_assembly>All member states represented</general_assembly>
                <security_council>15 members, 5 permanent with veto power</security_council>
                <economic_social_council>54 members, economic and social issues</economic_social_council>
                <trusteeship_council>Suspended operations</trusteeship_council>
                <international_court_justice>Principal judicial organ</international_court_justice>
                <secretariat>Administrative organ headed by Secretary-General</secretariat>
            </structure>

            <purposes>
                <peace_security>Maintain international peace and security</peace_security>
                <cooperation>Promote international cooperation</cooperation>
                <human_rights>Promote respect for human rights</human_rights>
                <self_determination>Respect for equal rights and self-determination</self_determination>
            </purposes>
        </united_nations>

        <regional_organizations>
            <european_union>
                <description>Political and economic union of European states</description>
                <institutions>European Parliament, Council, Commission, Court of Justice</institutions>
            </european_union>

            <african_union>
                <description>Continental union of African states</description>
                <goals>Political and economic integration, peace and security</goals>
            </african_union>

            <organization_american_states>
                <description>Regional organization of American states</description>
                <focus>Democracy, human rights, security, development</focus>
            </organization_american_states>
        </regional_organizations>

        <specialized_agencies>
            <world_health_organization>Global health coordination</world_health_organization>
            <international_labour_organization>Labor standards and rights</international_labour_organization>
            <world_trade_organization>International trade regulation</world_trade_organization>
            <international_monetary_fund>Monetary cooperation and stability</international_monetary_fund>
        </specialized_agencies>
    </international_organizations>

    <human_rights_law>
        <universal_declaration>
            <adoption>1948 by UN General Assembly</adoption>
            <status>Not legally binding but customary law</status>
            <rights>Civil, political, economic, social, cultural rights</rights>
        </universal_declaration>

        <core_treaties>
            <iccpr>International Covenant on Civil and Political Rights</iccpr>
            <icescr>International Covenant on Economic, Social and Cultural Rights</icescr>
            <cerd>Convention on Elimination of Racial Discrimination</cerd>
            <cedaw>Convention on Elimination of Discrimination Against Women</cedaw>
            <cat>Convention Against Torture</cat>
            <crc>Convention on Rights of the Child</crc>
        </core_treaties>

        <regional_systems>
            <european>European Convention on Human Rights</european>
            <inter_american>American Convention on Human Rights</inter_american>
            <african>African Charter on Human and Peoples' Rights</african>
        </regional_systems>
    </human_rights_law>

    <international_humanitarian_law>
        <geneva_conventions>
            <description>Laws of war and protection of civilians</description>
            <conventions>
                <first>Wounded and sick in armed forces</first>
                <second>Wounded, sick, and shipwrecked at sea</second>
                <third>Prisoners of war</third>
                <fourth>Civilian persons in time of war</fourth>
            </conventions>
            <additional_protocols>
                <protocol_i>International armed conflicts</protocol_i>
                <protocol_ii>Non-international armed conflicts</protocol_ii>
                <protocol_iii>Additional distinctive emblem</protocol_iii>
            </additional_protocols>
        </geneva_conventions>

        <principles>
            <distinction>Distinguish between civilians and combatants</distinction>
            <proportionality>Attacks must not cause excessive civilian harm</proportionality>
            <precaution>Take precautions to minimize civilian harm</precaution>
            <humanity>Prohibit unnecessary suffering</humanity>
        </principles>
    </international_humanitarian_law>

    <dispute_resolution>
        <international_court_justice>
            <jurisdiction>
                <contentious>Disputes between states</contentious>
                <advisory>Legal questions from UN organs</advisory>
            </jurisdiction>
            <procedure>
                <written>Memorial, counter-memorial, reply, rejoinder</written>
                <oral>Public hearings with arguments</oral>
                <judgment>Final and binding decision</judgment>
            </procedure>
        </international_court_justice>

        <arbitration>
            <permanent_court_arbitration>Established 1899, facilitates arbitration</permanent_court_arbitration>
            <icsid>Investment dispute arbitration</icsid>
            <wto_dispute_settlement>Trade dispute resolution</wto_dispute_settlement>
        </arbitration>

        <diplomatic_methods>
            <negotiation>Direct talks between parties</negotiation>
            <good_offices>Third party provides forum</good_offices>
            <mediation>Third party proposes solutions</mediation>
            <conciliation>Formal investigation and recommendations</conciliation>
        </diplomatic_methods>
    </dispute_resolution>

    <state_responsibility>
        <elements>
            <attribution>Conduct attributable to state</attribution>
            <breach>Violation of international obligation</breach>
        </elements>

        <circumstances_precluding_wrongfulness>
            <consent>Injured state consents to conduct</consent>
            <self_defense>Lawful measures of self-defense</self_defense>
            <countermeasures>Response to internationally wrongful act</countermeasures>
            <force_majeure>Irresistible force or unforeseen event</force_majeure>
            <distress>No other reasonable way to save lives</distress>
            <necessity>Only way to safeguard essential interest</necessity>
        </circumstances_precluding_wrongfulness>

        <consequences>
            <cessation>End the wrongful conduct</cessation>
            <non_repetition>Assurances and guarantees</non_repetition>
            <reparation>Restitution, compensation, satisfaction</reparation>
        </consequences>
    </state_responsibility>

    <contemporary_challenges>
        <climate_change>
            <paris_agreement>Global climate action framework</paris_agreement>
            <common_differentiated_responsibilities>Different obligations based on capabilities</common_differentiated_responsibilities>
            <loss_damage>Compensation for climate impacts</loss_damage>
        </climate_change>

        <cyber_warfare>
            <tallinn_manual>Expert analysis of cyber law</tallinn_manual>
            <attribution>Identifying state responsibility for cyber attacks</attribution>
            <proportionality>Appropriate response to cyber attacks</proportionality>
        </cyber_warfare>

        <space_law>
            <outer_space_treaty>Peaceful use of outer space</outer_space_treaty>
            <moon_agreement>Moon and celestial bodies governance</moon_agreement>
            <space_debris>Liability for space object damage</space_debris>
        </space_law>

        <artificial_intelligence>
            <autonomous_weapons>Regulation of lethal autonomous weapons</autonomous_weapons>
            <liability>Responsibility for AI decisions</liability>
            <governance>International AI governance frameworks</governance>
        </artificial_intelligence>
    </contemporary_challenges>
</international_law_guide>"""),

    # Education
    ("education_06_special_education.md", """# Special Education: Principles, Practices, and Legal Framework

## Introduction
Special education provides specialized instruction and related services to students with disabilities, ensuring they receive a free appropriate public education (FAPE) in the least restrictive environment (LRE).

## Legal Foundation

### Individuals with Disabilities Education Act (IDEA)
- **Purpose**: Ensure FAPE for students with disabilities
- **Key Principles**: Zero reject, nondiscriminatory evaluation, FAPE, LRE, procedural safeguards, parent participation
- **Age Range**: Birth to 21 years
- **Funding**: Federal funding to states and local districts

### Section 504 of Rehabilitation Act
- **Coverage**: Students with disabilities who don't qualify under IDEA
- **Accommodations**: Modifications to regular education programs
- **Civil Rights**: Protection from discrimination
- **Broader Definition**: Any physical or mental impairment

### Americans with Disabilities Act (ADA)
- **Public Accommodations**: Access to school facilities and programs
- **Employment**: Protection for school employees with disabilities
- **Communication**: Auxiliary aids and services
- **Physical Access**: Architectural accessibility

## Disability Categories under IDEA

### Intellectual Disability
- Significantly below average intellectual functioning
- Deficits in adaptive behavior
- Manifested during developmental period
- Educational impact on learning

### Specific Learning Disabilities
- **Dyslexia**: Reading difficulties
- **Dyscalculia**: Math difficulties
- **Dysgraphia**: Writing difficulties
- **Processing Disorders**: Auditory, visual, or language processing

### Autism Spectrum Disorders
- Social communication challenges
- Restricted and repetitive behaviors
- Sensory sensitivities
- Wide range of abilities and needs

### Emotional Disturbance
- Inability to learn not explained by other factors
- Inappropriate behaviors or feelings
- Pervasive mood of unhappiness or depression
- Physical symptoms or fears

### Speech or Language Impairments
- **Articulation Disorders**: Speech sound production
- **Fluency Disorders**: Stuttering or cluttering
- **Voice Disorders**: Pitch, loudness, or quality
- **Language Disorders**: Receptive or expressive language

### Other Health Impairments
- ADHD (Attention Deficit Hyperactivity Disorder)
- Epilepsy and seizure disorders
- Diabetes and other chronic conditions
- Limited strength, vitality, or alertness

### Physical Disabilities
- **Orthopedic Impairments**: Mobility limitations
- **Traumatic Brain Injury**: Acquired brain injury
- **Multiple Disabilities**: Combination of impairments
- **Deaf-Blindness**: Combined hearing and visual impairments

### Sensory Impairments
- **Visual Impairments**: Blindness or low vision
- **Hearing Impairments**: Deafness or hard of hearing
- **Deaf-Blindness**: Combined sensory impairments

## Special Education Process

### Referral and Identification
- Teacher or parent concerns
- Response to Intervention (RTI) data
- Screening and early identification
- Formal referral for evaluation

### Evaluation and Assessment
- **Comprehensive Evaluation**: Multiple assessments and observations
- **Multidisciplinary Team**: Various professionals involved
- **Nondiscriminatory**: Culturally and linguistically appropriate
- **Informed Consent**: Parent permission required

### Eligibility Determination
- Review of evaluation data
- Determination of disability category
- Educational need for special education
- Team decision-making process

### Individualized Education Program (IEP)
- **Present Levels**: Current academic and functional performance
- **Goals and Objectives**: Measurable annual goals
- **Services**: Special education and related services
- **Placement**: Least restrictive environment
- **Transition**: Post-secondary goals and services

## Instructional Strategies

### Universal Design for Learning (UDL)
- **Multiple Means of Representation**: How information is presented
- **Multiple Means of Engagement**: How students are motivated
- **Multiple Means of Action/Expression**: How students demonstrate learning
- **Proactive Design**: Accessible from the start

### Differentiated Instruction
- **Content**: What students learn
- **Process**: How students learn
- **Product**: How students show what they know
- **Learning Environment**: Physical and emotional climate

### Evidence-Based Practices
- **Applied Behavior Analysis (ABA)**: Systematic behavior intervention
- **Direct Instruction**: Explicit, systematic teaching
- **Cognitive Strategy Instruction**: Teaching thinking strategies
- **Peer-Mediated Instruction**: Student-to-student support

### Assistive Technology
- **Low-Tech**: Simple tools and adaptations
- **High-Tech**: Computer-based solutions
- **Communication Devices**: AAC (Augmentative and Alternative Communication)
- **Mobility Aids**: Wheelchairs, walkers, positioning devices

## Related Services

### Speech-Language Therapy
- Communication assessment and intervention
- Articulation and language therapy
- Augmentative communication support
- Swallowing and feeding therapy

### Occupational Therapy
- Fine motor skill development
- Sensory integration therapy
- Activities of daily living
- Assistive technology assessment

### Physical Therapy
- Gross motor skill development
- Mobility and positioning
- Strength and endurance building
- Equipment recommendations

### School Psychology Services
- Psychological and educational assessment
- Counseling and mental health support
- Behavior intervention planning
- Crisis intervention

### School Social Work
- Family support and advocacy
- Community resource coordination
- Attendance and truancy intervention
- Transition planning support

## Inclusive Education

### Least Restrictive Environment (LRE)
- General education classroom with supports
- Resource room for specialized instruction
- Separate classroom for intensive needs
- Separate school or residential placement

### Co-Teaching Models
- **One Teach, One Assist**: Support teacher assists
- **Station Teaching**: Students rotate between teachers
- **Parallel Teaching**: Teachers teach same content to different groups
- **Alternative Teaching**: One teacher works with small group
- **Team Teaching**: Both teachers share instruction

### Collaboration Strategies
- **Professional Learning Communities**: Shared responsibility for all students
- **Consultation Model**: Special educator advises general educator
- **Collaborative Planning**: Joint lesson and unit planning
- **Data-Based Decision Making**: Using student data to guide instruction

## Behavior Support

### Positive Behavior Interventions and Supports (PBIS)
- **School-wide Systems**: Universal behavior expectations
- **Targeted Interventions**: Small group supports
- **Intensive Interventions**: Individual behavior plans
- **Data-Based Decisions**: Continuous monitoring and adjustment

### Functional Behavior Assessment (FBA)
- Identify function or purpose of behavior
- Analyze antecedents and consequences
- Develop hypothesis about behavior
- Design intervention based on function

### Behavior Intervention Plan (BIP)
- Replacement behaviors to teach
- Environmental modifications
- Consequence strategies
- Crisis intervention procedures

## Transition Services

### Early Childhood Transition
- Transition from early intervention to preschool
- Individualized Family Service Plan (IFSP) to IEP
- Coordination between agencies
- Family support and preparation

### School-to-Adult Life Transition
- **Post-Secondary Education**: College and vocational training
- **Employment**: Job skills and career preparation
- **Independent Living**: Daily living and self-advocacy skills
- **Community Participation**: Recreation and social activities

### Transition Planning Process
- Begin by age 16 (or earlier)
- Student-centered planning
- Interagency collaboration
- Family involvement and support

## Assessment and Evaluation

### Progress Monitoring
- Regular data collection on IEP goals
- Curriculum-based measurement
- Behavioral data tracking
- Adjustment of instruction based on data

### Standardized Assessments
- **Accommodations**: Changes in how test is given
- **Modifications**: Changes in what is tested
- **Alternate Assessments**: For students with significant disabilities
- **Universal Design**: Accessible test design

### Portfolio Assessment
- Collection of student work over time
- Multiple types of evidence
- Student reflection and self-assessment
- Authentic demonstration of learning

## Family Engagement

### Parent Rights and Responsibilities
- Informed consent for evaluation and services
- Participation in IEP meetings
- Access to educational records
- Due process rights

### Collaborative Partnerships
- Shared decision-making
- Regular communication
- Home-school coordination
- Cultural responsiveness

### Advocacy and Support
- Parent training and information centers
- Support groups and networks
- Legal advocacy resources
- Empowerment and self-advocacy

## Professional Development

### Special Education Teacher Preparation
- Content knowledge in disability areas
- Instructional strategies and methods
- Assessment and evaluation skills
- Collaboration and consultation

### Ongoing Professional Learning
- Evidence-based practice updates
- Technology integration
- Cultural competency development
- Leadership and advocacy skills

### Interdisciplinary Collaboration
- Team-based service delivery
- Shared professional development
- Cross-disciplinary understanding
- Communication and consultation skills

## Current Issues and Trends

### Inclusion and Equity
- Disproportionate representation in special education
- Cultural and linguistic diversity
- Intersectionality of identities
- Social justice perspectives

### Technology Integration
- Assistive technology advances
- Digital accessibility
- Online and remote learning
- Data management systems

### Evidence-Based Practices
- Research-to-practice gap
- Implementation science
- Fidelity of implementation
- Continuous improvement

### Policy and Funding
- IDEA reauthorization
- State and local funding formulas
- Accountability and outcomes
- Personnel shortages

## Conclusion
Special education continues to evolve as our understanding of disabilities, effective practices, and inclusive education grows. The field emphasizes individualized, evidence-based approaches that support students with disabilities in achieving their full potential while promoting inclusion, equity, and self-determination. Success requires collaboration among educators, families, and communities to create supportive learning environments for all students.
""")
]

# Create all documents
for filename, content in final_docs:
    file_path = docs_dir / filename

    if isinstance(content, dict):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    print(f"Created: {file_path}")

# Count total documents
total_docs = len(list(docs_dir.glob('*')))
print(f"\nTotal documents in dataset: {total_docs}")