#!/usr/bin/env python3
"""
Script to create additional RAG documents for the dataset.
This will create documents across different domains and formats.
"""

import json
import os
from pathlib import Path

# Define the documents directory
docs_dir = Path("rag_documents/documents")

# Technology documents
tech_docs = [
    {
        "filename": "tech_04_api_design.md",
        "content": """# RESTful API Design Best Practices

## Introduction
REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs are widely used for web services due to their simplicity and scalability.

## Core Principles

### 1. Stateless
Each request must contain all information needed to process it. The server should not store client context between requests.

### 2. Client-Server Architecture
Clear separation between client and server responsibilities.

### 3. Cacheable
Responses should be cacheable when appropriate to improve performance.

### 4. Uniform Interface
Consistent interface design across the API.

## HTTP Methods

- **GET**: Retrieve data (idempotent, safe)
- **POST**: Create new resources
- **PUT**: Update/replace entire resource (idempotent)
- **PATCH**: Partial update of resource
- **DELETE**: Remove resource (idempotent)

## URL Design

### Resource Naming
- Use nouns, not verbs: `/users` not `/getUsers`
- Use plural nouns: `/users` not `/user`
- Hierarchical structure: `/users/123/orders`

### Examples
```
GET /api/v1/users          # Get all users
GET /api/v1/users/123      # Get specific user
POST /api/v1/users         # Create new user
PUT /api/v1/users/123      # Update user
DELETE /api/v1/users/123   # Delete user
```

## Status Codes

### Success (2xx)
- 200 OK: Successful GET, PUT, PATCH
- 201 Created: Successful POST
- 204 No Content: Successful DELETE

### Client Error (4xx)
- 400 Bad Request: Invalid request
- 401 Unauthorized: Authentication required
- 403 Forbidden: Access denied
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Validation errors

### Server Error (5xx)
- 500 Internal Server Error: Generic server error
- 503 Service Unavailable: Server overloaded

## Response Format

### JSON Structure
```json
{
  "data": {
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com"
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "1.0"
  }
}
```

### Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

## Pagination

### Offset-based
```
GET /api/v1/users?offset=20&limit=10
```

### Cursor-based
```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=10
```

## Filtering and Sorting

```
GET /api/v1/users?status=active&sort=created_at&order=desc
```

## Versioning

### URL Versioning
```
GET /api/v1/users
GET /api/v2/users
```

### Header Versioning
```
GET /api/users
Accept: application/vnd.api+json;version=1
```

## Security

### Authentication
- API Keys
- JWT Tokens
- OAuth 2.0

### Authorization
- Role-based access control
- Resource-level permissions

### HTTPS
Always use HTTPS in production.

## Documentation

### OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Get all users
      responses:
        '200':
          description: Successful response
```

## Rate Limiting

### Headers
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1640995200
```

## Best Practices

1. Use consistent naming conventions
2. Implement proper error handling
3. Provide comprehensive documentation
4. Use appropriate HTTP status codes
5. Implement caching strategies
6. Monitor API performance
7. Version your APIs
8. Validate input data
9. Use HTTPS
10. Implement rate limiting
"""
    },
    {
        "filename": "tech_05_docker_containers.json",
        "content": {
            "title": "Docker Containerization Guide",
            "version": "1.0",
            "sections": {
                "introduction": {
                    "description": "Docker is a platform for developing, shipping, and running applications using containerization technology.",
                    "benefits": [
                        "Consistent environments across development, testing, and production",
                        "Improved resource utilization",
                        "Faster deployment and scaling",
                        "Simplified dependency management"
                    ]
                },
                "core_concepts": {
                    "image": "Read-only template used to create containers",
                    "container": "Running instance of an image",
                    "dockerfile": "Text file with instructions to build an image",
                    "registry": "Storage and distribution system for Docker images"
                },
                "dockerfile_example": {
                    "content": "FROM node:16-alpine\nWORKDIR /app\nCOPY package*.json ./\nRUN npm ci --only=production\nCOPY . .\nEXPOSE 3000\nCMD [\"npm\", \"start\"]",
                    "explanation": "Multi-stage build for Node.js application"
                },
                "commands": {
                    "build": "docker build -t myapp:latest .",
                    "run": "docker run -d -p 3000:3000 myapp:latest",
                    "list": "docker ps",
                    "logs": "docker logs container_id",
                    "exec": "docker exec -it container_id /bin/bash"
                },
                "best_practices": [
                    "Use official base images",
                    "Minimize layer count",
                    "Use .dockerignore file",
                    "Don't run as root user",
                    "Use multi-stage builds",
                    "Keep images small",
                    "Use specific tags, not 'latest'",
                    "Implement health checks"
                ]
            }
        }
    }
]

# Business documents
business_docs = [
    {
        "filename": "business_02_project_management.md",
        "content": """# Project Management Methodologies and Best Practices

## Introduction
Project management is the application of knowledge, skills, tools, and techniques to project activities to meet project requirements. Effective project management ensures projects are completed on time, within budget, and to the required quality standards.

## Project Management Methodologies

### Waterfall
Sequential approach with distinct phases:
1. Requirements gathering
2. Design
3. Implementation
4. Testing
5. Deployment
6. Maintenance

**Pros**: Clear structure, well-documented, predictable
**Cons**: Inflexible, late testing, assumes stable requirements

### Agile
Iterative approach emphasizing collaboration and adaptability:
- Short iterations (sprints)
- Regular customer feedback
- Adaptive planning
- Cross-functional teams

**Frameworks**: Scrum, Kanban, Extreme Programming (XP)

### Scrum
Agile framework with specific roles and ceremonies:
- **Roles**: Product Owner, Scrum Master, Development Team
- **Events**: Sprint Planning, Daily Standups, Sprint Review, Retrospective
- **Artifacts**: Product Backlog, Sprint Backlog, Increment

### Kanban
Visual workflow management:
- Kanban board with columns (To Do, In Progress, Done)
- Work-in-progress (WIP) limits
- Continuous flow
- Pull-based system

## Project Lifecycle

### Initiation
- Define project charter
- Identify stakeholders
- Conduct feasibility study
- Establish project goals

### Planning
- Create work breakdown structure (WBS)
- Develop project schedule
- Estimate resources and costs
- Identify risks
- Create communication plan

### Execution
- Coordinate people and resources
- Manage stakeholder expectations
- Implement quality assurance
- Monitor progress

### Monitoring and Control
- Track project performance
- Manage changes
- Control scope, schedule, and budget
- Report status to stakeholders

### Closure
- Complete final deliverables
- Release project resources
- Document lessons learned
- Celebrate success

## Key Project Management Areas

### Scope Management
- Define project boundaries
- Create detailed requirements
- Manage scope changes
- Prevent scope creep

### Time Management
- Create realistic schedules
- Identify critical path
- Monitor progress
- Manage dependencies

### Cost Management
- Estimate project costs
- Create budget
- Track expenses
- Control costs

### Quality Management
- Define quality standards
- Implement quality assurance
- Perform quality control
- Continuous improvement

### Risk Management
- Identify potential risks
- Assess probability and impact
- Develop mitigation strategies
- Monitor and control risks

### Communication Management
- Identify stakeholders
- Plan communication methods
- Distribute information
- Manage stakeholder engagement

## Tools and Techniques

### Project Management Software
- Microsoft Project
- Jira
- Asana
- Trello
- Monday.com

### Estimation Techniques
- Expert judgment
- Analogous estimating
- Parametric estimating
- Three-point estimating
- Planning poker (Agile)

### Scheduling Tools
- Gantt charts
- Network diagrams
- Critical path method (CPM)
- Program evaluation and review technique (PERT)

## Success Factors

### Leadership
- Clear vision and direction
- Strong communication skills
- Decision-making ability
- Team motivation

### Team Management
- Right skills and experience
- Clear roles and responsibilities
- Effective collaboration
- Regular feedback

### Stakeholder Engagement
- Identify all stakeholders
- Understand their needs
- Regular communication
- Manage expectations

### Change Management
- Establish change control process
- Assess impact of changes
- Communicate changes effectively
- Update project documents

## Common Challenges

### Scope Creep
- Unclear requirements
- Poor change control
- Stakeholder pressure
- Inadequate documentation

### Resource Constraints
- Limited budget
- Skill shortages
- Competing priorities
- External dependencies

### Communication Issues
- Poor stakeholder engagement
- Inadequate reporting
- Cultural differences
- Remote team challenges

## Best Practices

1. Define clear project objectives
2. Engage stakeholders early and often
3. Create realistic schedules and budgets
4. Implement robust change control
5. Monitor progress regularly
6. Communicate effectively
7. Learn from past projects
8. Celebrate milestones and success
9. Document lessons learned
10. Invest in team development

## Conclusion
Successful project management requires a combination of methodology, tools, and soft skills. Choose the right approach for your project context, engage stakeholders effectively, and maintain focus on delivering value to the organization.
"""
    }
]

# Science documents
science_docs = [
    {
        "filename": "science_02_quantum_computing.txt",
        "content": """Quantum Computing: Principles and Applications

INTRODUCTION

Quantum computing represents a revolutionary approach to computation that leverages quantum mechanical phenomena to process information. Unlike classical computers that use bits (0 or 1), quantum computers use quantum bits (qubits) that can exist in superposition states, enabling exponentially more powerful computation for certain problems.

QUANTUM MECHANICS FUNDAMENTALS

Superposition:
A quantum system can exist in multiple states simultaneously until measured. A qubit can be in a combination of |0⟩ and |1⟩ states, represented as α|0⟩ + β|1⟩ where α and β are complex probability amplitudes.

Entanglement:
Quantum particles can be correlated in such a way that the quantum state of each particle cannot be described independently. Measuring one particle instantly affects the state of its entangled partner, regardless of distance.

Quantum Interference:
Quantum states can interfere constructively or destructively, allowing quantum algorithms to amplify correct answers and cancel out wrong ones.

QUANTUM COMPUTING PRINCIPLES

Qubits:
The fundamental unit of quantum information. Physical implementations include:
- Superconducting circuits
- Trapped ions
- Photons
- Quantum dots
- Topological qubits

Quantum Gates:
Operations that manipulate qubits, analogous to logic gates in classical computing:
- Pauli-X gate (quantum NOT)
- Hadamard gate (creates superposition)
- CNOT gate (creates entanglement)
- Phase gates
- Rotation gates

Quantum Circuits:
Sequences of quantum gates that perform quantum algorithms. Circuits are represented as diagrams showing the flow of qubits through various gates.

QUANTUM ALGORITHMS

Shor's Algorithm:
Efficiently factors large integers, threatening current RSA encryption. Provides exponential speedup over classical factoring algorithms.

Grover's Algorithm:
Searches unsorted databases quadratically faster than classical algorithms. Reduces search time from O(N) to O(√N).

Quantum Fourier Transform:
Quantum version of the discrete Fourier transform, used in many quantum algorithms including Shor's algorithm.

Variational Quantum Eigensolver (VQE):
Hybrid quantum-classical algorithm for finding ground state energies of molecules, useful for drug discovery and materials science.

Quantum Approximate Optimization Algorithm (QAOA):
Solves combinatorial optimization problems, potentially useful for logistics, finance, and machine learning.

QUANTUM HARDWARE

Superconducting Qubits:
- Used by IBM, Google, Rigetti
- Operate at millikelvin temperatures
- Fast gate operations
- Relatively short coherence times

Trapped Ion Systems:
- Used by IonQ, Honeywell
- High-fidelity operations
- Longer coherence times
- Slower gate operations

Photonic Systems:
- Room temperature operation
- Natural for quantum communication
- Challenges with deterministic operations

Quantum Error Correction:
Essential for fault-tolerant quantum computing:
- Surface codes
- Stabilizer codes
- Logical qubits from physical qubits
- Error syndrome detection

APPLICATIONS

Cryptography:
- Breaking current encryption (Shor's algorithm)
- Quantum key distribution
- Post-quantum cryptography development

Drug Discovery:
- Molecular simulation
- Protein folding prediction
- Drug-target interaction modeling

Materials Science:
- Catalyst design
- Superconductor research
- Battery technology

Financial Modeling:
- Portfolio optimization
- Risk analysis
- Fraud detection
- High-frequency trading

Machine Learning:
- Quantum neural networks
- Quantum support vector machines
- Quantum principal component analysis

CURRENT LIMITATIONS

Quantum Decoherence:
Quantum states are fragile and easily disrupted by environmental noise, limiting computation time.

Error Rates:
Current quantum computers have high error rates, requiring error correction for practical applications.

Limited Qubit Count:
Current systems have dozens to hundreds of qubits, but many applications require thousands or millions.

Classical Simulation:
Many quantum algorithms can still be simulated classically for small problem sizes.

QUANTUM ADVANTAGE

Quantum Supremacy:
Demonstration that a quantum computer can solve a problem that is intractable for classical computers. Google claimed this in 2019 with their Sycamore processor.

Practical Quantum Advantage:
When quantum computers solve real-world problems faster than classical computers. This remains an active area of research.

PROGRAMMING QUANTUM COMPUTERS

Quantum Programming Languages:
- Qiskit (IBM)
- Cirq (Google)
- Q# (Microsoft)
- PennyLane (Xanadu)

Quantum Development Platforms:
- IBM Quantum Experience
- Google Quantum AI
- Microsoft Azure Quantum
- Amazon Braket

FUTURE OUTLOOK

Near-term Applications (NISQ era):
Noisy Intermediate-Scale Quantum devices may provide advantages for specific optimization and simulation problems.

Long-term Vision:
Fault-tolerant quantum computers could revolutionize computing, enabling breakthroughs in science, cryptography, and artificial intelligence.

Timeline Predictions:
- 2020s: NISQ applications and quantum advantage demonstrations
- 2030s: Early fault-tolerant systems
- 2040s+: Large-scale quantum computers

CHALLENGES AND RESEARCH DIRECTIONS

Technical Challenges:
- Improving qubit coherence times
- Reducing error rates
- Scaling to larger systems
- Developing error correction codes

Algorithmic Research:
- Finding new quantum algorithms
- Hybrid quantum-classical approaches
- Quantum machine learning
- Quantum simulation methods

CONCLUSION

Quantum computing represents a paradigm shift in computation with the potential to solve previously intractable problems. While significant technical challenges remain, rapid progress in hardware, algorithms, and software is bringing practical quantum computing closer to reality. The field requires continued investment in research and development to realize its transformative potential."""
    }
]

# Create all documents
all_docs = tech_docs + business_docs + science_docs

for doc in all_docs:
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

print(f"\nCreated {len(all_docs)} additional documents")
