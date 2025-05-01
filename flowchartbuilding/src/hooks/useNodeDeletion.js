export const useNodeDeletion = ({ selectedNodeId, setSelectedNodeId, setNodes, setEdges }) => {
    const onDeleteNode = () => {
      if (selectedNodeId) {
        setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
        setEdges((eds) => eds.filter((edge) => edge.source !== selectedNodeId && edge.target !== selectedNodeId));
        setSelectedNodeId(null);
      }
    };
  
    return { onDeleteNode };
  };
  