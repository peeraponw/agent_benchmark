"""
Shared Dataset Manager for AI Agent Framework Comparison.

This module provides the core dataset management functionality for loading,
validating, and managing test datasets across all AI agent frameworks.

This is the main interface module that coordinates between the specialized
modules for loading, statistics, and I/O operations.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Import from modular components
from .core.models import DatasetItem
from .core.exceptions import DatasetError, create_user_friendly_error_message
from .loaders import DatasetLoader
from .statistics import DatasetStatistics
from .io_utils import DatasetIOManager


class DatasetManager:
    """
    Core dataset management class for loading and managing test datasets.

    This class provides centralized access to all shared datasets used for
    evaluating AI agent frameworks, ensuring consistency and standardization.

    The class now uses a modular architecture with specialized components for
    loading, statistics, and I/O operations while maintaining backward compatibility.
    """

    def __init__(self, dataset_path: Union[str, Path]):
        """
        Initialize the DatasetManager with modular components.

        Args:
            dataset_path: Path to the root directory containing datasets
        """
        self.dataset_path = Path(dataset_path)
        self._setup_logging()
        self._validate_dataset_path()

        # Initialize modular components
        try:
            self.loader = DatasetLoader(self.dataset_path)
            self.statistics = DatasetStatistics()
            self.io_manager = DatasetIOManager(self.dataset_path)
        except Exception as e:
            error_msg = create_user_friendly_error_message(
                DatasetError(f"Failed to initialize dataset components: {str(e)}")
            )
            self.logger.error(error_msg)
            raise
    
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
        Load and parse a JSON file safely using the modular loader.

        Args:
            file_path: Path to the JSON file

        Returns:
            List of dictionaries from the JSON file

        Raises:
            DatasetError: If loading fails
        """
        try:
            return self.loader.load_json_file(file_path)
        except Exception as e:
            # Convert to user-friendly error message
            error_msg = create_user_friendly_error_message(
                DatasetError(f"Failed to load JSON file {file_path}: {str(e)}")
            )
            self.logger.error(error_msg)
            raise
    
    def _save_json_file(self, data: List[Dict[str, Any]], file_path: Path) -> None:
        """
        Save data to a JSON file safely using the modular I/O manager.

        Args:
            data: List of dictionaries to save
            file_path: Path where to save the file
        """
        try:
            self.io_manager.save_json_file(data, file_path, create_backup=True)
        except Exception as e:
            # Convert to user-friendly error message
            error_msg = create_user_friendly_error_message(
                DatasetError(f"Failed to save JSON file {file_path}: {str(e)}")
            )
            self.logger.error(error_msg)
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
        Load a single document file using the modular loader.

        Args:
            file_path: Path to the document file

        Returns:
            Dictionary containing document content and metadata, or None if failed
        """
        try:
            return self.loader.load_document_file(file_path)
        except Exception as e:
            self.logger.error(f"Error loading document {file_path}: {e}")
            return None



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
        """Get current timestamp in ISO format using the modular statistics component."""
        return self.statistics.get_current_timestamp()

    def _calculate_qa_stats(self, items: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate Q&A dataset statistics using the modular statistics component."""
        try:
            return self.statistics.calculate_qa_stats(items)
        except Exception as e:
            self.logger.error(f"Error calculating Q&A statistics: {e}")
            return {'error': str(e), 'total_items': len(items) if items else 0}

    def _calculate_rag_stats(self, documents: List[Dict[str, Any]], ground_truth: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate RAG dataset statistics using the modular statistics component."""
        try:
            # Note: ground_truth parameter maintained for backward compatibility
            # but not currently used by the modular statistics component
            return self.statistics.calculate_rag_stats(documents)
        except Exception as e:
            self.logger.error(f"Error calculating RAG statistics: {e}")
            return {'error': str(e), 'total_documents': len(documents) if documents else 0}

    def _calculate_search_stats(self, queries: List[DatasetItem]) -> Dict[str, Any]:
        """Calculate web search dataset statistics using the modular statistics component."""
        try:
            return self.statistics.calculate_web_search_stats(queries)
        except Exception as e:
            self.logger.error(f"Error calculating web search statistics: {e}")
            return {'error': str(e), 'total_queries': len(queries) if queries else 0}

    def _calculate_multiagent_stats(self, scenarios: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate multi-agent dataset statistics using the modular statistics component."""
        try:
            return self.statistics.calculate_multi_agent_stats(scenarios)
        except Exception as e:
            self.logger.error(f"Error calculating multi-agent statistics: {e}")
            return {'error': str(e), 'total_scenarios': len(scenarios) if scenarios else 0}

    def _calculate_overall_stats(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall dataset statistics using the modular statistics component."""
        try:
            return self.statistics.calculate_overall_stats(stats)
        except Exception as e:
            self.logger.error(f"Error calculating overall statistics: {e}")
            return {'error': str(e), 'total_datasets': 0, 'total_items': 0}

    def export_dataset(self, dataset_type: str, format: str, output_path: Path, compress: bool = False) -> None:
        """
        Export dataset to specified format and location using the modular I/O manager.

        Args:
            dataset_type: Type of dataset to export (qa, rag, web_search, multi_agent)
            format: Export format (json, jsonl, csv)
            output_path: Path where to save the exported data
            compress: Whether to compress the output file using gzip

        Raises:
            DatasetError: If export operation fails
        """
        try:
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

            # Use the modular I/O manager for export
            self.io_manager.export_dataset(dataset_type, format, output_path, data, compress)

        except Exception as e:
            error_msg = create_user_friendly_error_message(
                DatasetError(f"Failed to export {dataset_type} dataset: {str(e)}")
            )
            self.logger.error(error_msg)
            raise



    def import_dataset(self, source_path: Path, format: str, dataset_type: str, merge: bool = False) -> None:
        """
        Import dataset from external source using the modular I/O manager.

        Args:
            source_path: Path to the source file
            format: Source format (json, jsonl, csv)
            dataset_type: Target dataset type (qa, rag, web_search, multi_agent)
            merge: Whether to merge with existing data or replace

        Raises:
            DatasetError: If import operation fails
        """
        try:
            # Use the modular I/O manager for import
            imported_data = self.io_manager.import_dataset(source_path, format, dataset_type)

            # Convert to appropriate format and save
            if dataset_type == 'qa':
                self._import_qa_dataset(imported_data, merge)
            elif dataset_type == 'web_search':
                self._import_search_dataset(imported_data, merge)
            else:
                # For rag and multi_agent, direct file replacement for now
                self._import_direct_dataset(imported_data, dataset_type, merge)

            self.logger.info(f"Successfully imported {len(imported_data)} items for {dataset_type} dataset")

        except Exception as e:
            error_msg = create_user_friendly_error_message(
                DatasetError(f"Failed to import {dataset_type} dataset: {str(e)}")
            )
            self.logger.error(error_msg)
            raise



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
