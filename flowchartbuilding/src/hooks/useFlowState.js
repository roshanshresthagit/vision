import { useState, useCallback } from 'react';
import { useNodesState, useEdgesState } from 'reactflow';

export const useFlowState = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [inputNodeCount, setInputNodeCount] = useState(0);
  const [generatedCode, setGeneratedCode] = useState('');

  const onDeleteNode = useCallback(() => {
    if (selectedNodeId) {
      setNodes(nds => nds.filter(node => node.id !== selectedNodeId));
      setEdges(eds => eds.filter(edge => 
        edge.source !== selectedNodeId && edge.target !== selectedNodeId
      ));
      setSelectedNodeId(null);
    }
  }, [selectedNodeId, setNodes, setEdges]);

  return {
    nodes, setNodes, onNodesChange,
    edges, setEdges, onEdgesChange,
    nodeId, setNodeId,
    inputs, setInputs,
    selectedNodeId, setSelectedNodeId,
    inputNodeCount, setInputNodeCount,
    generatedCode, setGeneratedCode,
    onDeleteNode
  };
};