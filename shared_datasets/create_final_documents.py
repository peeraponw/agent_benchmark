#!/usr/bin/env python3
"""
Script to create the final batch of RAG documents to reach 40+ total documents.
"""

import json
import os
from pathlib import Path

# Define the documents directory
docs_dir = Path("rag_documents/documents")

# Final batch of documents to reach 40+ total
documents = [
    # Science documents (6 more to reach 8 total)
    {
        "filename": "science_03_genetics_dna.md",
        "content": """# Genetics and DNA: Fundamentals of Heredity

## Introduction to Genetics
Genetics is the study of heredity and variation in living organisms. It explains how traits are passed from parents to offspring and how genetic diversity arises.

## DNA Structure and Function

### DNA Composition
- **Nucleotides**: Building blocks containing phosphate, sugar (deoxyribose), and nitrogenous base
- **Bases**: Adenine (A), Thymine (T), Guanine (G), Cytosine (C)
- **Base Pairing**: A-T and G-C complementary pairs
- **Double Helix**: Two antiparallel strands wound around each other

### DNA Replication
1. **Initiation**: DNA unwinds at origin of replication
2. **Elongation**: DNA polymerase adds complementary nucleotides
3. **Termination**: Replication completes when entire molecule is copied

### Gene Expression
- **Transcription**: DNA → RNA (mRNA, tRNA, rRNA)
- **Translation**: mRNA → Protein using genetic code
- **Regulation**: Control of when and how genes are expressed

## Mendelian Genetics

### Mendel's Laws
1. **Law of Segregation**: Allele pairs separate during gamete formation
2. **Law of Independent Assortment**: Genes for different traits assort independently
3. **Law of Dominance**: Dominant alleles mask recessive alleles

### Inheritance Patterns
- **Dominant**: Expressed when one copy present (AA, Aa)
- **Recessive**: Expressed only when two copies present (aa)
- **Codominance**: Both alleles expressed simultaneously
- **Incomplete Dominance**: Blended phenotype

## Modern Genetics

### Chromosomes and Karyotypes
- **Autosomes**: Non-sex chromosomes (22 pairs in humans)
- **Sex Chromosomes**: X and Y chromosomes
- **Karyotype**: Complete set of chromosomes in a cell

### Genetic Mutations
- **Point Mutations**: Single nucleotide changes
- **Insertions/Deletions**: Adding or removing nucleotides
- **Chromosomal Aberrations**: Large-scale changes
- **Causes**: Spontaneous errors, environmental factors

### Population Genetics
- **Allele Frequency**: Proportion of alleles in a population
- **Hardy-Weinberg Equilibrium**: Stable allele frequencies
- **Genetic Drift**: Random changes in allele frequencies
- **Natural Selection**: Differential survival and reproduction

## Genetic Technologies

### DNA Sequencing
- **Sanger Sequencing**: Chain termination method
- **Next-Generation Sequencing**: High-throughput parallel sequencing
- **Applications**: Genome projects, medical diagnosis, research

### Genetic Engineering
- **Recombinant DNA**: Combining DNA from different sources
- **CRISPR-Cas9**: Precise gene editing tool
- **Gene Therapy**: Treating diseases by modifying genes
- **Genetically Modified Organisms**: Altered genetic makeup

### Biotechnology Applications
- **Medicine**: Personalized treatments, drug development
- **Agriculture**: Improved crops, disease resistance
- **Forensics**: DNA fingerprinting, paternity testing
- **Conservation**: Preserving endangered species

## Human Genetics

### Genetic Disorders
- **Single Gene Disorders**: Sickle cell anemia, cystic fibrosis
- **Chromosomal Disorders**: Down syndrome, Turner syndrome
- **Multifactorial Disorders**: Heart disease, diabetes
- **Mitochondrial Disorders**: Inherited through maternal line

### Genetic Counseling
- **Risk Assessment**: Calculating probability of genetic conditions
- **Family History**: Pedigree analysis
- **Testing Options**: Carrier screening, prenatal testing
- **Ethical Considerations**: Privacy, discrimination, informed consent

## Epigenetics

### Mechanisms
- **DNA Methylation**: Chemical modification affecting gene expression
- **Histone Modification**: Changes to proteins packaging DNA
- **Non-coding RNA**: Regulatory molecules controlling gene expression

### Environmental Influences
- **Nutrition**: Diet affecting gene expression
- **Stress**: Environmental stressors causing epigenetic changes
- **Toxins**: Chemical exposure altering gene regulation
- **Inheritance**: Some epigenetic marks passed to offspring

## Genomics and Personalized Medicine

### Human Genome Project
- **Completion**: 2003, mapping all human genes
- **Impact**: Understanding genetic basis of disease
- **Cost Reduction**: From billions to hundreds of dollars

### Pharmacogenomics
- **Drug Response**: Genetic factors affecting medication effectiveness
- **Personalized Dosing**: Tailoring treatment to individual genetics
- **Adverse Reactions**: Predicting drug side effects

### Precision Medicine
- **Targeted Therapy**: Treatments based on genetic profile
- **Cancer Treatment**: Tumor-specific genetic alterations
- **Rare Diseases**: Genetic diagnosis and treatment

## Ethical and Social Implications

### Genetic Privacy
- **Data Security**: Protecting genetic information
- **Insurance Discrimination**: Genetic Information Nondiscrimination Act
- **Employment**: Workplace genetic testing policies

### Gene Editing Ethics
- **Therapeutic vs Enhancement**: Treating disease vs improving traits
- **Germline Editing**: Heritable genetic modifications
- **Consent**: Future generations cannot consent to changes

### Genetic Equity
- **Access**: Ensuring equal access to genetic technologies
- **Diversity**: Including diverse populations in genetic research
- **Global Health**: Addressing genetic diseases worldwide

## Future Directions

### Emerging Technologies
- **Base Editing**: Precise single nucleotide changes
- **Prime Editing**: Targeted insertions, deletions, replacements
- **Epigenome Editing**: Modifying gene expression without changing DNA

### Research Frontiers
- **Single Cell Genomics**: Analyzing individual cells
- **Spatial Genomics**: Gene expression in tissue context
- **Synthetic Biology**: Engineering biological systems

### Challenges
- **Complexity**: Understanding gene interactions and networks
- **Regulation**: Balancing innovation with safety
- **Education**: Public understanding of genetics

## Conclusion
Genetics has revolutionized our understanding of life and heredity. From Mendel's peas to CRISPR gene editing, the field continues to advance rapidly, offering new possibilities for treating disease, improving agriculture, and understanding evolution while raising important ethical questions about the future of genetic technology.
"""
    },
    {
        "filename": "science_04_renewable_energy.json",
        "content": {
            "title": "Renewable Energy Technologies and Systems",
            "overview": "Comprehensive guide to renewable energy sources, technologies, and implementation",
            "energy_sources": {
                "solar": {
                    "description": "Energy from sunlight converted to electricity or heat",
                    "technologies": {
                        "photovoltaic": {
                            "efficiency": "15-22% for commercial panels",
                            "lifespan": "25-30 years",
                            "applications": ["Residential rooftops", "Utility-scale farms", "Off-grid systems"]
                        },
                        "concentrated_solar_power": {
                            "efficiency": "15-25%",
                            "storage": "Molten salt thermal storage",
                            "applications": ["Large-scale power generation", "Industrial heat"]
                        }
                    },
                    "advantages": ["Abundant resource", "No emissions during operation", "Declining costs"],
                    "challenges": ["Intermittency", "Weather dependence", "Energy storage needs"]
                },
                "wind": {
                    "description": "Kinetic energy from wind converted to electricity",
                    "technologies": {
                        "onshore": {
                            "capacity_factor": "25-35%",
                            "turbine_size": "2-3 MW typical",
                            "cost": "$1,200-1,700 per kW installed"
                        },
                        "offshore": {
                            "capacity_factor": "35-45%",
                            "turbine_size": "6-15 MW",
                            "cost": "$3,000-5,000 per kW installed"
                        }
                    },
                    "advantages": ["High capacity factors offshore", "Mature technology", "Job creation"],
                    "challenges": ["Visual impact", "Noise concerns", "Bird and bat mortality"]
                },
                "hydroelectric": {
                    "description": "Energy from flowing or falling water",
                    "types": {
                        "large_hydro": {
                            "capacity": "> 30 MW",
                            "efficiency": "80-90%",
                            "lifespan": "50-100 years"
                        },
                        "small_hydro": {
                            "capacity": "< 30 MW",
                            "environmental_impact": "Lower than large hydro",
                            "applications": ["Rural electrification", "Distributed generation"]
                        },
                        "pumped_storage": {
                            "function": "Energy storage and grid balancing",
                            "efficiency": "70-85%",
                            "capacity": "Can store energy for hours to days"
                        }
                    },
                    "advantages": ["High efficiency", "Long lifespan", "Grid stability services"],
                    "challenges": ["Environmental impact", "Displacement of communities", "Drought vulnerability"]
                },
                "geothermal": {
                    "description": "Heat from Earth's interior converted to electricity or direct use",
                    "technologies": {
                        "dry_steam": {
                            "temperature": "> 235°C",
                            "efficiency": "10-15%",
                            "locations": ["The Geysers, California", "Larderello, Italy"]
                        },
                        "flash_steam": {
                            "temperature": "150-235°C",
                            "process": "Hot water flashed to steam",
                            "most_common": "Most widely used technology"
                        },
                        "binary_cycle": {
                            "temperature": "85-150°C",
                            "process": "Heat exchanger with working fluid",
                            "environmental": "Closed-loop system"
                        }
                    },
                    "advantages": ["Baseload power", "Small land footprint", "Low emissions"],
                    "challenges": ["Geographic limitations", "High upfront costs", "Induced seismicity"]
                },
                "biomass": {
                    "description": "Organic matter converted to energy",
                    "feedstocks": {
                        "wood": ["Forest residues", "Energy crops", "Wood pellets"],
                        "agricultural": ["Crop residues", "Energy crops", "Animal waste"],
                        "municipal": ["Organic waste", "Landfill gas", "Sewage sludge"]
                    },
                    "conversion_technologies": {
                        "combustion": "Direct burning for heat and electricity",
                        "gasification": "Thermal conversion to synthetic gas",
                        "pyrolysis": "Thermal decomposition without oxygen",
                        "anaerobic_digestion": "Biological conversion to biogas"
                    },
                    "advantages": ["Carbon neutral potential", "Waste utilization", "Energy storage"],
                    "challenges": ["Land use competition", "Air quality concerns", "Supply chain logistics"]
                }
            },
            "energy_storage": {
                "battery_technologies": {
                    "lithium_ion": {
                        "energy_density": "150-250 Wh/kg",
                        "efficiency": "85-95%",
                        "applications": ["Grid storage", "Electric vehicles", "Residential systems"]
                    },
                    "flow_batteries": {
                        "duration": "4-12 hours typical",
                        "scalability": "Independent power and energy scaling",
                        "lifespan": "20+ years"
                    }
                },
                "mechanical_storage": {
                    "pumped_hydro": {
                        "capacity": "95% of global storage capacity",
                        "efficiency": "70-85%",
                        "duration": "Hours to days"
                    },
                    "compressed_air": {
                        "technology": "CAES - Compressed Air Energy Storage",
                        "efficiency": "40-70%",
                        "applications": ["Grid-scale storage", "Load balancing"]
                    }
                }
            },
            "grid_integration": {
                "challenges": {
                    "intermittency": "Variable output from solar and wind",
                    "grid_stability": "Maintaining frequency and voltage",
                    "transmission": "Connecting remote renewable resources to load centers"
                },
                "solutions": {
                    "smart_grids": "Advanced monitoring and control systems",
                    "demand_response": "Adjusting consumption to match generation",
                    "energy_storage": "Storing excess energy for later use",
                    "grid_flexibility": "Flexible generation and consumption"
                }
            },
            "economics": {
                "cost_trends": {
                    "solar_pv": "85% cost reduction 2010-2020",
                    "onshore_wind": "70% cost reduction 2010-2020",
                    "offshore_wind": "48% cost reduction 2010-2020"
                },
                "levelized_cost": {
                    "solar_pv": "$0.048-0.142 per kWh",
                    "onshore_wind": "$0.023-0.076 per kWh",
                    "offshore_wind": "$0.075-0.213 per kWh"
                },
                "financing": {
                    "mechanisms": ["Power purchase agreements", "Feed-in tariffs", "Renewable energy certificates"],
                    "challenges": ["High upfront costs", "Long payback periods", "Policy uncertainty"]
                }
            },
            "environmental_impact": {
                "benefits": {
                    "ghg_reduction": "Significant reduction in greenhouse gas emissions",
                    "air_quality": "Reduced air pollution and health impacts",
                    "water_use": "Lower water consumption than fossil fuels"
                },
                "considerations": {
                    "land_use": "Large land requirements for some technologies",
                    "materials": "Mining and processing of rare earth elements",
                    "end_of_life": "Recycling and disposal of renewable energy equipment"
                }
            },
            "policy_support": {
                "mechanisms": {
                    "renewable_portfolio_standards": "Mandating percentage of renewable energy",
                    "feed_in_tariffs": "Guaranteed payments for renewable energy",
                    "tax_incentives": "Investment and production tax credits",
                    "carbon_pricing": "Making fossil fuels more expensive"
                },
                "international_agreements": {
                    "paris_agreement": "Global commitment to limit warming to 1.5-2°C",
                    "sdg7": "UN Sustainable Development Goal for clean energy",
                    "irena": "International Renewable Energy Agency coordination"
                }
            }
        }
    }
]

# Create all documents
for doc in documents:
    file_path = docs_dir / doc["filename"]

    if isinstance(doc["content"], dict):
        # JSON content
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(doc["content"], f, indent=2, ensure_ascii=False)
    else:
        # Text/Markdown content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])

    print(f"Created: {file_path}")

    # Legal documents (4 more to reach 6 total)
    {
        "filename": "legal_02_contract_law.txt",
        "content": """Contract Law Fundamentals and Best Practices

INTRODUCTION TO CONTRACT LAW

A contract is a legally binding agreement between two or more parties that creates mutual obligations enforceable by law. Contract law governs the formation, performance, and enforcement of these agreements.

ELEMENTS OF A VALID CONTRACT

Offer:
An offer is a promise to do or refrain from doing something in exchange for consideration. It must be:
- Definite and certain in terms
- Communicated to the offeree
- Made with intent to be bound

Acceptance:
Acceptance is the offeree's agreement to the terms of the offer. It must be:
- Unqualified and unconditional
- Communicated to the offeror
- Made within a reasonable time or specified time limit

Consideration:
Consideration is something of value exchanged between parties. It can be:
- Money, goods, or services
- A promise to do or refrain from doing something
- Must be legally sufficient (not necessarily adequate)

Capacity:
Parties must have legal capacity to enter contracts:
- Age of majority (18 in most jurisdictions)
- Mental competence
- Not under duress or undue influence

Legality:
The contract's purpose and terms must be legal:
- Not violate statutes or public policy
- Not involve illegal activities
- Not unconscionable or against public interest

TYPES OF CONTRACTS

Express vs. Implied:
- Express: Terms explicitly stated orally or in writing
- Implied: Terms inferred from conduct or circumstances

Bilateral vs. Unilateral:
- Bilateral: Both parties make promises (most common)
- Unilateral: One party makes promise in exchange for performance

Executed vs. Executory:
- Executed: Fully performed by all parties
- Executory: Performance still pending

Valid, Void, Voidable, Unenforceable:
- Valid: Meets all legal requirements
- Void: No legal effect from the beginning
- Voidable: Valid until one party chooses to void
- Unenforceable: Valid but cannot be enforced in court

CONTRACT FORMATION

Statute of Frauds:
Certain contracts must be in writing:
- Sale of real estate
- Contracts that cannot be performed within one year
- Sale of goods over $500 (UCC)
- Marriage contracts
- Contracts to pay another's debt

Parol Evidence Rule:
When parties have a written contract intended as final expression:
- Oral evidence cannot contradict written terms
- Exceptions: fraud, mistake, ambiguity, subsequent modifications

PERFORMANCE AND BREACH

Performance Standards:
- Complete Performance: Full compliance with contract terms
- Substantial Performance: Performance with minor deviations
- Material Breach: Significant failure to perform

Conditions:
- Condition Precedent: Must occur before performance is due
- Condition Subsequent: Terminates existing duty to perform
- Concurrent Conditions: Performances due simultaneously

Excuses for Non-Performance:
- Impossibility: Performance becomes objectively impossible
- Impracticability: Performance becomes extremely difficult/expensive
- Frustration of Purpose: Principal purpose is substantially frustrated

REMEDIES FOR BREACH

Damages:
- Compensatory: Put non-breaching party in position if contract performed
- Consequential: Foreseeable losses resulting from breach
- Incidental: Costs incurred due to breach
- Punitive: Rarely awarded in contract cases

Equitable Remedies:
- Specific Performance: Court orders actual performance
- Injunction: Court orders party to refrain from certain acts
- Rescission: Contract is cancelled and parties restored to pre-contract position
- Reformation: Contract terms are modified to reflect true intent

Mitigation of Damages:
Non-breaching party must take reasonable steps to minimize losses

SPECIAL CONTRACT TYPES

Sales Contracts (UCC):
- Uniform Commercial Code governs sale of goods
- Different rules for formation, performance, and remedies
- Warranties: express, implied warranty of merchantability, fitness for purpose

Employment Contracts:
- At-will employment vs. contract employment
- Non-compete and non-disclosure agreements
- Termination provisions and severance

Real Estate Contracts:
- Purchase agreements
- Lease agreements
- Specific performance commonly available
- Recording requirements

INTERNATIONAL CONTRACTS

Choice of Law:
- Parties can choose governing law
- Courts will honor reasonable choices
- Default rules apply if no choice made

Dispute Resolution:
- Litigation in courts
- Arbitration (binding or non-binding)
- Mediation and other ADR methods

CISG (Convention on International Sale of Goods):
- Governs international sales contracts
- Different rules from domestic law
- Parties can opt out

CONTRACT DRAFTING BEST PRACTICES

Clear and Precise Language:
- Use plain English when possible
- Define technical terms
- Avoid ambiguous language
- Be specific about obligations

Essential Clauses:
- Parties and their roles
- Scope of work or goods
- Payment terms and schedule
- Performance deadlines
- Termination provisions
- Dispute resolution mechanisms

Risk Allocation:
- Limitation of liability clauses
- Indemnification provisions
- Insurance requirements
- Force majeure clauses

COMMON CONTRACT ISSUES

Ambiguity:
- Courts interpret against drafter
- Extrinsic evidence may be considered
- Industry custom and usage

Unconscionability:
- Procedural: unfair bargaining process
- Substantive: unfair contract terms
- Courts may refuse to enforce

Mistake:
- Mutual mistake: both parties mistaken about material fact
- Unilateral mistake: generally not grounds for relief
- May void contract or allow reformation

ELECTRONIC CONTRACTS

E-SIGN Act and UETA:
- Electronic signatures legally valid
- Electronic records admissible
- Consent to electronic transactions

Formation Issues:
- Click-wrap agreements
- Browse-wrap agreements
- Email acceptances

CONCLUSION

Contract law provides the framework for commercial relationships and personal agreements. Understanding the basic principles helps parties create enforceable agreements, avoid disputes, and protect their interests. Proper contract drafting and management are essential business skills in today's commercial environment."""
    },
    {
        "filename": "legal_03_intellectual_property.csv",
        "content": """IP Type,Protection Duration,Requirements,Rights Granted,Registration Required,Examples,Enforcement
Patent,20 years from filing,Novel; Non-obvious; Useful; Patentable subject matter,Exclusive right to make use sell,Yes - USPTO,Inventions; Processes; Machines; Compositions,Federal court litigation; ITC proceedings
Trademark,Indefinite with renewal,Distinctive; Used in commerce; Not confusing,Exclusive right to use mark,No but recommended,Brand names; Logos; Slogans; Trade dress,Federal and state courts; TTAB proceedings
Copyright,Life + 70 years (individual); 95 years (corporate),Original work; Fixed in tangible medium; Minimal creativity,Reproduce; Distribute; Display; Perform; Create derivatives,No but recommended,Books; Music; Software; Art; Films,Federal court litigation; DMCA takedowns
Trade Secret,Indefinite if maintained,Information with economic value; Reasonable secrecy efforts,Exclusive use of confidential information,No,Formulas; Customer lists; Processes; Know-how,State court litigation; Misappropriation claims
Design Patent,15 years from grant,Novel; Non-obvious; Ornamental design,Exclusive right to use design,Yes - USPTO,Product appearance; GUI designs; Ornamental features,Federal court litigation
Utility Model,7-10 years (varies by country),Lower novelty threshold than patents; Utility,Exclusive right to use invention,Yes - varies by country,Simple mechanical devices; Incremental improvements,Varies by jurisdiction
Plant Patent,20 years from filing,Distinct; New plant variety; Asexually reproduced,Exclusive right to reproduce plant,Yes - USPTO,New plant varieties; Hybrid plants,Federal court litigation
Mask Work,10 years from registration,Original layout design; Fixed in semiconductor,Exclusive right to reproduce mask work,Yes - USPTO,Semiconductor chip layouts; IC designs,Federal court litigation
Geographical Indication,Indefinite,Product originates from specific region; Quality linked to origin,Exclusive right to use indication,Varies,Champagne; Roquefort cheese; Scotch whisky,Varies by jurisdiction
Publicity Rights,Varies by state,Use of person's name or likeness; Commercial value,Control commercial use of identity,No,Celebrity endorsements; Name and likeness use,State court litigation
Moral Rights,Life + 70 years (varies),Author of creative work; Recognized in some jurisdictions,Attribution; Integrity; Disclosure,Automatic,Artistic works; Literary works,Varies by jurisdiction
Database Rights,15 years (EU),Substantial investment in database; Sui generis protection,Prevent extraction and reutilization,No,Compilations; Databases; Collections,EU courts and national courts
Semiconductor Topography,10 years,Original topography; Commercial exploitation,Exclusive right to reproduce topography,Yes - varies,Integrated circuit layouts; Chip designs,Varies by jurisdiction"""
    },
    {
        "filename": "education_02_learning_theories.md",
        "content": """# Learning Theories and Educational Psychology

## Introduction
Learning theories provide frameworks for understanding how people acquire, process, and retain knowledge. These theories inform educational practices and help educators design effective learning experiences.

## Behaviorist Learning Theories

### Classical Conditioning (Pavlov)
- **Principle**: Learning through association between stimuli
- **Process**: Unconditioned stimulus → Conditioned stimulus → Conditioned response
- **Educational Application**: Creating positive associations with learning
- **Example**: Using pleasant music during study time

### Operant Conditioning (Skinner)
- **Principle**: Learning through consequences of behavior
- **Reinforcement**: Increases likelihood of behavior repetition
  - Positive reinforcement: Adding pleasant stimulus
  - Negative reinforcement: Removing unpleasant stimulus
- **Punishment**: Decreases likelihood of behavior repetition
- **Educational Application**: Reward systems, feedback, grading

### Social Learning Theory (Bandura)
- **Principle**: Learning through observation and imitation
- **Components**: Attention, retention, reproduction, motivation
- **Modeling**: Learning from observing others' behaviors
- **Educational Application**: Peer learning, teacher modeling, video demonstrations

## Cognitive Learning Theories

### Information Processing Theory
- **Model**: Mind as computer processing information
- **Components**: Sensory memory, short-term memory, long-term memory
- **Processes**: Encoding, storage, retrieval
- **Educational Application**: Chunking information, repetition, mnemonics

### Cognitive Load Theory (Sweller)
- **Principle**: Limited working memory capacity
- **Types of Load**:
  - Intrinsic: Inherent difficulty of material
  - Extraneous: Poor instructional design
  - Germane: Processing that builds schemas
- **Educational Application**: Simplify presentations, reduce distractions

### Schema Theory
- **Principle**: Knowledge organized in mental frameworks (schemas)
- **Process**: New information integrated into existing schemas
- **Accommodation**: Modifying schemas for new information
- **Assimilation**: Fitting new information into existing schemas
- **Educational Application**: Building on prior knowledge, concept mapping

## Constructivist Learning Theories

### Piaget's Cognitive Development
- **Stages**:
  1. Sensorimotor (0-2 years): Learning through senses and motor actions
  2. Preoperational (2-7 years): Symbolic thinking, language development
  3. Concrete Operational (7-11 years): Logical thinking about concrete objects
  4. Formal Operational (11+ years): Abstract and hypothetical thinking
- **Educational Application**: Age-appropriate instruction, hands-on learning

### Vygotsky's Social Development Theory
- **Zone of Proximal Development (ZPD)**: Gap between current and potential ability
- **Scaffolding**: Temporary support to help learners achieve goals
- **Social Interaction**: Learning occurs through social interaction
- **Cultural Tools**: Language, symbols, and cultural artifacts mediate learning
- **Educational Application**: Collaborative learning, peer tutoring, guided practice

### Constructivism (Bruner, Dewey)
- **Principle**: Learners actively construct knowledge through experience
- **Discovery Learning**: Learning through exploration and problem-solving
- **Spiral Curriculum**: Revisiting topics with increasing complexity
- **Educational Application**: Project-based learning, inquiry-based instruction

## Humanistic Learning Theories

### Maslow's Hierarchy of Needs
- **Levels**: Physiological, safety, belonging, esteem, self-actualization
- **Principle**: Lower needs must be met before higher needs
- **Educational Application**: Creating safe, supportive learning environments

### Rogers' Person-Centered Learning
- **Principles**: Learner autonomy, self-direction, personal relevance
- **Teacher Role**: Facilitator rather than authority figure
- **Educational Application**: Student-centered instruction, choice in learning

## Multiple Intelligence Theory (Gardner)

### Eight Intelligences
1. **Linguistic**: Word and language skills
2. **Logical-Mathematical**: Logic, reasoning, numbers
3. **Spatial**: Visual and spatial processing
4. **Musical**: Music, rhythm, sound
5. **Bodily-Kinesthetic**: Physical movement, coordination
6. **Interpersonal**: Understanding others, social skills
7. **Intrapersonal**: Self-awareness, introspection
8. **Naturalistic**: Nature, environment, patterns

### Educational Implications
- Recognize diverse strengths and learning styles
- Provide multiple ways to learn and demonstrate knowledge
- Differentiated instruction based on student strengths

## Learning Styles Theories

### VARK Model (Fleming)
- **Visual**: Learning through seeing (diagrams, charts, maps)
- **Auditory**: Learning through hearing (lectures, discussions)
- **Reading/Writing**: Learning through text (reading, note-taking)
- **Kinesthetic**: Learning through doing (hands-on activities)

### Kolb's Experiential Learning Cycle
1. **Concrete Experience**: Direct experience or activity
2. **Reflective Observation**: Thinking about the experience
3. **Abstract Conceptualization**: Understanding concepts and theories
4. **Active Experimentation**: Testing ideas in new situations

## Motivation Theories

### Self-Determination Theory (Deci & Ryan)
- **Basic Needs**:
  - Autonomy: Feeling volitional and self-directed
  - Competence: Feeling effective and capable
  - Relatedness: Feeling connected to others
- **Educational Application**: Choice, optimal challenge, supportive relationships

### Achievement Goal Theory
- **Mastery Goals**: Focus on learning and understanding
- **Performance Goals**: Focus on demonstrating ability
- **Approach vs. Avoidance**: Seeking success vs. avoiding failure
- **Educational Application**: Emphasize learning over grades, growth mindset

### Flow Theory (Csikszentmihalyi)
- **Characteristics**: Complete absorption, clear goals, immediate feedback
- **Conditions**: Balance between challenge and skill level
- **Educational Application**: Optimal challenge, clear objectives, timely feedback

## Memory and Learning

### Dual Coding Theory (Paivio)
- **Verbal System**: Processing linguistic information
- **Visual System**: Processing non-verbal imagery
- **Educational Application**: Combine text with visuals, use imagery

### Levels of Processing (Craik & Lockhart)
- **Shallow Processing**: Surface features (appearance, sound)
- **Deep Processing**: Meaning and significance
- **Educational Application**: Encourage meaningful learning, elaboration

### Forgetting Curve (Ebbinghaus)
- **Principle**: Rapid forgetting without reinforcement
- **Spaced Repetition**: Reviewing at increasing intervals
- **Educational Application**: Distributed practice, review sessions

## Modern Learning Theories

### Connectivism (Siemens)
- **Principle**: Learning as network formation in digital age
- **Characteristics**: Distributed knowledge, technology-mediated learning
- **Educational Application**: Online learning, social networks, digital literacy

### Transformative Learning (Mezirow)
- **Principle**: Learning that changes perspective and assumptions
- **Process**: Critical reflection on experiences and beliefs
- **Educational Application**: Critical thinking, perspective-taking, reflection

## Applications in Education

### Instructional Design
- **ADDIE Model**: Analysis, Design, Development, Implementation, Evaluation
- **Bloom's Taxonomy**: Hierarchical classification of learning objectives
- **Backward Design**: Starting with desired outcomes

### Assessment Strategies
- **Formative Assessment**: Ongoing feedback during learning
- **Summative Assessment**: Evaluation at end of instruction
- **Authentic Assessment**: Real-world application of knowledge

### Differentiated Instruction
- **Content**: What students learn
- **Process**: How students learn
- **Product**: How students demonstrate learning
- **Learning Environment**: Physical and emotional climate

## Conclusion
Learning theories provide valuable insights into how people learn and inform effective educational practices. Understanding these theories helps educators create engaging, effective learning experiences that accommodate diverse learners and promote deep, meaningful learning.
"""
    },
    {
        "filename": "education_03_curriculum_design.xml",
        "content": """<?xml version="1.0" encoding="UTF-8"?>
<curriculum_design_guide>
    <overview>
        <title>Curriculum Design and Development Framework</title>
        <description>Comprehensive guide to designing effective educational curricula</description>
        <scope>K-12 and higher education curriculum development</scope>
    </overview>

    <design_principles>
        <principle id="1">
            <name>Alignment</name>
            <description>Curriculum components must be aligned with learning objectives, assessments, and instructional methods</description>
            <implementation>
                <step>Define clear learning outcomes</step>
                <step>Design assessments that measure outcomes</step>
                <step>Select instructional strategies that support outcomes</step>
            </implementation>
        </principle>

        <principle id="2">
            <name>Coherence</name>
            <description>Curriculum should be logically organized and sequenced</description>
            <elements>
                <element>Vertical coherence: progression across grade levels</element>
                <element>Horizontal coherence: integration across subjects</element>
                <element>Internal coherence: consistency within courses</element>
            </elements>
        </principle>

        <principle id="3">
            <name>Relevance</name>
            <description>Content should be meaningful and applicable to students' lives</description>
            <strategies>
                <strategy>Connect to real-world applications</strategy>
                <strategy>Include diverse perspectives and cultures</strategy>
                <strategy>Address current issues and challenges</strategy>
            </strategies>
        </principle>

        <principle id="4">
            <name>Rigor</name>
            <description>Curriculum should challenge students appropriately</description>
            <components>
                <component>Depth of knowledge requirements</component>
                <component>Critical thinking expectations</component>
                <component>Problem-solving opportunities</component>
            </components>
        </principle>
    </design_principles>

    <development_process>
        <phase id="1">
            <name>Needs Assessment</name>
            <duration>2-4 weeks</duration>
            <activities>
                <activity>Analyze student demographics and needs</activity>
                <activity>Review current curriculum effectiveness</activity>
                <activity>Identify gaps and areas for improvement</activity>
                <activity>Consult stakeholders (teachers, parents, employers)</activity>
            </activities>
            <deliverables>
                <deliverable>Needs assessment report</deliverable>
                <deliverable>Stakeholder feedback summary</deliverable>
            </deliverables>
        </phase>

        <phase id="2">
            <name>Goal Setting</name>
            <duration>1-2 weeks</duration>
            <activities>
                <activity>Define program mission and vision</activity>
                <activity>Establish learning goals and objectives</activity>
                <activity>Align with institutional standards</activity>
                <activity>Set measurable outcomes</activity>
            </activities>
            <deliverables>
                <deliverable>Mission and vision statements</deliverable>
                <deliverable>Learning objectives framework</deliverable>
            </deliverables>
        </phase>

        <phase id="3">
            <name>Content Selection</name>
            <duration>3-6 weeks</duration>
            <activities>
                <activity>Research current knowledge in field</activity>
                <activity>Select essential content and skills</activity>
                <activity>Organize content into logical sequences</activity>
                <activity>Consider prerequisite knowledge</activity>
            </activities>
            <deliverables>
                <deliverable>Content outline and scope</deliverable>
                <deliverable>Prerequisite mapping</deliverable>
            </deliverables>
        </phase>

        <phase id="4">
            <name>Structure Design</name>
            <duration>2-4 weeks</duration>
            <activities>
                <activity>Determine course/unit organization</activity>
                <activity>Create scope and sequence charts</activity>
                <activity>Design pacing guides</activity>
                <activity>Plan integration opportunities</activity>
            </activities>
            <deliverables>
                <deliverable>Curriculum structure document</deliverable>
                <deliverable>Scope and sequence charts</deliverable>
            </deliverables>
        </phase>

        <phase id="5">
            <name>Assessment Design</name>
            <duration>2-3 weeks</duration>
            <activities>
                <activity>Design formative assessments</activity>
                <activity>Create summative assessments</activity>
                <activity>Develop rubrics and criteria</activity>
                <activity>Plan authentic assessments</activity>
            </activities>
            <deliverables>
                <deliverable>Assessment framework</deliverable>
                <deliverable>Sample assessments and rubrics</deliverable>
            </deliverables>
        </phase>

        <phase id="6">
            <name>Implementation Planning</name>
            <duration>2-3 weeks</duration>
            <activities>
                <activity>Develop implementation timeline</activity>
                <activity>Plan professional development</activity>
                <activity>Identify resource requirements</activity>
                <activity>Create communication strategy</activity>
            </activities>
            <deliverables>
                <deliverable>Implementation plan</deliverable>
                <deliverable>Professional development schedule</deliverable>
            </deliverables>
        </phase>
    </development_process>

    <curriculum_models>
        <model id="tyler">
            <name>Tyler Model</name>
            <developer>Ralph Tyler</developer>
            <steps>
                <step>Define educational objectives</step>
                <step>Select learning experiences</step>
                <step>Organize learning experiences</step>
                <step>Evaluate effectiveness</step>
            </steps>
            <strengths>
                <strength>Clear, systematic approach</strength>
                <strength>Emphasis on objectives</strength>
                <strength>Logical sequence</strength>
            </strengths>
            <limitations>
                <limitation>Linear, inflexible process</limitation>
                <limitation>Limited stakeholder input</limitation>
                <limitation>Behaviorist orientation</limitation>
            </limitations>
        </model>

        <model id="taba">
            <name>Taba Model</name>
            <developer>Hilda Taba</developer>
            <steps>
                <step>Diagnose needs</step>
                <step>Formulate objectives</step>
                <step>Select content</step>
                <step>Organize content</step>
                <step>Select learning experiences</step>
                <step>Organize learning experiences</step>
                <step>Determine evaluation methods</step>
            </steps>
            <strengths>
                <strength>Inductive approach</strength>
                <strength>Teacher involvement</strength>
                <strength>Detailed process</strength>
            </strengths>
        </model>

        <model id="wheeler">
            <name>Wheeler Model</name>
            <developer>D.K. Wheeler</developer>
            <characteristics>
                <characteristic>Cyclical process</characteristic>
                <characteristic>Continuous evaluation</characteristic>
                <characteristic>Flexible adaptation</characteristic>
            </characteristics>
            <phases>
                <phase>Aims, goals, and objectives</phase>
                <phase>Selection of learning experiences</phase>
                <phase>Selection of content</phase>
                <phase>Organization and integration</phase>
                <phase>Evaluation</phase>
            </phases>
        </model>
    </curriculum_models>

    <learning_theories_integration>
        <theory name="Constructivism">
            <application>
                <approach>Project-based learning</approach>
                <approach>Inquiry-driven curriculum</approach>
                <approach>Authentic problem-solving</approach>
            </application>
        </theory>

        <theory name="Multiple Intelligences">
            <application>
                <approach>Varied instructional methods</approach>
                <approach>Multiple assessment formats</approach>
                <approach>Differentiated learning paths</approach>
            </application>
        </theory>

        <theory name="Social Learning">
            <application>
                <approach>Collaborative learning activities</approach>
                <approach>Peer teaching opportunities</approach>
                <approach>Community-based learning</approach>
            </application>
        </theory>
    </learning_theories_integration>

    <assessment_strategies>
        <formative_assessment>
            <purpose>Monitor learning progress and provide feedback</purpose>
            <methods>
                <method>Exit tickets</method>
                <method>Quick polls and surveys</method>
                <method>Peer assessments</method>
                <method>Learning journals</method>
            </methods>
            <frequency>Ongoing throughout instruction</frequency>
        </formative_assessment>

        <summative_assessment>
            <purpose>Evaluate learning achievement at end of instruction</purpose>
            <methods>
                <method>Traditional tests and exams</method>
                <method>Performance tasks</method>
                <method>Portfolios</method>
                <method>Capstone projects</method>
            </methods>
            <timing>End of units, courses, or programs</timing>
        </summative_assessment>

        <authentic_assessment>
            <purpose>Evaluate learning in real-world contexts</purpose>
            <characteristics>
                <characteristic>Realistic tasks and contexts</characteristic>
                <characteristic>Complex, open-ended problems</characteristic>
                <characteristic>Multiple solution paths</characteristic>
                <characteristic>Collaboration opportunities</characteristic>
            </characteristics>
        </authentic_assessment>
    </assessment_strategies>

    <implementation_considerations>
        <stakeholder_engagement>
            <stakeholder group="teachers">
                <involvement>Curriculum development participation</involvement>
                <involvement>Professional development</involvement>
                <involvement>Feedback and evaluation</involvement>
            </stakeholder>

            <stakeholder group="students">
                <involvement>Pilot testing</involvement>
                <involvement>Feedback collection</involvement>
                <involvement>Learning outcome assessment</involvement>
            </stakeholder>

            <stakeholder group="parents">
                <involvement>Information sessions</involvement>
                <involvement>Home support strategies</involvement>
                <involvement>Progress communication</involvement>
            </stakeholder>

            <stakeholder group="administrators">
                <involvement>Resource allocation</involvement>
                <involvement>Policy alignment</involvement>
                <involvement>Implementation oversight</involvement>
            </stakeholder>
        </stakeholder_engagement>

        <resource_requirements>
            <category name="Human Resources">
                <resource>Curriculum specialists</resource>
                <resource>Subject matter experts</resource>
                <resource>Instructional designers</resource>
                <resource>Professional development facilitators</resource>
            </category>

            <category name="Material Resources">
                <resource>Textbooks and instructional materials</resource>
                <resource>Technology and software</resource>
                <resource>Assessment tools</resource>
                <resource>Professional development materials</resource>
            </category>

            <category name="Financial Resources">
                <resource>Development costs</resource>
                <resource>Implementation expenses</resource>
                <resource>Professional development funding</resource>
                <resource>Ongoing maintenance costs</resource>
            </category>
        </resource_requirements>

        <change_management>
            <strategy name="Communication">
                <description>Clear, consistent messaging about curriculum changes</description>
                <tactics>
                    <tactic>Regular updates and newsletters</tactic>
                    <tactic>Town hall meetings</tactic>
                    <tactic>FAQ documents</tactic>
                </tactics>
            </strategy>

            <strategy name="Training">
                <description>Comprehensive professional development for educators</description>
                <components>
                    <component>Curriculum content knowledge</component>
                    <component>Instructional strategies</component>
                    <component>Assessment methods</component>
                    <component>Technology integration</component>
                </components>
            </strategy>

            <strategy name="Support">
                <description>Ongoing assistance during implementation</description>
                <support_types>
                    <type>Mentoring programs</type>
                    <type>Coaching and feedback</type>
                    <type>Resource libraries</type>
                    <type>Technical assistance</type>
                </support_types>
            </strategy>
        </change_management>
    </implementation_considerations>

    <evaluation_framework>
        <evaluation_levels>
            <level name="Student Learning">
                <indicators>
                    <indicator>Achievement of learning objectives</indicator>
                    <indicator>Skill development progress</indicator>
                    <indicator>Knowledge retention</indicator>
                    <indicator>Transfer of learning</indicator>
                </indicators>
            </level>

            <level name="Curriculum Effectiveness">
                <indicators>
                    <indicator>Alignment with standards</indicator>
                    <indicator>Content relevance and currency</indicator>
                    <indicator>Instructional coherence</indicator>
                    <indicator>Assessment validity</indicator>
                </indicators>
            </level>

            <level name="Implementation Quality">
                <indicators>
                    <indicator>Teacher preparedness</indicator>
                    <indicator>Resource adequacy</indicator>
                    <indicator>Stakeholder satisfaction</indicator>
                    <indicator>Fidelity of implementation</indicator>
                </indicators>
            </level>
        </evaluation_levels>

        <data_collection_methods>
            <method>Student performance data</method>
            <method>Teacher surveys and interviews</method>
            <method>Classroom observations</method>
            <method>Parent and student feedback</method>
            <method>External evaluations</method>
        </data_collection_methods>

        <continuous_improvement>
            <cycle>
                <step>Collect evaluation data</step>
                <step>Analyze findings</step>
                <step>Identify improvement areas</step>
                <step>Develop action plans</step>
                <step>Implement changes</step>
                <step>Monitor results</step>
            </cycle>
        </continuous_improvement>
    </evaluation_framework>
</curriculum_design_guide>"""
    }
]

# Create all documents
for doc in documents:
    file_path = docs_dir / doc["filename"]

    if isinstance(doc["content"], dict):
        # JSON content
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(doc["content"], f, indent=2, ensure_ascii=False)
    else:
        # Text/Markdown content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])

    print(f"Created: {file_path}")

print(f"\nCreated {len(documents)} additional documents")

# Count total documents
total_docs = len(list(docs_dir.glob('*')))
print(f"Total documents in dataset: {total_docs}")