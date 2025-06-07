#!/usr/bin/env python3
"""
Script to create the remaining RAG documents to reach 40+ total documents.
"""

import json
import os
from pathlib import Path

# Define the documents directory
docs_dir = Path("rag_documents/documents")

# Additional documents to create
documents = [
    # Technology documents (6 more to reach 10 total)
    {
        "filename": "tech_07_cybersecurity.md",
        "content": """# Cybersecurity Best Practices and Threat Landscape

## Introduction
Cybersecurity involves protecting digital systems, networks, and data from cyber threats. As organizations become increasingly digital, robust cybersecurity measures are essential.

## Common Threats

### Malware
- **Viruses**: Self-replicating programs that attach to other files
- **Trojans**: Disguised malicious software
- **Ransomware**: Encrypts data and demands payment
- **Spyware**: Secretly monitors user activity

### Social Engineering
- **Phishing**: Fraudulent emails to steal credentials
- **Spear Phishing**: Targeted phishing attacks
- **Pretexting**: Creating false scenarios to gain information
- **Baiting**: Offering something enticing to spread malware

### Network Attacks
- **DDoS**: Overwhelming systems with traffic
- **Man-in-the-Middle**: Intercepting communications
- **SQL Injection**: Exploiting database vulnerabilities
- **Cross-Site Scripting (XSS)**: Injecting malicious scripts

## Security Framework

### CIA Triad
- **Confidentiality**: Protecting information from unauthorized access
- **Integrity**: Ensuring data accuracy and completeness
- **Availability**: Maintaining system accessibility

### Defense in Depth
Multiple layers of security controls:
1. Physical security
2. Network security
3. Endpoint security
4. Application security
5. Data security
6. Identity and access management

## Best Practices

### Access Control
- Principle of least privilege
- Multi-factor authentication
- Regular access reviews
- Strong password policies

### Network Security
- Firewalls and intrusion detection
- Network segmentation
- VPN for remote access
- Regular security updates

### Data Protection
- Encryption at rest and in transit
- Regular backups
- Data classification
- Secure disposal

### Incident Response
- Incident response plan
- Regular drills and testing
- Forensic capabilities
- Communication procedures

## Compliance and Regulations
- GDPR (General Data Protection Regulation)
- HIPAA (Health Insurance Portability and Accountability Act)
- SOX (Sarbanes-Oxley Act)
- PCI DSS (Payment Card Industry Data Security Standard)

## Emerging Threats
- AI-powered attacks
- IoT vulnerabilities
- Cloud security challenges
- Supply chain attacks
"""
    },
    {
        "filename": "tech_08_devops_practices.json",
        "content": {
            "title": "DevOps Practices and Culture",
            "description": "Guide to implementing DevOps methodologies and tools",
            "core_principles": {
                "collaboration": "Breaking down silos between development and operations",
                "automation": "Automating repetitive tasks and processes",
                "continuous_improvement": "Constantly optimizing processes and tools",
                "customer_focus": "Delivering value to end users quickly and reliably"
            },
            "practices": {
                "continuous_integration": {
                    "description": "Frequently integrating code changes",
                    "tools": ["Jenkins", "GitLab CI", "GitHub Actions", "Azure DevOps"],
                    "benefits": ["Early bug detection", "Reduced integration problems", "Faster feedback"]
                },
                "continuous_deployment": {
                    "description": "Automatically deploying code changes to production",
                    "requirements": ["Comprehensive testing", "Monitoring", "Rollback capabilities"],
                    "strategies": ["Blue-green deployment", "Canary releases", "Feature flags"]
                },
                "infrastructure_as_code": {
                    "description": "Managing infrastructure through code",
                    "tools": ["Terraform", "CloudFormation", "Ansible", "Puppet"],
                    "benefits": ["Version control", "Reproducibility", "Consistency"]
                },
                "monitoring_and_logging": {
                    "description": "Observing system behavior and performance",
                    "types": ["Application monitoring", "Infrastructure monitoring", "Log aggregation"],
                    "tools": ["Prometheus", "Grafana", "ELK Stack", "Datadog"]
                }
            },
            "cultural_aspects": {
                "shared_responsibility": "Everyone is responsible for the entire pipeline",
                "fail_fast": "Identify and fix problems quickly",
                "learning_culture": "Continuous learning and experimentation",
                "blameless_postmortems": "Focus on process improvement, not blame"
            }
        }
    },
    {
        "filename": "tech_09_agile_development.txt",
        "content": """Agile Software Development Methodologies

AGILE MANIFESTO

The Agile Manifesto, created in 2001, values:
- Individuals and interactions over processes and tools
- Working software over comprehensive documentation
- Customer collaboration over contract negotiation
- Responding to change over following a plan

AGILE PRINCIPLES

1. Customer satisfaction through early and continuous delivery
2. Welcome changing requirements, even late in development
3. Deliver working software frequently
4. Business people and developers must work together daily
5. Build projects around motivated individuals
6. Face-to-face conversation is the most efficient communication
7. Working software is the primary measure of progress
8. Sustainable development pace
9. Continuous attention to technical excellence
10. Simplicity - maximizing the amount of work not done
11. Self-organizing teams
12. Regular reflection and adaptation

SCRUM FRAMEWORK

Roles:
- Product Owner: Defines product vision and priorities
- Scrum Master: Facilitates process and removes impediments
- Development Team: Cross-functional team that builds the product

Events:
- Sprint Planning: Plan work for the upcoming sprint
- Daily Scrum: 15-minute daily synchronization meeting
- Sprint Review: Demonstrate completed work to stakeholders
- Sprint Retrospective: Reflect on process and identify improvements

Artifacts:
- Product Backlog: Prioritized list of features and requirements
- Sprint Backlog: Work selected for the current sprint
- Increment: Potentially shippable product increment

KANBAN METHOD

Principles:
- Visualize workflow
- Limit work in progress (WIP)
- Manage flow
- Make policies explicit
- Implement feedback loops
- Improve collaboratively

Kanban Board:
- To Do: Work items waiting to be started
- In Progress: Work currently being done
- Done: Completed work items

EXTREME PROGRAMMING (XP)

Practices:
- Pair Programming: Two developers working together
- Test-Driven Development: Write tests before code
- Continuous Integration: Frequent code integration
- Refactoring: Improving code structure without changing functionality
- Simple Design: Keep design as simple as possible
- Collective Code Ownership: Everyone can modify any code
- On-site Customer: Customer representative available to team
- Small Releases: Frequent small releases to production

LEAN SOFTWARE DEVELOPMENT

Principles:
- Eliminate waste
- Amplify learning
- Decide as late as possible
- Deliver as fast as possible
- Empower the team
- Build integrity in
- See the whole

SCALED AGILE FRAMEWORKS

SAFe (Scaled Agile Framework):
- Portfolio level: Strategic themes and epics
- Program level: Agile Release Trains (ARTs)
- Team level: Scrum/Kanban teams

LeSS (Large-Scale Scrum):
- Scaling Scrum to multiple teams
- Single Product Owner and Product Backlog
- Sprint Planning with all teams

AGILE ESTIMATION

Techniques:
- Planning Poker: Team-based estimation using cards
- T-shirt Sizing: Relative sizing (XS, S, M, L, XL)
- Story Points: Relative complexity estimation
- Ideal Days: Estimation in ideal working days

AGILE TESTING

Approaches:
- Test-Driven Development (TDD)
- Behavior-Driven Development (BDD)
- Acceptance Test-Driven Development (ATDD)
- Continuous Testing

Test Pyramid:
- Unit Tests: Fast, isolated tests
- Integration Tests: Component interaction tests
- End-to-End Tests: Full system tests

AGILE METRICS

Velocity: Amount of work completed per sprint
Burndown Charts: Work remaining over time
Cumulative Flow Diagram: Work flow visualization
Lead Time: Time from request to delivery
Cycle Time: Time from start to completion

COMMON CHALLENGES

- Resistance to change
- Lack of customer involvement
- Insufficient training
- Scaling difficulties
- Maintaining quality under pressure
- Distributed teams
- Legacy system constraints

BENEFITS OF AGILE

- Faster time to market
- Improved quality
- Better customer satisfaction
- Increased team morale
- Greater flexibility
- Reduced risk
- Better visibility and control"""
    },
    {
        "filename": "tech_10_software_architecture.md",
        "content": """# Software Architecture Patterns and Design Principles

## Introduction
Software architecture defines the high-level structure of a software system, including components, their relationships, and the principles governing their design and evolution.

## Architectural Patterns

### Layered Architecture
Organizes system into horizontal layers:
- **Presentation Layer**: User interface
- **Business Layer**: Business logic and rules
- **Persistence Layer**: Data access
- **Database Layer**: Data storage

**Pros**: Clear separation of concerns, easy to understand
**Cons**: Performance overhead, tight coupling between layers

### Microservices Architecture
Decomposes application into small, independent services:
- Each service owns its data
- Services communicate via APIs
- Independent deployment and scaling
- Technology diversity

**Pros**: Scalability, technology flexibility, fault isolation
**Cons**: Complexity, network latency, data consistency

### Event-Driven Architecture
Components communicate through events:
- **Event Producers**: Generate events
- **Event Consumers**: React to events
- **Event Channels**: Transport events

**Pros**: Loose coupling, scalability, real-time processing
**Cons**: Complex debugging, eventual consistency

### Hexagonal Architecture (Ports and Adapters)
Isolates core business logic from external concerns:
- **Core**: Business logic
- **Ports**: Interfaces for external communication
- **Adapters**: Implementations of ports

**Pros**: Testability, flexibility, independence from frameworks
**Cons**: Initial complexity, over-engineering risk

## Design Principles

### SOLID Principles

**Single Responsibility Principle (SRP)**
A class should have only one reason to change.

**Open/Closed Principle (OCP)**
Software entities should be open for extension but closed for modification.

**Liskov Substitution Principle (LSP)**
Objects of a superclass should be replaceable with objects of a subclass.

**Interface Segregation Principle (ISP)**
Clients should not be forced to depend on interfaces they don't use.

**Dependency Inversion Principle (DIP)**
High-level modules should not depend on low-level modules.

### DRY (Don't Repeat Yourself)
Avoid code duplication by abstracting common functionality.

### KISS (Keep It Simple, Stupid)
Prefer simple solutions over complex ones.

### YAGNI (You Aren't Gonna Need It)
Don't implement functionality until it's actually needed.

## Quality Attributes

### Performance
- **Throughput**: Requests processed per unit time
- **Latency**: Time to process a single request
- **Response Time**: Time from request to response

### Scalability
- **Horizontal Scaling**: Adding more servers
- **Vertical Scaling**: Adding more power to existing servers
- **Load Balancing**: Distributing requests across servers

### Reliability
- **Availability**: System uptime percentage
- **Fault Tolerance**: Ability to continue operating despite failures
- **Recovery**: Time to restore service after failure

### Security
- **Authentication**: Verifying user identity
- **Authorization**: Controlling access to resources
- **Data Protection**: Encrypting sensitive information

### Maintainability
- **Modularity**: Well-defined, independent components
- **Readability**: Clear, understandable code
- **Testability**: Easy to write and run tests

## Architectural Decision Records (ADRs)
Document important architectural decisions:
- **Context**: Situation requiring a decision
- **Decision**: The chosen solution
- **Status**: Proposed, accepted, deprecated, superseded
- **Consequences**: Positive and negative outcomes

## Technology Stack Considerations

### Frontend
- **Frameworks**: React, Angular, Vue.js
- **State Management**: Redux, MobX, Vuex
- **Build Tools**: Webpack, Vite, Parcel

### Backend
- **Languages**: Java, Python, Node.js, Go, C#
- **Frameworks**: Spring Boot, Django, Express, Gin
- **Databases**: PostgreSQL, MongoDB, Redis

### Infrastructure
- **Cloud Providers**: AWS, Azure, Google Cloud
- **Containers**: Docker, Kubernetes
- **Monitoring**: Prometheus, Grafana, ELK Stack

## Common Anti-Patterns

### Big Ball of Mud
Lack of clear architecture leading to tangled code.

### God Object
Single class that knows too much or does too much.

### Spaghetti Code
Code with complex and tangled control structure.

### Golden Hammer
Using the same solution for every problem.

## Best Practices

1. **Start Simple**: Begin with simple architecture and evolve
2. **Document Decisions**: Use ADRs to capture reasoning
3. **Consider Trade-offs**: Every decision has pros and cons
4. **Plan for Change**: Design for flexibility and evolution
5. **Measure Performance**: Use metrics to validate decisions
6. **Security by Design**: Consider security from the beginning
7. **Automate Testing**: Ensure architecture supports testing
8. **Monitor Production**: Observe system behavior in production

## Conclusion
Good software architecture balances multiple quality attributes while meeting business requirements. It requires understanding trade-offs, following proven principles, and continuously evolving based on feedback and changing needs.
"""
    },
    
    # Business documents (5 more to reach 8 total)
    {
        "filename": "business_04_supply_chain.csv",
        "content": """Stage,Process,Key Activities,Stakeholders,Metrics,Challenges,Technologies
Planning,Demand Forecasting,Historical analysis; Market research; Statistical modeling,Sales team; Marketing; Customers,Forecast accuracy; Demand variability,Seasonality; Market volatility,AI/ML algorithms; ERP systems
Planning,Supply Planning,Capacity planning; Resource allocation; Inventory optimization,Operations; Procurement; Finance,Service level; Inventory turnover,Capacity constraints; Lead time variability,Advanced planning systems; Optimization software
Sourcing,Supplier Selection,RFQ process; Vendor evaluation; Contract negotiation,Procurement; Legal; Quality,Cost savings; Supplier performance,Supplier risk; Quality issues,E-sourcing platforms; Supplier portals
Sourcing,Strategic Sourcing,Category management; Market analysis; Supplier relationship management,Category managers; Suppliers; Stakeholders,Cost reduction; Innovation,Market dynamics; Supplier consolidation,Spend analytics; Contract management
Manufacturing,Production Planning,Master production schedule; Material requirements planning; Capacity scheduling,Production; Planning; Materials,On-time delivery; Efficiency,Equipment downtime; Quality issues,MES systems; IoT sensors
Manufacturing,Quality Control,Inspection; Testing; Process monitoring; Corrective actions,Quality; Production; Engineering,Defect rate; First pass yield,Process variation; Human error,Statistical process control; Automated inspection
Logistics,Warehousing,Receiving; Storage; Picking; Packing; Shipping,Warehouse; Transportation; Customers,Order accuracy; Cycle time,Space constraints; Labor availability,WMS systems; Automation; RFID
Logistics,Transportation,Route planning; Carrier selection; Shipment tracking; Delivery,Logistics; Carriers; Customers,On-time delivery; Cost per shipment,Traffic; Weather; Fuel costs,TMS systems; GPS tracking; Route optimization
Distribution,Order Management,Order processing; Inventory allocation; Fulfillment coordination,Customer service; Warehouse; Finance,Order cycle time; Fill rate,System integration; Inventory availability,OMS systems; EDI; API integration
Distribution,Customer Service,Order status; Issue resolution; Returns processing; Communication,Customer service; Customers; Returns,Customer satisfaction; Response time,Complex inquiries; System limitations,CRM systems; Chatbots; Self-service portals
Returns,Reverse Logistics,Returns processing; Refurbishment; Disposal; Recycling,Returns; Quality; Environmental,Return rate; Recovery value,Product condition; Processing costs,Returns management systems; Tracking
Analytics,Performance Monitoring,KPI tracking; Dashboard reporting; Trend analysis; Benchmarking,Management; Operations; Finance,Cost; Service; Quality metrics,Data quality; System integration,BI tools; Analytics platforms; Real-time monitoring
Risk Management,Supply Risk,Supplier assessment; Contingency planning; Risk monitoring; Mitigation,Risk; Procurement; Business continuity,Risk exposure; Mitigation effectiveness,Supplier failures; Natural disasters,Risk management platforms; Supplier monitoring
Risk Management,Demand Risk,Market analysis; Scenario planning; Flexibility planning; Buffer management,Sales; Marketing; Planning,Forecast accuracy; Responsiveness,Market volatility; Product lifecycle,Demand sensing; Scenario modeling
Sustainability,Environmental,Carbon footprint; Waste reduction; Sustainable sourcing; Green logistics,Sustainability; Operations; Procurement,Carbon emissions; Waste reduction,Regulatory compliance; Cost implications,Carbon tracking; Lifecycle assessment
Sustainability,Social,Labor practices; Community impact; Ethical sourcing; Diversity,HR; Procurement; Community relations,Compliance rate; Community satisfaction,Supply chain visibility; Cultural differences,Supplier auditing; Certification systems
Technology,Digital Transformation,Process automation; Data analytics; AI implementation; System integration,IT; Operations; Management,ROI; Efficiency gains,Change management; Integration complexity,Cloud platforms; AI/ML; Blockchain
Technology,Data Management,Data collection; Data quality; Analytics; Reporting; Governance,IT; Analytics; Management,Data accuracy; Insights generation,Data silos; Quality issues,Data lakes; ETL tools; Master data management
Collaboration,Supplier Collaboration,Joint planning; Information sharing; Innovation partnerships; Performance improvement,Procurement; Suppliers; R&D,Innovation rate; Cost reduction,Trust; Information sharing,Collaboration platforms; Shared systems
Collaboration,Customer Collaboration,Demand collaboration; Joint forecasting; VMI; CPFR,Sales; Customers; Planning,Forecast accuracy; Service level,Information sharing; System integration,EDI; Collaboration platforms; Shared forecasting
Continuous Improvement,Process Optimization,Lean implementation; Six Sigma; Kaizen; Best practice sharing,Operations; Quality; Management,Process efficiency; Cost reduction,Change resistance; Resource allocation,Process mining; Lean tools; Project management
Continuous Improvement,Innovation,New technology adoption; Process innovation; Product innovation; Partnership innovation,R&D; Operations; Partners,Innovation pipeline; Time to market,Investment; Risk; Capability gaps,Innovation management; R&D platforms"""
    },
    {
        "filename": "business_05_leadership.md",
        "content": """# Leadership Principles and Management Best Practices

## Leadership vs Management

### Leadership
- **Vision**: Creating and communicating a compelling future
- **Inspiration**: Motivating people to achieve goals
- **Change**: Driving transformation and innovation
- **People Focus**: Developing and empowering individuals

### Management
- **Planning**: Setting objectives and creating strategies
- **Organization**: Structuring resources and processes
- **Control**: Monitoring performance and ensuring compliance
- **Efficiency**: Optimizing operations and reducing waste

## Leadership Styles

### Transformational Leadership
- Inspirational motivation
- Intellectual stimulation
- Individualized consideration
- Idealized influence

### Servant Leadership
- Putting followers first
- Empowering and developing people
- Creating value for community
- Demonstrating stewardship

### Situational Leadership
- Adapting style to situation and follower readiness
- Directing, coaching, supporting, delegating
- Assessing competence and commitment

### Authentic Leadership
- Self-awareness and genuineness
- Relational transparency
- Balanced processing
- Moral perspective

## Core Leadership Competencies

### Emotional Intelligence
- **Self-Awareness**: Understanding own emotions and impact
- **Self-Regulation**: Managing emotions and impulses
- **Motivation**: Drive to achieve and improve
- **Empathy**: Understanding others' emotions
- **Social Skills**: Managing relationships effectively

### Communication
- Active listening
- Clear and concise messaging
- Nonverbal communication
- Feedback delivery
- Difficult conversations

### Decision Making
- Problem analysis
- Alternative evaluation
- Risk assessment
- Stakeholder consideration
- Implementation planning

### Strategic Thinking
- Systems thinking
- Future orientation
- Pattern recognition
- Innovation mindset
- Competitive analysis

## Building High-Performance Teams

### Team Development Stages
1. **Forming**: Getting acquainted, establishing ground rules
2. **Storming**: Conflict and competition emerge
3. **Norming**: Cooperation and cohesion develop
4. **Performing**: High productivity and effectiveness
5. **Adjourning**: Task completion and team dissolution

### Team Effectiveness Factors
- Clear purpose and goals
- Defined roles and responsibilities
- Open communication
- Mutual trust and respect
- Complementary skills
- Shared accountability

### Psychological Safety
- Freedom to express ideas and concerns
- Learning from mistakes
- Taking calculated risks
- Asking questions without fear
- Challenging the status quo

## Change Management

### Kotter's 8-Step Process
1. Create urgency
2. Form a guiding coalition
3. Develop vision and strategy
4. Communicate the vision
5. Empower broad-based action
6. Generate short-term wins
7. Consolidate gains and produce more change
8. Anchor new approaches in culture

### ADKAR Model
- **Awareness**: Why change is needed
- **Desire**: Personal motivation to change
- **Knowledge**: How to change
- **Ability**: Skills and behaviors to change
- **Reinforcement**: Sustaining the change

### Overcoming Resistance
- Understand root causes
- Communicate benefits clearly
- Involve people in planning
- Provide training and support
- Address concerns promptly

## Performance Management

### Goal Setting (SMART)
- **Specific**: Clear and well-defined
- **Measurable**: Quantifiable outcomes
- **Achievable**: Realistic and attainable
- **Relevant**: Aligned with objectives
- **Time-bound**: Clear deadlines

### Feedback and Coaching
- Regular check-ins
- Specific and actionable feedback
- Focus on behavior and impact
- Two-way dialogue
- Development planning

### Recognition and Rewards
- Timely acknowledgment
- Meaningful recognition
- Fair and consistent rewards
- Both monetary and non-monetary
- Public and private recognition

## Delegation and Empowerment

### Effective Delegation
- Select the right person
- Define expectations clearly
- Provide necessary resources
- Set checkpoints and deadlines
- Allow autonomy in execution

### Empowerment Strategies
- Share information and context
- Involve in decision making
- Provide learning opportunities
- Encourage initiative
- Support calculated risks

## Conflict Resolution

### Conflict Sources
- Resource competition
- Goal differences
- Communication breakdowns
- Personality clashes
- Role ambiguity

### Resolution Strategies
- **Competing**: Win-lose approach
- **Accommodating**: Lose-win approach
- **Avoiding**: Lose-lose approach
- **Compromising**: Partial win-win
- **Collaborating**: Full win-win

### Mediation Process
1. Set ground rules
2. Allow each party to speak
3. Identify common interests
4. Generate options
5. Reach agreement
6. Follow up

## Ethical Leadership

### Ethical Principles
- Integrity and honesty
- Fairness and justice
- Respect for others
- Responsibility and accountability
- Transparency

### Ethical Decision Making
1. Identify the ethical issue
2. Gather relevant information
3. Consider stakeholders
4. Evaluate alternatives
5. Choose best course of action
6. Implement and monitor

## Developing Others

### Mentoring
- Share knowledge and experience
- Provide guidance and support
- Create learning opportunities
- Offer honest feedback
- Build confidence

### Succession Planning
- Identify key positions
- Assess talent pipeline
- Develop high-potential employees
- Create development plans
- Ensure knowledge transfer

## Leading in Crisis

### Crisis Leadership Principles
- Communicate frequently and transparently
- Make decisions quickly with available information
- Show empathy and compassion
- Maintain calm and confidence
- Focus on what can be controlled

### Crisis Communication
- Acknowledge the situation
- Express concern for stakeholders
- Explain actions being taken
- Provide regular updates
- Be honest about uncertainties

## Continuous Learning

### Personal Development
- Self-reflection and assessment
- Seeking feedback
- Reading and research
- Formal education and training
- Learning from failures

### Learning Organization
- Encourage experimentation
- Share knowledge and best practices
- Learn from mistakes
- Adapt to changing conditions
- Invest in employee development

## Conclusion
Effective leadership requires a combination of skills, behaviors, and mindsets that can be developed over time. Great leaders inspire others, drive results, and create positive organizational cultures that enable sustained success.
"""
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
