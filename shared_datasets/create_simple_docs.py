#!/usr/bin/env python3
"""
Simple script to create additional documents.
"""

import json
from pathlib import Path

docs_dir = Path("rag_documents/documents")

# Science documents
science_content = """Neuroscience and Brain Function

INTRODUCTION TO NEUROSCIENCE

Neuroscience is the scientific study of the nervous system, including the brain, spinal cord, and peripheral nerves. It encompasses multiple disciplines including biology, psychology, chemistry, physics, and medicine.

BRAIN STRUCTURE AND FUNCTION

Cerebrum:
- Largest part of the brain
- Divided into left and right hemispheres
- Contains cerebral cortex (gray matter)
- Responsible for higher-order thinking

Cerebellum:
- Located at back of brain
- Coordinates movement and balance
- Involved in motor learning
- Contains more neurons than rest of brain

Brainstem:
- Connects brain to spinal cord
- Controls vital functions (breathing, heart rate)
- Includes medulla, pons, midbrain
- Regulates sleep-wake cycles

NEURONS AND SYNAPSES

Neuron Structure:
- Cell body (soma): Contains nucleus
- Dendrites: Receive signals
- Axon: Transmits signals
- Synapses: Connections between neurons

Neurotransmitters:
- Dopamine: Reward and motivation
- Serotonin: Mood regulation
- Acetylcholine: Memory and learning
- GABA: Inhibitory neurotransmitter

BRAIN PLASTICITY

Neuroplasticity:
- Brain's ability to reorganize
- Forms new neural connections
- Occurs throughout life
- Enhanced by learning and experience

Types of Plasticity:
- Structural: Changes in brain anatomy
- Functional: Changes in neural activity
- Synaptic: Strengthening/weakening connections

COGNITIVE FUNCTIONS

Memory:
- Working memory: Temporary storage
- Long-term memory: Permanent storage
- Episodic: Personal experiences
- Semantic: General knowledge

Learning:
- Associative learning: Classical/operant conditioning
- Observational learning: Learning by watching
- Procedural learning: Motor skills
- Declarative learning: Facts and events

NEUROSCIENCE RESEARCH METHODS

Brain Imaging:
- fMRI: Functional magnetic resonance imaging
- PET: Positron emission tomography
- EEG: Electroencephalography
- MEG: Magnetoencephalography

Experimental Techniques:
- Lesion studies: Brain damage effects
- Stimulation: Electrical/magnetic stimulation
- Single-cell recording: Individual neuron activity
- Optogenetics: Light-controlled neurons

NEUROLOGICAL DISORDERS

Alzheimer's Disease:
- Progressive memory loss
- Amyloid plaques and tau tangles
- Affects 50+ million worldwide
- No current cure

Parkinson's Disease:
- Movement disorder
- Loss of dopamine neurons
- Tremor, rigidity, bradykinesia
- Treated with L-DOPA

Depression:
- Mood disorder
- Altered neurotransmitter function
- Affects 300+ million worldwide
- Treated with therapy and medication

FUTURE DIRECTIONS

Brain-Computer Interfaces:
- Direct communication between brain and computers
- Applications in paralysis and prosthetics
- Ethical considerations about privacy

Artificial Intelligence:
- Neural networks inspired by brain
- Machine learning and deep learning
- Potential for understanding cognition

Precision Medicine:
- Personalized treatments based on genetics
- Biomarkers for early diagnosis
- Targeted therapies for brain disorders"""

# Legal document
legal_content = """Employment Law Fundamentals

INTRODUCTION TO EMPLOYMENT LAW

Employment law governs the relationship between employers and employees, covering hiring, workplace conditions, compensation, and termination. It includes federal, state, and local regulations.

AT-WILL EMPLOYMENT

Definition:
Employment relationship can be terminated by either party at any time, for any reason, or no reason at all, without advance notice.

Exceptions:
- Public policy violations
- Implied contracts
- Covenant of good faith and fair dealing
- Statutory protections

EQUAL EMPLOYMENT OPPORTUNITY

Title VII (1964):
- Prohibits discrimination based on race, color, religion, sex, national origin
- Applies to employers with 15+ employees
- Covers hiring, firing, promotion, compensation
- Enforced by EEOC

Americans with Disabilities Act (ADA):
- Prohibits discrimination against qualified individuals with disabilities
- Requires reasonable accommodations
- Applies to employers with 15+ employees
- Covers physical and mental impairments

Age Discrimination in Employment Act (ADEA):
- Protects individuals 40 years and older
- Applies to employers with 20+ employees
- Prohibits age-based discrimination in employment decisions

WAGE AND HOUR LAWS

Fair Labor Standards Act (FLSA):
- Establishes minimum wage requirements
- Requires overtime pay (1.5x regular rate for 40+ hours)
- Regulates child labor
- Distinguishes exempt vs. non-exempt employees

Exempt Employees:
- Executive, administrative, professional positions
- Paid on salary basis
- Not entitled to overtime pay
- Must meet specific duties tests

WORKPLACE SAFETY

Occupational Safety and Health Act (OSHA):
- Ensures safe and healthy working conditions
- Requires employers to provide hazard-free workplace
- Establishes safety standards and regulations
- Provides for inspections and penalties

Workers' Compensation:
- State-mandated insurance for work-related injuries
- Provides medical benefits and wage replacement
- No-fault system (regardless of who caused injury)
- Exclusive remedy (prevents lawsuits in most cases)

FAMILY AND MEDICAL LEAVE

Family and Medical Leave Act (FMLA):
- Provides up to 12 weeks unpaid leave
- For birth/adoption, serious health condition, military family leave
- Applies to employers with 50+ employees
- Job protection and health insurance continuation

State Leave Laws:
- Many states provide additional leave benefits
- Paid family leave programs
- Expanded coverage and duration
- Broader definitions of family

EMPLOYEE PRIVACY

Electronic Communications:
- Employer monitoring of email and internet use
- Reasonable expectation of privacy
- Company policies and consent
- State law variations

Drug Testing:
- Pre-employment testing generally permitted
- Random testing varies by state and industry
- Safety-sensitive positions have broader testing rights
- Medical marijuana considerations

TERMINATION AND SEVERANCE

Wrongful Termination:
- Termination that violates law or public policy
- Breach of employment contract
- Discrimination or retaliation
- Violation of implied covenant

Severance Agreements:
- Not required by law (except in limited circumstances)
- Often includes release of claims
- May include non-compete or non-disclosure provisions
- Consideration requirements

LABOR RELATIONS

National Labor Relations Act (NLRA):
- Protects right to organize and bargain collectively
- Prohibits unfair labor practices
- Covers private sector employees
- Administered by NLRB

Collective Bargaining:
- Negotiation between union and employer
- Covers wages, hours, working conditions
- Results in collective bargaining agreement
- Grievance and arbitration procedures

EMERGING ISSUES

Gig Economy:
- Classification of workers (employee vs. independent contractor)
- Benefits and protections for gig workers
- State legislation (e.g., California AB5)
- Federal regulatory developments

Remote Work:
- Wage and hour compliance across state lines
- Workers' compensation coverage
- Privacy and monitoring issues
- Accommodation requirements

Artificial Intelligence:
- AI in hiring and employment decisions
- Bias and discrimination concerns
- Transparency and explainability requirements
- Regulatory developments

COMPLIANCE BEST PRACTICES

Policies and Procedures:
- Written employment policies
- Regular updates to reflect law changes
- Employee training and communication
- Consistent enforcement

Documentation:
- Maintain accurate employment records
- Document performance issues and disciplinary actions
- Preserve records for required retention periods
- Protect confidential information

Training:
- Manager training on employment law compliance
- Anti-harassment and discrimination training
- Safety training and procedures
- Regular updates on legal developments"""

# Educational document
education_content = """Assessment and Evaluation in Education

INTRODUCTION TO EDUCATIONAL ASSESSMENT

Educational assessment is the systematic process of gathering, analyzing, and interpreting evidence about student learning to make informed decisions about instruction and student progress.

TYPES OF ASSESSMENT

Formative Assessment:
- Ongoing evaluation during learning process
- Provides immediate feedback to students and teachers
- Helps adjust instruction in real-time
- Examples: exit tickets, quizzes, observations

Summative Assessment:
- Evaluation at end of instructional period
- Measures achievement of learning objectives
- Used for grading and reporting
- Examples: final exams, standardized tests, projects

Diagnostic Assessment:
- Identifies student strengths and weaknesses
- Conducted before instruction begins
- Helps plan appropriate instruction
- Examples: pre-tests, placement tests

ASSESSMENT METHODS

Traditional Assessments:
- Multiple choice questions
- True/false questions
- Short answer responses
- Essay questions

Performance-Based Assessments:
- Authentic tasks and real-world applications
- Portfolios and projects
- Presentations and demonstrations
- Laboratory experiments

Alternative Assessments:
- Peer assessment
- Self-assessment
- Observational checklists
- Learning journals

VALIDITY AND RELIABILITY

Validity:
- Content validity: Assessment measures intended content
- Construct validity: Assessment measures intended construct
- Criterion validity: Assessment predicts future performance
- Face validity: Assessment appears to measure what it claims

Reliability:
- Consistency of assessment results
- Test-retest reliability: Consistent results over time
- Inter-rater reliability: Consistent scoring across raters
- Internal consistency: Items measure same construct

RUBRICS AND SCORING

Holistic Rubrics:
- Single score for overall performance
- General descriptions of performance levels
- Quick and efficient scoring
- Less detailed feedback

Analytic Rubrics:
- Separate scores for different criteria
- Detailed descriptions for each criterion
- More specific feedback
- Takes longer to score

Scoring Considerations:
- Clear performance criteria
- Specific descriptors for each level
- Consistent application across students
- Regular calibration among raters

STANDARDIZED TESTING

Norm-Referenced Tests:
- Compare student performance to peer group
- Results reported as percentiles or standard scores
- Used for ranking and selection
- Examples: SAT, ACT, IQ tests

Criterion-Referenced Tests:
- Compare performance to predetermined standards
- Results indicate mastery of specific skills
- Used for certification and accountability
- Examples: state achievement tests, licensing exams

High-Stakes Testing:
- Results have significant consequences
- Used for graduation, promotion, school accountability
- Can lead to teaching to the test
- Requires careful consideration of validity and fairness

GRADING AND REPORTING

Grading Systems:
- Letter grades (A, B, C, D, F)
- Numerical grades (0-100)
- Pass/fail systems
- Standards-based grading

Grade Calculation:
- Weighted averages
- Points-based systems
- Category-based grading
- Most recent evidence

Reporting Methods:
- Traditional report cards
- Standards-based report cards
- Portfolios
- Conferences and narratives

TECHNOLOGY IN ASSESSMENT

Computer-Based Testing:
- Immediate scoring and feedback
- Adaptive testing capabilities
- Multimedia question types
- Reduced paper and administrative costs

Online Assessment Tools:
- Learning management systems
- Clicker systems for real-time feedback
- Digital portfolios
- Automated essay scoring

Data Analytics:
- Learning analytics and educational data mining
- Predictive modeling for student success
- Personalized learning recommendations
- Early warning systems

ASSESSMENT FOR DIVERSE LEARNERS

English Language Learners:
- Language considerations in assessment
- Accommodations and modifications
- Native language assessments
- Cultural responsiveness

Students with Disabilities:
- Individualized Education Program (IEP) considerations
- Accommodations vs. modifications
- Alternative assessments
- Universal Design for Learning principles

Cultural Considerations:
- Bias in assessment instruments
- Culturally responsive assessment practices
- Multiple ways of demonstrating knowledge
- Community and family involvement

ETHICAL CONSIDERATIONS

Fairness:
- Equal opportunity to demonstrate learning
- Appropriate accommodations
- Bias-free assessment instruments
- Transparent scoring criteria

Privacy:
- Confidentiality of student records
- Secure storage and transmission of data
- Student and parent rights
- FERPA compliance

Professional Responsibility:
- Competent assessment practices
- Appropriate use of assessment results
- Ongoing professional development
- Collaboration with colleagues

ASSESSMENT LITERACY

For Teachers:
- Understanding assessment principles
- Developing quality assessments
- Interpreting and using results
- Communicating with stakeholders

For Students:
- Understanding assessment criteria
- Self-assessment skills
- Goal setting and reflection
- Test-taking strategies

For Parents:
- Understanding assessment results
- Supporting learning at home
- Communicating with teachers
- Advocating for appropriate assessment

FUTURE TRENDS

Competency-Based Assessment:
- Focus on mastery rather than time
- Flexible pacing and pathways
- Multiple opportunities to demonstrate learning
- Personalized learning approaches

Authentic Assessment:
- Real-world applications
- Performance in natural settings
- Integration of knowledge and skills
- Meaningful and relevant tasks

Continuous Assessment:
- Ongoing monitoring of learning
- Real-time feedback and adjustment
- Seamless integration with instruction
- Technology-enabled data collection"""

# Create the documents
docs = [
    ("science_05_neuroscience.txt", science_content),
    ("legal_04_employment_law.txt", legal_content),
    ("education_04_assessment.txt", education_content)
]

for filename, content in docs:
    file_path = docs_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {file_path}")

# Count total documents
total_docs = len(list(docs_dir.glob('*')))
print(f"\nTotal documents in dataset: {total_docs}")
