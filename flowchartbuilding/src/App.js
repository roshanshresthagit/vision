import "./App.css";
import TopBar from "./Components/TopBar";
import Sidebar from "./Components/Sidebar";
import FlowCanvas from "./Components/FlowCanvas";
import { useFlowData } from "./hooks/useFlowData";
import React, { useState, useCallback } from "react";
import { useEdgeManagement } from "./hooks/useEdgeManagement";
import { nodeTypes, DefaultInputList } from "./constants/nodes";
import { useNodesState, useEdgesState, useReactFlow } from "reactflow";
import { useFlowExecution } from "./hooks/useFlowExecution";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { coy } from "react-syntax-highlighter/dist/esm/styles/prism";
import { useFlowStorage } from "./hooks/useFlowStorage";

export default function App() {
  const {setViewport} = useReactFlow();
  const [nodeId, setNodeId] = useState(1);
  const [inputs, setInputs] = useState({});
  const [rfInstance, setRfInstance] = useState(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedNodeId, setSelectedNodeId] = useState(null);
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);
  const [inputNodeCount, setInputNodeCount] = useState(DefaultInputList);
  const { functionDict, functionList, functionDefinitions } = useFlowData();
  const { onSave, onRestore } = useFlowStorage({ rfInstance, setNodes, setEdges, setViewport });
  const { onConnect,onEdgeUpdateStart,onEdgeUpdate,onEdgeUpdateEnd } = useEdgeManagement(setEdges);
  const { executeFlow, generatedCode, setGeneratedCode} = useFlowExecution(nodes, edges, inputs, setNodes);


  const toggleSidebar = () => {
    setIsSidebarVisible((prev) => !prev);
  };

  const onDragStart = (event, func) => {
    event.dataTransfer.setData("application/reactflow", JSON.stringify(func));
    event.dataTransfer.effectAllowed = "move";
  };

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();
      const reactFlowBounds = event.target.getBoundingClientRect();
      const func = JSON.parse(event.dataTransfer.getData("application/reactflow"));
      const position = {
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      };
  
      const newNodeId = `${nodeId}`;
  
      const isInput = func.id === "input";
      const isImageInput = func.id === "imageinput";
      const isModelInput = func.id === "modelinput";
  
      const newNode = {
        id: newNodeId,
        type: isInput
          ? "inputNode"
          : isImageInput
          ? "imageInputNode"
          : isModelInput
          ? "modelInputNode"
          : func.id === "result"
          ? "resultNode"
          : "functionNode",
        position,
        data: {
          label: isInput
            ? `${func.label}${inputNodeCount}`
            : isImageInput
            ? `${func.label}${inputNodeCount}`
            : isModelInput
            ? `${func.label}${inputNodeCount}`
            : func.label,
          func: func.func,
          value: isInput || isImageInput || isModelInput ? 0 : undefined, 
          setValue:
            isInput || isImageInput || isModelInput
              ? (val) =>
                  setInputs((prev) => {
                    const updatedInputs = { ...prev, [newNodeId]: val };
                    setNodes((nds) =>
                      nds.map((node) =>
                        node.id === newNodeId
                          ? { ...node, data: { ...node.data, value: val } }
                          : node
                      )
                    );
                    return updatedInputs;
                  })
              : undefined,
          functionDict,
        },
      };
  
      setNodes((nds) => [...nds, newNode]);
      setNodeId((id) => id + 1);
  
      if (isInput || isImageInput) {
        setInputNodeCount((count) => count + 1);
      }
    },
    [setNodes, nodeId, inputNodeCount, functionDict]
  );
  
  const onDeleteNode = () => {
    if (selectedNodeId) {
      setNodes((nds) => nds.filter((node) => node.id !== selectedNodeId));
      setEdges((eds) => eds.filter((edge) => edge.source !== selectedNodeId && edge.target !== selectedNodeId));
      setSelectedNodeId(null);
    }
  };

  return (
    <div className="container">
      <TopBar
        toggleSidebar={toggleSidebar}
        executeFlow={executeFlow}
        onDeleteNode={onDeleteNode}
        selectedNodeId={selectedNodeId}
        nodes={nodes}
        edges={edges}
        functionDefinitions={functionDefinitions}
        setGeneratedCode={setGeneratedCode}
        onSave={onSave}
        onRestore={onRestore}
      />
      <div className="main-content">
        <Sidebar
          onDragStart={onDragStart}
          functionListCall={functionList}
          isVisible={isSidebarVisible}
        />
        <div className="canvas-container">
          <FlowCanvas
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onEdgeUpdate={onEdgeUpdate} 
            onEdgeUpdateStart={onEdgeUpdateStart}
            onEdgeUpdateEnd={onEdgeUpdateEnd}
            onConnect={onConnect}
            nodeTypes={nodeTypes}
            setSelectedNodeId={setSelectedNodeId}
            onDrop={onDrop}
            onInit={setRfInstance}
          />
          <SyntaxHighlighter language="python" style={coy}>
            {typeof generatedCode === "string"
              ? generatedCode
              : JSON.stringify(generatedCode, null, 2)}
          </SyntaxHighlighter>
        </div>
      </div>
    </div>
  );
}
