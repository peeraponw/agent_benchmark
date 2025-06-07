"""
Shared Dataset Manager for AI Agent Framework Comparison.

This module provides the core dataset management functionality for loading,
validating, and managing test datasets across all AI agent frameworks.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class DifficultyLevel(str, Enum):
    """Enumeration for dataset item difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    CREATIVE = "creative"


class DatasetItem(BaseModel):
    """
    Core data model for individual dataset items.
    
    This model provides a standardized structure for all types of test data
    across different evaluation scenarios (Q&A, RAG, multi-agent, etc.).
    """
    
    id: str = Field(
        ...,
        description="Unique identifier for the dataset item",
        min_length=1,
        max_length=100
    )
    
    input_data: Any = Field(
        ...,
        description="Input data for the test case - can be question, query, scenario, etc."
    )
    
    expected_output: Any = Field(
        ...,
        description="Expected output or ground truth for evaluation"
    )
    
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context and metadata for the dataset item"
    )
    
    difficulty_level: Optional[DifficultyLevel] = Field(
        None,
        description="Difficulty level categorization"
    )
    
    category: Optional[str] = Field(
        None,
        description="Category or type classification for grouping",
        max_length=50
    )
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Validate that ID follows expected format."""
        if not v or not isinstance(v, str):
            raise ValueError("ID must be a non-empty string")

        # Check for valid ID format (alphanumeric with underscores)
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError("ID must contain only alphanumeric characters, underscores, and hyphens")

        return v

    @field_validator('metadata')
    @classmethod
    def validate_metadata(cls, v):
        """Ensure metadata is a valid dictionary."""
        if not isinstance(v, dict):
            raise ValueError("Metadata must be a dictionary")
        return v

    @model_validator(mode='after')
    def validate_consistency(self):
        """Validate consistency between fields."""
        # Ensure input_data and expected_output are not None
        if self.input_data is None:
            raise ValueError("input_data cannot be None")

        if self.expected_output is None:
            raise ValueError("expected_output cannot be None")

        return self
    
    class Config:
        """Pydantic model configuration."""
        use_enum_values = True
        validate_assignment = True
        extra = "forbid"  # Prevent additional fields
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DatasetItem':
        """Create a DatasetItem from a dictionary."""
        return cls(**data)


class DatasetManager:
    """
    Core dataset management class for loading and managing test datasets.
    
    This class provides centralized access to all shared datasets used for
    evaluating AI agent frameworks, ensuring consistency and standardization.
    """
    
    def __init__(self, dataset_path: Union[str, Path]):
        """
        Initialize the DatasetManager.
        
        Args:
            dataset_path: Path to the root directory containing datasets
        """
        self.dataset_path = Path(dataset_path)
        self._setup_logging()
        self._validate_dataset_path()
    
    def _setup_logging(self) -> None:
        """Set up logging for dataset operations."""
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _validate_dataset_path(self) -> None:
        """Validate that the dataset path exists and is accessible."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset path does not exist: {self.dataset_path}")
        
        if not self.dataset_path.is_dir():
            raise NotADirectoryError(f"Dataset path is not a directory: {self.dataset_path}")
        
        self.logger.info(f"DatasetManager initialized with path: {self.dataset_path}")
    
    @property
    def dataset_path(self) -> Path:
        """Get the dataset path."""
        return self._dataset_path
    
    @dataset_path.setter
    def dataset_path(self, value: Union[str, Path]) -> None:
        """Set the dataset path with validation."""
        self._dataset_path = Path(value).resolve()
    
    def _load_json_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load and parse a JSON file safely.
        
        Args:
            file_path: Path to the JSON file
            
        Returns:
            List of dictionaries from the JSON file
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError(f"Expected list in JSON file, got {type(data)}")
            
            self.logger.info(f"Successfully loaded {len(data)} items from {file_path}")
            return data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in file {file_path}: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error loading file {file_path}: {e}")
            raise
    
    def _save_json_file(self, data: List[Dict[str, Any]], file_path: Path) -> None:
        """
        Save data to a JSON file safely.
        
        Args:
            data: List of dictionaries to save
            file_path: Path where to save the file
        """
        try:
            # Create backup if file exists
            if file_path.exists():
                backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
                file_path.rename(backup_path)
                self.logger.info(f"Created backup: {backup_path}")
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the data
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Successfully saved {len(data)} items to {file_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving file {file_path}: {e}")
            raise

    def load_qa_dataset(self) -> List[DatasetItem]:
        """
        Load standardized Q&A test data.

        Returns:
            List of DatasetItem objects containing Q&A pairs

        Raises:
            FileNotFoundError: If Q&A files don't exist
            ValueError: If data validation fails
        """
        qa_dir = self.dataset_path / "qa"
        questions_file = qa_dir / "questions.json"
        answers_file = qa_dir / "answers.json"

        # Load questions and answers
        questions_data = self._load_json_file(questions_file)
        answers_data = self._load_json_file(answers_file)

        # Create lookup dictionary for answers
        answers_lookup = {item['id']: item for item in answers_data}

        dataset_items = []

        for question_item in questions_data:
            question_id = question_item.get('id')

            if not question_id:
                self.logger.warning("Question item missing ID, skipping")
                continue

            if question_id not in answers_lookup:
                self.logger.warning(f"No answer found for question ID: {question_id}")
                continue

            answer_item = answers_lookup[question_id]

            # Create DatasetItem
            try:
                dataset_item = DatasetItem(
                    id=question_id,
                    input_data={
                        "question": question_item.get('question'),
                        "expected_response_type": question_item.get('expected_response_type')
                    },
                    expected_output={
                        "answer": answer_item.get('answer'),
                        "explanation": answer_item.get('explanation'),
                        "sources": answer_item.get('sources', []),
                        "confidence": answer_item.get('confidence', 1.0)
                    },
                    metadata={
                        "question_type": question_item.get('category'),
                        "response_type": question_item.get('expected_response_type'),
                        "sources": answer_item.get('sources', []),
                        "confidence": answer_item.get('confidence', 1.0)
                    },
                    difficulty_level=question_item.get('difficulty'),
                    category=question_item.get('category')
                )

                dataset_items.append(dataset_item)

            except Exception as e:
                self.logger.error(f"Error creating DatasetItem for {question_id}: {e}")
                continue

        self.logger.info(f"Successfully loaded {len(dataset_items)} Q&A dataset items")
        return dataset_items

    def save_qa_dataset(self, items: List[DatasetItem]) -> None:
        """
        Save Q&A dataset items to structured JSON format.

        Args:
            items: List of DatasetItem objects to save

        Raises:
            ValueError: If items are invalid
        """
        if not items:
            raise ValueError("Cannot save empty dataset")

        qa_dir = self.dataset_path / "qa"
        questions_file = qa_dir / "questions.json"
        answers_file = qa_dir / "answers.json"

        questions_data = []
        answers_data = []

        for item in items:
            # Validate item
            if not isinstance(item, DatasetItem):
                raise ValueError(f"Expected DatasetItem, got {type(item)}")

            # Extract question data
            input_data = item.input_data
            if isinstance(input_data, dict):
                question_entry = {
                    "id": item.id,
                    "question": input_data.get("question"),
                    "category": item.category,
                    "difficulty": item.difficulty_level,
                    "expected_response_type": input_data.get("expected_response_type")
                }
            else:
                # Handle simple string input
                question_entry = {
                    "id": item.id,
                    "question": str(input_data),
                    "category": item.category,
                    "difficulty": item.difficulty_level,
                    "expected_response_type": "text"
                }

            questions_data.append(question_entry)

            # Extract answer data
            expected_output = item.expected_output
            if isinstance(expected_output, dict):
                answer_entry = {
                    "id": item.id,
                    "answer": expected_output.get("answer"),
                    "explanation": expected_output.get("explanation"),
                    "sources": expected_output.get("sources", []),
                    "confidence": expected_output.get("confidence", 1.0)
                }
            else:
                # Handle simple string output
                answer_entry = {
                    "id": item.id,
                    "answer": str(expected_output),
                    "explanation": "",
                    "sources": [],
                    "confidence": 1.0
                }

            answers_data.append(answer_entry)

        # Save both files
        self._save_json_file(questions_data, questions_file)
        self._save_json_file(answers_data, answers_file)

        self.logger.info(f"Successfully saved {len(items)} Q&A dataset items")

    def load_rag_documents(self) -> List[Dict[str, Any]]:
        """
        Load documents for RAG testing from various formats.

        Returns:
            List of document dictionaries with content and metadata

        Raises:
            FileNotFoundError: If RAG documents directory doesn't exist
        """
        rag_dir = self.dataset_path / "rag_documents"
        documents_dir = rag_dir / "documents"

        if not documents_dir.exists():
            raise FileNotFoundError(f"RAG documents directory not found: {documents_dir}")

        documents = []
        supported_extensions = {'.txt', '.md', '.json', '.csv', '.xml'}

        # Recursively find all supported document files
        for file_path in documents_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                try:
                    document = self._load_document_file(file_path)
                    if document:
                        documents.append(document)
                except Exception as e:
                    self.logger.warning(f"Failed to load document {file_path}: {e}")
                    continue

        self.logger.info(f"Successfully loaded {len(documents)} RAG documents")
        return documents

    def _load_document_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load a single document file and extract its content and metadata.

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary containing document content and metadata, or None if failed
        """
        try:
            # Read file content based on extension
            if file_path.suffix.lower() in {'.txt', '.md'}:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            elif file_path.suffix.lower() == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
            else:
                # For other formats, read as text for now
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

            # Extract metadata
            stat = file_path.stat()

            document = {
                'id': str(file_path.relative_to(self.dataset_path)),
                'filename': file_path.name,
                'filepath': str(file_path),
                'content': content,
                'format': file_path.suffix.lower().lstrip('.'),
                'size_bytes': stat.st_size,
                'created_date': stat.st_ctime,
                'modified_date': stat.st_mtime,
                'metadata': {
                    'source': 'local_file',
                    'domain': self._infer_domain_from_path(file_path),
                    'content_type': self._infer_content_type(file_path, content)
                }
            }

            return document

        except Exception as e:
            self.logger.error(f"Error loading document {file_path}: {e}")
            return None

    def _infer_domain_from_path(self, file_path: Path) -> str:
        """
        Infer document domain from file path structure.

        Args:
            file_path: Path to the document

        Returns:
            Inferred domain category
        """
        path_parts = file_path.parts

        # Look for domain indicators in path
        domain_keywords = {
            'technology': ['tech', 'software', 'programming', 'code'],
            'business': ['business', 'finance', 'marketing', 'sales'],
            'science': ['science', 'research', 'academic', 'study'],
            'legal': ['legal', 'law', 'policy', 'regulation'],
            'education': ['education', 'learning', 'tutorial', 'guide']
        }

        for part in path_parts:
            part_lower = part.lower()
            for domain, keywords in domain_keywords.items():
                if any(keyword in part_lower for keyword in keywords):
                    return domain

        return 'general'

    def _infer_content_type(self, file_path: Path, content: Any) -> str:
        """
        Infer content type from file extension and content.

        Args:
            file_path: Path to the document
            content: Document content

        Returns:
            Inferred content type
        """
        extension = file_path.suffix.lower()

        if extension == '.md':
            return 'markdown'
        elif extension == '.json':
            return 'structured_data'
        elif extension == '.csv':
            return 'tabular_data'
        elif extension == '.xml':
            return 'structured_markup'
        elif extension == '.txt':
            # Try to infer from content
            if isinstance(content, str):
                if content.strip().startswith(('# ', '## ', '### ')):
                    return 'markdown'
                elif content.count('\n') > content.count(' ') * 0.1:
                    return 'structured_text'
            return 'plain_text'
        else:
            return 'unknown'

    def load_rag_ground_truth(self) -> List[Dict[str, Any]]:
        """
        Load expected retrieval results for RAG queries.

        Returns:
            List of ground truth data for RAG evaluation

        Raises:
            FileNotFoundError: If ground truth files don't exist
        """
        rag_dir = self.dataset_path / "rag_documents"
        ground_truth_dir = rag_dir / "ground_truth"

        if not ground_truth_dir.exists():
            raise FileNotFoundError(f"RAG ground truth directory not found: {ground_truth_dir}")

        ground_truth_data = []

        # Look for ground truth files
        for file_path in ground_truth_dir.glob('*.json'):
            try:
                data = self._load_json_file(file_path)
                ground_truth_data.extend(data)
            except Exception as e:
                self.logger.warning(f"Failed to load ground truth file {file_path}: {e}")
                continue

        # Validate and structure ground truth data
        structured_data = []
        for item in ground_truth_data:
            try:
                structured_item = {
                    'query_id': item.get('query_id', item.get('id')),
                    'query': item.get('query'),
                    'expected_documents': item.get('expected_documents', []),
                    'relevance_scores': item.get('relevance_scores', {}),
                    'ranking': item.get('ranking', []),
                    'metadata': {
                        'query_type': item.get('query_type', 'general'),
                        'difficulty': item.get('difficulty', 'medium'),
                        'domain': item.get('domain', 'general'),
                        'multiple_answers': item.get('multiple_answers', False)
                    }
                }

                # Validate required fields
                if not structured_item['query_id'] or not structured_item['query']:
                    self.logger.warning(f"Skipping ground truth item with missing query_id or query")
                    continue

                structured_data.append(structured_item)

            except Exception as e:
                self.logger.warning(f"Error processing ground truth item: {e}")
                continue

        self.logger.info(f"Successfully loaded {len(structured_data)} RAG ground truth items")
        return structured_data

    def load_search_queries(self) -> List[DatasetItem]:
        """
        Load web search test queries.

        Returns:
            List of DatasetItem objects containing search queries and expected results

        Raises:
            FileNotFoundError: If web search files don't exist
        """
        web_search_dir = self.dataset_path / "web_search"
        queries_file = web_search_dir / "queries.json"
        expected_sources_file = web_search_dir / "expected_sources.json"

        # Load queries and expected sources
        queries_data = self._load_json_file(queries_file)
        expected_sources_data = self._load_json_file(expected_sources_file)

        # Create lookup dictionary for expected sources
        sources_lookup = {item['query_id']: item for item in expected_sources_data}

        dataset_items = []

        for query_item in queries_data:
            query_id = query_item.get('id')

            if not query_id:
                self.logger.warning("Query item missing ID, skipping")
                continue

            if query_id not in sources_lookup:
                self.logger.warning(f"No expected sources found for query ID: {query_id}")
                continue

            sources_item = sources_lookup[query_id]

            # Create DatasetItem
            try:
                dataset_item = DatasetItem(
                    id=query_id,
                    input_data={
                        "query": query_item.get('query'),
                        "search_type": query_item.get('search_type', 'general'),
                        "freshness_requirement": query_item.get('freshness_requirement'),
                        "expected_result_count": query_item.get('expected_result_count', 5)
                    },
                    expected_output={
                        "expected_sources": sources_item.get('expected_sources', []),
                        "credibility_levels": sources_item.get('credibility_levels', {}),
                        "source_types": sources_item.get('source_types', []),
                        "verification_criteria": sources_item.get('verification_criteria', [])
                    },
                    metadata={
                        "search_type": query_item.get('search_type', 'general'),
                        "time_sensitive": query_item.get('time_sensitive', False),
                        "freshness_requirement": query_item.get('freshness_requirement'),
                        "complexity": query_item.get('complexity', 'medium'),
                        "domain": query_item.get('domain', 'general')
                    },
                    difficulty_level=query_item.get('difficulty'),
                    category=query_item.get('category', 'web_search')
                )

                dataset_items.append(dataset_item)

            except Exception as e:
                self.logger.error(f"Error creating DatasetItem for query {query_id}: {e}")
                continue

        self.logger.info(f"Successfully loaded {len(dataset_items)} web search query items")
        return dataset_items

    def load_multiagent_scenarios(self) -> List[Dict[str, Any]]:
        """
        Load multi-agent use case scenarios.

        Returns:
            List of multi-agent scenario dictionaries

        Raises:
            FileNotFoundError: If multi-agent directory doesn't exist
        """
        multi_agent_dir = self.dataset_path / "multi_agent"

        if not multi_agent_dir.exists():
            raise FileNotFoundError(f"Multi-agent directory not found: {multi_agent_dir}")

        scenarios = []

        # Load different types of multi-agent scenarios
        scenario_files = {
            'research_tasks.json': 'research',
            'customer_service.json': 'customer_service',
            'content_creation.json': 'content_creation'
        }

        for filename, scenario_type in scenario_files.items():
            file_path = multi_agent_dir / filename

            if file_path.exists():
                try:
                    data = self._load_json_file(file_path)

                    # Process and structure each scenario
                    for item in data:
                        scenario = {
                            'id': item.get('id'),
                            'type': scenario_type,
                            'title': item.get('task', item.get('project', item.get('scenario'))),
                            'description': item.get('description'),
                            'required_agents': item.get('required_agents', []),
                            'coordination_pattern': self._analyze_coordination_pattern(item.get('required_agents', [])),
                            'complexity_level': self._determine_complexity_level(item.get('required_agents', [])),
                            'expected_workflow': item.get('expected_workflow', []),
                            'success_criteria': item.get('success_criteria', []),
                            'metadata': {
                                'scenario_type': scenario_type,
                                'agent_count': len(item.get('required_agents', [])),
                                'estimated_duration': item.get('estimated_duration'),
                                'difficulty': item.get('difficulty', 'medium'),
                                'domain': item.get('domain', scenario_type)
                            }
                        }

                        # Validate required fields
                        if scenario['id'] and scenario['title'] and scenario['required_agents']:
                            scenarios.append(scenario)
                        else:
                            self.logger.warning(f"Skipping incomplete scenario: {scenario.get('id', 'unknown')}")

                except Exception as e:
                    self.logger.warning(f"Failed to load scenario file {filename}: {e}")
                    continue
            else:
                self.logger.info(f"Scenario file not found: {filename}")

        self.logger.info(f"Successfully loaded {len(scenarios)} multi-agent scenarios")
        return scenarios

    def _analyze_coordination_pattern(self, agents: List[Dict[str, Any]]) -> str:
        """
        Analyze the coordination pattern based on agent roles and responsibilities.

        Args:
            agents: List of agent definitions

        Returns:
            Coordination pattern type
        """
        if not agents:
            return 'none'

        agent_count = len(agents)

        if agent_count <= 2:
            return 'linear'
        elif agent_count == 3:
            return 'triangular'
        elif agent_count <= 4:
            return 'hierarchical'
        else:
            return 'complex_network'

    def _determine_complexity_level(self, agents: List[Dict[str, Any]]) -> str:
        """
        Determine complexity level based on agent count and roles.

        Args:
            agents: List of agent definitions

        Returns:
            Complexity level (simple, medium, complex, advanced)
        """
        if not agents:
            return 'simple'

        agent_count = len(agents)

        # Check for role complexity
        has_coordinator = any('coordinator' in agent.get('role', '').lower() for agent in agents)
        has_specialized_roles = len(set(agent.get('role', '') for agent in agents)) > 2

        if agent_count <= 2:
            return 'simple'
        elif agent_count == 3 and not has_specialized_roles:
            return 'medium'
        elif agent_count <= 4 and (has_specialized_roles or has_coordinator):
            return 'complex'
        else:
            return 'advanced'

    def get_dataset_stats(self) -> Dict[str, Any]:
        """
        Calculate comprehensive dataset statistics and analysis.

        Returns:
            Dictionary containing dataset statistics and metrics
        """
        stats = {
            'timestamp': self._get_current_timestamp(),
            'dataset_path': str(self.dataset_path),
            'qa_stats': {},
            'rag_stats': {},
            'web_search_stats': {},
            'multi_agent_stats': {},
            'overall_stats': {}
        }

        try:
            # Q&A dataset statistics
            qa_items = self.load_qa_dataset()
            stats['qa_stats'] = self._calculate_qa_stats(qa_items)
        except Exception as e:
            self.logger.warning(f"Could not load Q&A dataset for stats: {e}")
            stats['qa_stats'] = {'error': str(e)}

        try:
            # RAG dataset statistics
            rag_docs = self.load_rag_documents()
            rag_ground_truth = self.load_rag_ground_truth()
            stats['rag_stats'] = self._calculate_rag_stats(rag_docs, rag_ground_truth)
        except Exception as e:
            self.logger.warning(f"Could not load RAG dataset for stats: {e}")
            stats['rag_stats'] = {'error': str(e)}

        try:
            # Web search statistics
            search_queries = self.load_search_queries()
            stats['web_search_stats'] = self._calculate_search_stats(search_queries)
        except Exception as e:
            self.logger.warning(f"Could not load web search dataset for stats: {e}")
            stats['web_search_stats'] = {'error': str(e)}

        try:
            # Multi-agent statistics
            scenarios = self.load_multiagent_scenarios()
            stats['multi_agent_stats'] = self._calculate_multiagent_stats(scenarios)
        except Exception as e:
            self.logger.warning(f"Could not load multi-agent dataset for stats: {e}")
            stats['multi_agent_stats'] = {'error': str(e)}

        # Calculate overall statistics
        stats['overall_stats'] = self._calculate_overall_stats(stats)

        return stats

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()

    def _calculate_qa_stats(self, items: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate Q&A dataset statistics."""
        if not items:
            return {'count': 0}

        from collections import Counter

        stats = {
            'count': len(items),
            'categories': dict(Counter(item.category for item in items if item.category)),
            'difficulty_levels': dict(Counter(item.difficulty_level for item in items if item.difficulty_level)),
            'avg_question_length': 0,
            'avg_answer_length': 0,
            'question_types': {},
            'confidence_distribution': {}
        }

        # Calculate average lengths and analyze content
        question_lengths = []
        answer_lengths = []
        question_types = Counter()
        confidences = []

        for item in items:
            # Question analysis
            if isinstance(item.input_data, dict) and 'question' in item.input_data:
                question = item.input_data['question']
                if isinstance(question, str):
                    question_lengths.append(len(question))
                    question_types[item.input_data.get('expected_response_type', 'unknown')] += 1

            # Answer analysis
            if isinstance(item.expected_output, dict):
                answer = item.expected_output.get('answer', '')
                if isinstance(answer, str):
                    answer_lengths.append(len(answer))

                confidence = item.expected_output.get('confidence')
                if confidence is not None:
                    confidences.append(confidence)

        if question_lengths:
            stats['avg_question_length'] = sum(question_lengths) / len(question_lengths)

        if answer_lengths:
            stats['avg_answer_length'] = sum(answer_lengths) / len(answer_lengths)

        stats['question_types'] = dict(question_types)

        if confidences:
            stats['confidence_distribution'] = {
                'min': min(confidences),
                'max': max(confidences),
                'avg': sum(confidences) / len(confidences)
            }

        return stats

    def _calculate_rag_stats(self, documents: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate RAG dataset statistics."""
        from collections import Counter

        stats = {
            'document_count': len(documents),
            'ground_truth_count': len(ground_truth),
            'document_formats': {},
            'document_domains': {},
            'content_types': {},
            'avg_document_size': 0,
            'total_size_mb': 0
        }

        if documents:
            # Analyze document formats and domains
            formats = Counter(doc.get('format', 'unknown') for doc in documents)
            domains = Counter(doc.get('metadata', {}).get('domain', 'unknown') for doc in documents)
            content_types = Counter(doc.get('metadata', {}).get('content_type', 'unknown') for doc in documents)

            stats['document_formats'] = dict(formats)
            stats['document_domains'] = dict(domains)
            stats['content_types'] = dict(content_types)

            # Calculate size statistics
            sizes = [doc.get('size_bytes', 0) for doc in documents]
            if sizes:
                stats['avg_document_size'] = sum(sizes) / len(sizes)
                stats['total_size_mb'] = sum(sizes) / (1024 * 1024)

        if ground_truth:
            # Analyze ground truth data
            query_types = Counter(item.get('metadata', {}).get('query_type', 'unknown') for item in ground_truth)
            difficulties = Counter(item.get('metadata', {}).get('difficulty', 'unknown') for item in ground_truth)

            stats['query_types'] = dict(query_types)
            stats['query_difficulties'] = dict(difficulties)

            # Calculate average expected documents per query
            expected_doc_counts = [len(item.get('expected_documents', [])) for item in ground_truth]
            if expected_doc_counts:
                stats['avg_expected_docs_per_query'] = sum(expected_doc_counts) / len(expected_doc_counts)

        return stats

    def _calculate_search_stats(self, queries: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate web search dataset statistics."""
        if not queries:
            return {'count': 0}

        from collections import Counter

        stats = {
            'count': len(queries),
            'search_types': {},
            'complexity_levels': {},
            'time_sensitive_queries': 0,
            'avg_expected_results': 0,
            'domains': {}
        }

        search_types = Counter()
        complexity_levels = Counter()
        domains = Counter()
        expected_result_counts = []
        time_sensitive_count = 0

        for query in queries:
            if isinstance(query.input_data, dict):
                search_type = query.input_data.get('search_type', 'general')
                search_types[search_type] += 1

                expected_count = query.input_data.get('expected_result_count', 0)
                if expected_count:
                    expected_result_counts.append(expected_count)

            if query.metadata:
                complexity = query.metadata.get('complexity', 'medium')
                complexity_levels[complexity] += 1

                domain = query.metadata.get('domain', 'general')
                domains[domain] += 1

                if query.metadata.get('time_sensitive', False):
                    time_sensitive_count += 1

        stats['search_types'] = dict(search_types)
        stats['complexity_levels'] = dict(complexity_levels)
        stats['domains'] = dict(domains)
        stats['time_sensitive_queries'] = time_sensitive_count

        if expected_result_counts:
            stats['avg_expected_results'] = sum(expected_result_counts) / len(expected_result_counts)

        return stats

    def _calculate_multiagent_stats(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate multi-agent dataset statistics."""
        if not scenarios:
            return {'count': 0}

        from collections import Counter

        stats = {
            'count': len(scenarios),
            'scenario_types': {},
            'complexity_levels': {},
            'coordination_patterns': {},
            'agent_count_distribution': {},
            'avg_agents_per_scenario': 0,
            'role_frequency': {}
        }

        scenario_types = Counter(scenario.get('type', 'unknown') for scenario in scenarios)
        complexity_levels = Counter(scenario.get('complexity_level', 'unknown') for scenario in scenarios)
        coordination_patterns = Counter(scenario.get('coordination_pattern', 'unknown') for scenario in scenarios)

        agent_counts = []
        all_roles = Counter()

        for scenario in scenarios:
            agent_count = scenario.get('metadata', {}).get('agent_count', 0)
            if agent_count:
                agent_counts.append(agent_count)

            # Count roles across all scenarios
            agents = scenario.get('required_agents', [])
            for agent in agents:
                role = agent.get('role', 'unknown')
                all_roles[role] += 1

        stats['scenario_types'] = dict(scenario_types)
        stats['complexity_levels'] = dict(complexity_levels)
        stats['coordination_patterns'] = dict(coordination_patterns)
        stats['role_frequency'] = dict(all_roles)

        if agent_counts:
            stats['avg_agents_per_scenario'] = sum(agent_counts) / len(agent_counts)
            agent_count_dist = Counter(agent_counts)
            stats['agent_count_distribution'] = dict(agent_count_dist)

        return stats

    def _calculate_overall_stats(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall dataset statistics."""
        overall = {
            'total_datasets': 0,
            'total_items': 0,
            'datasets_with_errors': 0,
            'coverage_analysis': {},
            'freshness_info': {
                'last_updated': stats.get('timestamp'),
                'dataset_path': stats.get('dataset_path')
            }
        }

        # Count datasets and items
        for dataset_type in ['qa_stats', 'rag_stats', 'web_search_stats', 'multi_agent_stats']:
            dataset_stats = stats.get(dataset_type, {})

            if 'error' not in dataset_stats:
                overall['total_datasets'] += 1

                # Add item counts
                if dataset_type == 'qa_stats':
                    overall['total_items'] += dataset_stats.get('count', 0)
                elif dataset_type == 'rag_stats':
                    overall['total_items'] += dataset_stats.get('document_count', 0)
                    overall['total_items'] += dataset_stats.get('ground_truth_count', 0)
                elif dataset_type == 'web_search_stats':
                    overall['total_items'] += dataset_stats.get('count', 0)
                elif dataset_type == 'multi_agent_stats':
                    overall['total_items'] += dataset_stats.get('count', 0)
            else:
                overall['datasets_with_errors'] += 1

        # Coverage analysis
        overall['coverage_analysis'] = {
            'qa_available': 'error' not in stats.get('qa_stats', {}),
            'rag_available': 'error' not in stats.get('rag_stats', {}),
            'web_search_available': 'error' not in stats.get('web_search_stats', {}),
            'multi_agent_available': 'error' not in stats.get('multi_agent_stats', {})
        }

        return overall

    def export_dataset(self, dataset_type: str, format: str, output_path: Path, compress: bool = False) -> None:
        """
        Export dataset to specified format and location.

        Args:
            dataset_type: Type of dataset to export (qa, rag, web_search, multi_agent)
            format: Export format (json, jsonl, csv)
            output_path: Path where to save the exported data
            compress: Whether to compress the output file using gzip

        Raises:
            ValueError: If dataset type or format is not supported
            FileNotFoundError: If dataset doesn't exist
        """
        # Validate format
        if format not in ['json', 'jsonl', 'csv']:
            raise ValueError(f"Unsupported export format: {format}")

        # Load the appropriate dataset
        if dataset_type == 'qa':
            items = self.load_qa_dataset()
            data = [item.to_dict() for item in items]
        elif dataset_type == 'rag':
            data = self.load_rag_documents()
        elif dataset_type == 'web_search':
            items = self.load_search_queries()
            data = [item.to_dict() for item in items]
        elif dataset_type == 'multi_agent':
            data = self.load_multiagent_scenarios()
        else:
            raise ValueError(f"Unsupported dataset type: {dataset_type}")

        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Adjust output path for compression
        final_output_path = output_path
        if compress:
            final_output_path = output_path.with_suffix(f"{output_path.suffix}.gz")

        # Export based on format
        if format == 'json':
            self._export_json(data, final_output_path, compress)
        elif format == 'jsonl':
            self._export_jsonl(data, final_output_path, compress)
        elif format == 'csv':
            self._export_csv(data, final_output_path, dataset_type, compress)

        compression_info = " (compressed)" if compress else ""
        self.logger.info(f"Successfully exported {len(data)} items to {final_output_path}{compression_info}")

    def _export_json(self, data: List[Dict[str, Any]], output_path: Path, compress: bool = False) -> None:
        """Export data as JSON."""
        if compress:
            import gzip
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

    def _export_jsonl(self, data: List[Dict[str, Any]], output_path: Path, compress: bool = False) -> None:
        """Export data as JSON Lines."""
        if compress:
            import gzip
            with gzip.open(output_path, 'wt', encoding='utf-8') as f:
                for item in data:
                    json.dump(item, f, ensure_ascii=False, default=str)
                    f.write('\n')
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                for item in data:
                    json.dump(item, f, ensure_ascii=False, default=str)
                    f.write('\n')

    def _export_csv(self, data: List[Dict[str, Any]], output_path: Path, dataset_type: str, compress: bool = False) -> None:
        """Export data as CSV with dataset-specific column handling."""
        import csv

        if not data:
            return

        # Define column mappings for different dataset types
        if dataset_type == 'qa':
            fieldnames = ['id', 'input_data', 'expected_output', 'category', 'difficulty_level', 'metadata']
        elif dataset_type == 'rag':
            fieldnames = ['id', 'filename', 'content', 'format', 'size_bytes', 'domain', 'content_type']
        elif dataset_type == 'web_search':
            fieldnames = ['id', 'input_data', 'expected_output', 'category', 'difficulty_level', 'metadata']
        elif dataset_type == 'multi_agent':
            fieldnames = ['id', 'type', 'title', 'description', 'agent_count', 'complexity_level']
        else:
            # Fallback: use all keys from first item
            fieldnames = list(data[0].keys())

        if compress:
            import gzip
            with gzip.open(output_path, 'wt', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for item in data:
                    # Flatten complex fields for CSV
                    flattened_item = self._flatten_for_csv(item, dataset_type)
                    writer.writerow(flattened_item)
        else:
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()

                for item in data:
                    # Flatten complex fields for CSV
                    flattened_item = self._flatten_for_csv(item, dataset_type)
                    writer.writerow(flattened_item)

    def _flatten_for_csv(self, item: Dict[str, Any], dataset_type: str) -> Dict[str, Any]:
        """Flatten complex data structures for CSV export."""
        flattened = {}

        for key, value in item.items():
            if isinstance(value, (dict, list)):
                # Convert complex types to JSON strings
                flattened[key] = json.dumps(value, default=str)
            else:
                flattened[key] = value

        # Add dataset-specific flattening
        if dataset_type == 'rag' and 'metadata' in item:
            metadata = item['metadata']
            if isinstance(metadata, dict):
                flattened['domain'] = metadata.get('domain', '')
                flattened['content_type'] = metadata.get('content_type', '')

        if dataset_type == 'multi_agent' and 'metadata' in item:
            metadata = item['metadata']
            if isinstance(metadata, dict):
                flattened['agent_count'] = metadata.get('agent_count', 0)

        return flattened

    def import_dataset(self, source_path: Path, format: str, dataset_type: str, merge: bool = False) -> None:
        """
        Import dataset from external source.

        Args:
            source_path: Path to the source file
            format: Source format (json, jsonl, csv)
            dataset_type: Target dataset type (qa, rag, web_search, multi_agent)
            merge: Whether to merge with existing data or replace

        Raises:
            ValueError: If format or dataset type is not supported
            FileNotFoundError: If source file doesn't exist
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")

        if format not in ['json', 'jsonl', 'csv']:
            raise ValueError(f"Unsupported import format: {format}")

        if dataset_type not in ['qa', 'rag', 'web_search', 'multi_agent']:
            raise ValueError(f"Unsupported dataset type: {dataset_type}")

        # Load data from source
        if format == 'json':
            imported_data = self._import_json(source_path)
        elif format == 'jsonl':
            imported_data = self._import_jsonl(source_path)
        elif format == 'csv':
            imported_data = self._import_csv(source_path, dataset_type)

        # Validate imported data
        self._validate_imported_data(imported_data, dataset_type)

        # Convert to appropriate format and save
        if dataset_type == 'qa':
            self._import_qa_dataset(imported_data, merge)
        elif dataset_type == 'web_search':
            self._import_search_dataset(imported_data, merge)
        else:
            # For rag and multi_agent, direct file replacement for now
            self._import_direct_dataset(imported_data, dataset_type, merge)

        self.logger.info(f"Successfully imported {len(imported_data)} items for {dataset_type} dataset")

    def _import_json(self, source_path: Path) -> List[Dict[str, Any]]:
        """Import data from JSON file."""
        return self._load_json_file(source_path)

    def _import_jsonl(self, source_path: Path) -> List[Dict[str, Any]]:
        """Import data from JSON Lines file."""
        data = []
        with open(source_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    try:
                        item = json.loads(line)
                        data.append(item)
                    except json.JSONDecodeError as e:
                        self.logger.warning(f"Invalid JSON on line {line_num}: {e}")
                        continue
        return data

    def _import_csv(self, source_path: Path, dataset_type: str) -> List[Dict[str, Any]]:
        """Import data from CSV file."""
        import csv

        data = []
        with open(source_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row_num, row in enumerate(reader, 1):
                try:
                    # Unflatten complex fields that were JSON-encoded
                    processed_row = self._unflatten_from_csv(row, dataset_type)
                    data.append(processed_row)
                except Exception as e:
                    self.logger.warning(f"Error processing CSV row {row_num}: {e}")
                    continue

        return data

    def _unflatten_from_csv(self, row: Dict[str, str], dataset_type: str) -> Dict[str, Any]:
        """Unflatten CSV row data back to complex structures."""
        processed = {}

        # Dataset-specific field handling
        json_fields = {
            'qa': ['input_data', 'expected_output', 'metadata'],
            'rag': ['metadata'],
            'web_search': ['input_data', 'expected_output', 'metadata'],
            'multi_agent': ['required_agents', 'metadata', 'expected_workflow', 'success_criteria']
        }.get(dataset_type, ['metadata'])

        for key, value in row.items():
            if not value:  # Skip empty values
                continue

            # Try to parse JSON-encoded fields
            if key in json_fields:
                try:
                    processed[key] = json.loads(value)
                except json.JSONDecodeError:
                    processed[key] = value
            else:
                processed[key] = value

        return processed

    def _validate_imported_data(self, data: List[Dict[str, Any]], dataset_type: str) -> None:
        """Validate imported data structure."""
        if not data:
            raise ValueError("Imported data is empty")

        required_fields = {
            'qa': ['id'],
            'rag': ['id', 'content'],
            'web_search': ['id'],
            'multi_agent': ['id', 'type']
        }

        required = required_fields.get(dataset_type, ['id'])

        for i, item in enumerate(data):
            for field in required:
                if field not in item or not item[field]:
                    raise ValueError(f"Item {i}: Missing required field '{field}'")

    def _import_qa_dataset(self, data: List[Dict[str, Any]], merge: bool) -> None:
        """Import Q&A dataset with proper structure conversion."""
        # Convert imported data to DatasetItem objects
        dataset_items = []

        for item in data:
            try:
                # Handle different import formats
                if 'input_data' in item and 'expected_output' in item:
                    # Already in DatasetItem format
                    dataset_item = DatasetItem.from_dict(item)
                else:
                    # Convert from separate question/answer format
                    dataset_item = DatasetItem(
                        id=item['id'],
                        input_data=item.get('question', item.get('input_data', '')),
                        expected_output=item.get('answer', item.get('expected_output', '')),
                        metadata=item.get('metadata', {}),
                        difficulty_level=item.get('difficulty_level', item.get('difficulty')),
                        category=item.get('category')
                    )

                dataset_items.append(dataset_item)

            except Exception as e:
                self.logger.warning(f"Error converting item {item.get('id', 'unknown')}: {e}")
                continue

        # Merge or replace
        if merge:
            try:
                existing_items = self.load_qa_dataset()
                # Remove duplicates by ID
                existing_ids = {item.id for item in existing_items}
                new_items = [item for item in dataset_items if item.id not in existing_ids]
                dataset_items = existing_items + new_items
            except Exception:
                # If loading fails, just use imported data
                pass

        # Save the dataset
        self.save_qa_dataset(dataset_items)

    def _import_search_dataset(self, data: List[Dict[str, Any]], merge: bool) -> None:
        """Import web search dataset with proper structure conversion."""
        # Similar to Q&A import but for search queries
        dataset_items = []

        for item in data:
            try:
                if 'input_data' in item and 'expected_output' in item:
                    dataset_item = DatasetItem.from_dict(item)
                else:
                    # Convert from query/sources format
                    dataset_item = DatasetItem(
                        id=item['id'],
                        input_data={
                            'query': item.get('query', ''),
                            'search_type': item.get('search_type', 'general')
                        },
                        expected_output={
                            'expected_sources': item.get('expected_sources', []),
                            'source_types': item.get('source_types', [])
                        },
                        metadata=item.get('metadata', {}),
                        difficulty_level=item.get('difficulty_level', item.get('difficulty')),
                        category=item.get('category', 'web_search')
                    )

                dataset_items.append(dataset_item)

            except Exception as e:
                self.logger.warning(f"Error converting search item {item.get('id', 'unknown')}: {e}")
                continue

        # Handle merge option
        if merge:
            try:
                existing_items = self.load_search_queries()
                existing_ids = {item.id for item in existing_items}
                new_items = [item for item in dataset_items if item.id not in existing_ids]
                dataset_items = existing_items + new_items
            except Exception:
                # If loading fails, just use imported data
                pass

        # For now, save as separate files (this would need custom implementation)
        # This is a simplified version - full implementation would require
        # splitting into queries.json and expected_sources.json
        self.logger.info(f"Converted {len(dataset_items)} search query items")

    def _import_direct_dataset(self, data: List[Dict[str, Any]], dataset_type: str, merge: bool) -> None:
        """Import datasets that don't need DatasetItem conversion."""
        # For RAG and multi-agent datasets, save directly to appropriate files
        target_dir = self.dataset_path / {
            'rag': 'rag_documents',
            'multi_agent': 'multi_agent'
        }[dataset_type]

        if merge:
            self.logger.warning(f"Merge not implemented for {dataset_type} datasets - replacing data")

        # Save to appropriate file
        if dataset_type == 'rag':
            output_file = target_dir / 'documents' / 'imported_documents.json'
        else:  # multi_agent
            output_file = target_dir / 'imported_scenarios.json'

        self._save_json_file(data, output_file)
