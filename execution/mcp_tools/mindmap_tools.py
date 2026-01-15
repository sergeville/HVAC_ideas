#!/usr/bin/env python3
"""
Mind Map Management Tools for MCP Thought-to-Action System

Provides tree structure operations for hierarchical idea organization.
Supports creation, node addition, traversal, and export to various formats.
"""

import logging
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any
from pathlib import Path

from .storage import MindMapStorage

logger = logging.getLogger("mcp_server.mindmap_tools")


@dataclass
class MindMapNode:
    """
    Mind map node with hierarchical structure.

    Each node can have multiple children, forming a tree.
    """
    id: str
    text: str
    children: List['MindMapNode'] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'text': self.text,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MindMapNode':
        """Create MindMapNode from dictionary."""
        children_data = data.get('children', [])
        children = [cls.from_dict(child) for child in children_data]

        return cls(
            id=data['id'],
            text=data['text'],
            children=children,
            metadata=data.get('metadata', {})
        )

    def find_node(self, node_id: str) -> Optional['MindMapNode']:
        """
        Find a node by ID in the tree.

        Args:
            node_id: ID of node to find

        Returns:
            MindMapNode if found, None otherwise
        """
        if self.id == node_id:
            return self

        for child in self.children:
            result = child.find_node(node_id)
            if result:
                return result

        return None

    def add_child(self, node: 'MindMapNode'):
        """Add a child node."""
        self.children.append(node)

    def count_nodes(self) -> int:
        """Count total nodes in subtree."""
        count = 1  # Count self
        for child in self.children:
            count += child.count_nodes()
        return count


@dataclass
class MindMap:
    """
    Complete mind map with metadata and root node.
    """
    id: str
    title: str
    created_at: str
    updated_at: str
    root: MindMapNode

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'root': self.root.to_dict()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MindMap':
        """Create MindMap from dictionary."""
        return cls(
            id=data['id'],
            title=data['title'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            root=MindMapNode.from_dict(data['root'])
        )


@dataclass
class CreateMindMapOutput:
    """Output from creating a mind map."""
    success: bool
    mindmap: Optional[MindMap]
    message: str


@dataclass
class AddNodeOutput:
    """Output from adding a node."""
    success: bool
    node: Optional[MindMapNode]
    mindmap_id: str
    message: str


@dataclass
class GetMindMapOutput:
    """Output from getting a mind map."""
    success: bool
    mindmap: Optional[MindMap]
    message: str


@dataclass
class ExportMindMapOutput:
    """Output from exporting a mind map."""
    success: bool
    content: str
    format: str
    message: str


class MindMapManager:
    """
    High-level manager for mind map operations.

    Usage:
        manager = MindMapManager(Path(".tmp/user_data/mindmaps"))
        result = manager.create_mindmap("MCP Integration", "Project Planning")
        print(result.message)
    """

    def __init__(self, mindmaps_dir: Path):
        """
        Initialize mind map manager.

        Args:
            mindmaps_dir: Directory for mind map storage
        """
        self.storage = MindMapStorage(mindmaps_dir)
        logger.info(f"MindMap manager initialized with storage: {mindmaps_dir}")

    def _generate_mindmap_id(self) -> str:
        """
        Generate unique mind map ID.

        Format: mindmap_YYYYMMDD_HHMMSS_uuid
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"mindmap_{timestamp}_{unique_id}"

    def _generate_node_id(self) -> str:
        """
        Generate unique node ID.

        Format: node_uuid
        """
        return f"node_{str(uuid.uuid4())[:8]}"

    def create_mindmap(
        self,
        title: str,
        root_topic: str,
        initial_nodes: Optional[List[str]] = None
    ) -> CreateMindMapOutput:
        """
        Create a new mind map.

        Args:
            title: Mind map title
            root_topic: Central topic (root node text)
            initial_nodes: Optional list of initial branch texts

        Returns:
            CreateMindMapOutput with success status and mind map
        """
        if not title or not title.strip():
            return CreateMindMapOutput(
                success=False,
                mindmap=None,
                message="Title cannot be empty"
            )

        if not root_topic or not root_topic.strip():
            return CreateMindMapOutput(
                success=False,
                mindmap=None,
                message="Root topic cannot be empty"
            )

        try:
            # Create root node
            root = MindMapNode(
                id="node_root",
                text=root_topic.strip(),
                children=[],
                metadata={}
            )

            # Add initial nodes if provided
            if initial_nodes:
                for node_text in initial_nodes:
                    if node_text and node_text.strip():
                        child = MindMapNode(
                            id=self._generate_node_id(),
                            text=node_text.strip(),
                            children=[],
                            metadata={}
                        )
                        root.add_child(child)

            # Create mind map
            now = datetime.now().isoformat()
            mindmap = MindMap(
                id=self._generate_mindmap_id(),
                title=title.strip(),
                created_at=now,
                updated_at=now,
                root=root
            )

            # Save to storage
            self.storage.save_mindmap(mindmap.to_dict())

            logger.info(f"Created mind map: {mindmap.id} - {mindmap.title}")
            return CreateMindMapOutput(
                success=True,
                mindmap=mindmap,
                message=f"Mind map created: {mindmap.title}"
            )

        except Exception as e:
            logger.error(f"Error creating mind map: {e}")
            return CreateMindMapOutput(
                success=False,
                mindmap=None,
                message=f"Error: {str(e)}"
            )

    def add_mindmap_node(
        self,
        mindmap_id: str,
        parent_node_id: str,
        text: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AddNodeOutput:
        """
        Add a node to an existing mind map.

        Args:
            mindmap_id: ID of mind map
            parent_node_id: ID of parent node
            text: Node text
            metadata: Optional metadata (color, icon, etc.)

        Returns:
            AddNodeOutput with success status and new node
        """
        if not text or not text.strip():
            return AddNodeOutput(
                success=False,
                node=None,
                mindmap_id=mindmap_id,
                message="Node text cannot be empty"
            )

        try:
            # Load mind map
            mindmap_dict = self.storage.load_mindmap(mindmap_id)
            if not mindmap_dict:
                return AddNodeOutput(
                    success=False,
                    node=None,
                    mindmap_id=mindmap_id,
                    message=f"Mind map not found: {mindmap_id}"
                )

            mindmap = MindMap.from_dict(mindmap_dict)

            # Find parent node
            parent = mindmap.root.find_node(parent_node_id)
            if not parent:
                return AddNodeOutput(
                    success=False,
                    node=None,
                    mindmap_id=mindmap_id,
                    message=f"Parent node not found: {parent_node_id}"
                )

            # Create new node
            new_node = MindMapNode(
                id=self._generate_node_id(),
                text=text.strip(),
                children=[],
                metadata=metadata or {}
            )

            # Add to parent
            parent.add_child(new_node)

            # Update timestamp
            mindmap.updated_at = datetime.now().isoformat()

            # Save
            self.storage.save_mindmap(mindmap.to_dict())

            logger.info(f"Added node to mind map {mindmap_id}: {new_node.id}")
            return AddNodeOutput(
                success=True,
                node=new_node,
                mindmap_id=mindmap_id,
                message=f"Node added: {new_node.text}"
            )

        except Exception as e:
            logger.error(f"Error adding node to mind map {mindmap_id}: {e}")
            return AddNodeOutput(
                success=False,
                node=None,
                mindmap_id=mindmap_id,
                message=f"Error: {str(e)}"
            )

    def get_mindmap(self, mindmap_id: str) -> GetMindMapOutput:
        """
        Get a mind map by ID.

        Args:
            mindmap_id: ID of mind map

        Returns:
            GetMindMapOutput with mind map
        """
        try:
            mindmap_dict = self.storage.load_mindmap(mindmap_id)
            if not mindmap_dict:
                return GetMindMapOutput(
                    success=False,
                    mindmap=None,
                    message=f"Mind map not found: {mindmap_id}"
                )

            mindmap = MindMap.from_dict(mindmap_dict)

            logger.info(f"Retrieved mind map: {mindmap_id}")
            return GetMindMapOutput(
                success=True,
                mindmap=mindmap,
                message=f"Mind map: {mindmap.title}"
            )

        except Exception as e:
            logger.error(f"Error getting mind map {mindmap_id}: {e}")
            return GetMindMapOutput(
                success=False,
                mindmap=None,
                message=f"Error: {str(e)}"
            )

    def list_mindmaps(self) -> List[Dict[str, str]]:
        """
        List all mind maps.

        Returns:
            List of {id, title, created_at} dictionaries
        """
        try:
            return self.storage.list_mindmaps()
        except Exception as e:
            logger.error(f"Error listing mind maps: {e}")
            return []

    def delete_mindmap(self, mindmap_id: str) -> bool:
        """
        Delete a mind map.

        Args:
            mindmap_id: ID of mind map to delete

        Returns:
            True if deleted, False otherwise
        """
        try:
            return self.storage.delete_mindmap(mindmap_id)
        except Exception as e:
            logger.error(f"Error deleting mind map {mindmap_id}: {e}")
            return False

    def export_mindmap(
        self,
        mindmap_id: str,
        format: str = "markdown"
    ) -> ExportMindMapOutput:
        """
        Export mind map to various formats.

        Args:
            mindmap_id: ID of mind map to export
            format: Export format (markdown, json, mermaid)

        Returns:
            ExportMindMapOutput with exported content
        """
        if format not in ['markdown', 'json', 'mermaid']:
            return ExportMindMapOutput(
                success=False,
                content="",
                format=format,
                message=f"Invalid format: {format}. Must be markdown, json, or mermaid"
            )

        try:
            mindmap_dict = self.storage.load_mindmap(mindmap_id)
            if not mindmap_dict:
                return ExportMindMapOutput(
                    success=False,
                    content="",
                    format=format,
                    message=f"Mind map not found: {mindmap_id}"
                )

            mindmap = MindMap.from_dict(mindmap_dict)

            if format == 'json':
                import json
                content = json.dumps(mindmap.to_dict(), indent=2)
            elif format == 'markdown':
                content = self._export_to_markdown(mindmap)
            elif format == 'mermaid':
                content = self._export_to_mermaid(mindmap)

            logger.info(f"Exported mind map {mindmap_id} to {format}")
            return ExportMindMapOutput(
                success=True,
                content=content,
                format=format,
                message=f"Mind map exported to {format}"
            )

        except Exception as e:
            logger.error(f"Error exporting mind map {mindmap_id}: {e}")
            return ExportMindMapOutput(
                success=False,
                content="",
                format=format,
                message=f"Error: {str(e)}"
            )

    def _export_to_markdown(self, mindmap: MindMap) -> str:
        """Export mind map to Markdown format."""
        lines = []
        lines.append(f"# {mindmap.title}\n")
        lines.append(f"*Created: {mindmap.created_at}*\n")
        lines.append(f"*Updated: {mindmap.updated_at}*\n")
        lines.append("")

        def render_node(node: MindMapNode, level: int = 0):
            indent = "  " * level
            bullet = "-" if level > 0 else "##"
            lines.append(f"{indent}{bullet} {node.text}")

            for child in node.children:
                render_node(child, level + 1)

        render_node(mindmap.root)
        return "\n".join(lines)

    def _export_to_mermaid(self, mindmap: MindMap) -> str:
        """Export mind map to Mermaid diagram format."""
        lines = []
        lines.append("```mermaid")
        lines.append("graph TD")

        def render_node(node: MindMapNode):
            node_label = node.text.replace('"', '\\"')
            lines.append(f'    {node.id}["{node_label}"]')

            for child in node.children:
                lines.append(f'    {node.id} --> {child.id}')
                render_node(child)

        render_node(mindmap.root)
        lines.append("```")
        return "\n".join(lines)
